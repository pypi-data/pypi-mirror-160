from __future__ import annotations

import contextlib
import itertools
import json
import subprocess
from array import array
from dataclasses import dataclass
from io import BytesIO
from typing import Optional

from gopro_overlay.common import temporary_file
from gopro_overlay.dimensions import Dimension
from gopro_overlay.execution import InProcessExecution
from gopro_overlay.functional import flatten


def run(cmd, **kwargs):
    return subprocess.run(cmd, check=True, **kwargs)


def invoke(cmd, **kwargs):
    try:
        return run(cmd, **kwargs, text=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise IOError(f"Error: {cmd}\n stdout: {e.stdout}\n stderr: {e.stderr}")


@dataclass(frozen=True)
class MetaMeta:
    stream: int
    frame_count: int
    timebase: int
    frame_duration: int


@dataclass(frozen=True)
class StreamInfo:
    audio: Optional[int]
    video: int
    meta: MetaMeta
    video_dimension: Dimension


def cut_file(input, output, start, duration):
    streams = find_streams(input)

    maps = list(itertools.chain.from_iterable(
        [["-map", f"0:{stream}"] for stream in [streams.video, streams.audio, streams.meta.stream] if stream is not None]))

    args = ["ffmpeg",
            "-hide_banner",
            "-y",
            "-i", input,
            "-map_metadata", "0",
            *maps,
            "-copy_unknown",
            "-ss", str(start),
            "-t", str(duration),
            "-c", "copy",
            output]

    print(args)

    run(args)


def join_files(filepaths, output):
    """only for joining parts of same trip"""

    streams = find_streams(filepaths[0])

    maps = list(itertools.chain.from_iterable(
        [["-map", f"0:{stream}"] for stream in [streams.video, streams.audio, streams.meta.stream] if stream is not None]))

    with temporary_file() as commandfile:
        with open(commandfile, "w") as f:
            for path in filepaths:
                f.write(f"file '{path}\n")

        args = ["ffmpeg",
                "-hide_banner",
                "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", commandfile,
                "-map_metadata", "0",
                *maps,
                "-copy_unknown",
                "-c", "copy",
                output]
        print(f"Running {args}")
        run(args)


def find_frame_duration(filepath, data_stream_number, invoke=invoke):

    ffprobe_output = str(invoke(
        ["ffprobe",
         "-hide_banner",
         "-print_format", "json",
         "-show_packets",
         "-select_streams", str(data_stream_number),
         "-read_intervals", "%+#1",
         filepath]
    ).stdout)

    ffprobe_packet_data = json.loads(ffprobe_output)
    packet = ffprobe_packet_data["packets"][0]

    duration = int(packet["duration"])

    return duration


def find_streams(filepath, invoke=invoke, find_frame_duration=find_frame_duration) -> StreamInfo:
    ffprobe_output = str(invoke(["ffprobe", "-hide_banner", "-print_format", "json", "-show_streams", filepath]).stdout)

    ffprobe_json = json.loads(ffprobe_output)

    video_selector = lambda s: s["codec_type"] == "video"
    audio_selector = lambda s: s["codec_type"] == "audio"
    data_selector = lambda s: s["codec_type"] == "data" and s["codec_tag_string"] == "gpmd"

    def first_and_only(what, l, p):
        matches = list(filter(p, l))
        if not matches:
            raise IOError(f"Unable to find {what} in ffprobe output")
        if len(matches) > 1:
            raise IOError(f"Multiple matching streams for {what} in ffprobe output")
        return matches[0]

    def only_if_present(what, l, p):
        matches = list(filter(p, l))
        if matches:
            return first_and_only(what, l, p)

    streams = ffprobe_json["streams"]
    video = first_and_only("video stream", streams, video_selector)
    video_stream = video["index"]
    video_dimension = Dimension(video["width"], video["height"])

    audio = only_if_present("audio stream", streams, audio_selector)
    audio_stream = None
    if audio:
        audio_stream = audio["index"]

    meta = first_and_only("metadata stream", streams, data_selector)

    data_stream_number = int(meta["index"])

    meta_meta = MetaMeta(
        stream=data_stream_number,
        frame_count=int(meta["nb_frames"]),
        timebase=int(meta["time_base"].split("/")[1]),
        frame_duration=find_frame_duration(filepath, data_stream_number, invoke)
    )

    if video_stream is None or meta_meta.stream is None or video_dimension is None:
        raise IOError("Invalid File? The data stream doesn't seem to contain GoPro video & metadata ")

    return StreamInfo(audio=audio_stream, video=video_stream, meta=meta_meta, video_dimension=video_dimension)


def load_gpmd_from(filepath):
    track = find_streams(filepath).meta.stream
    if track:
        cmd = ["ffmpeg", "-hide_banner", '-y', '-i', filepath, '-codec', 'copy', '-map', '0:%d' % track, '-f',
               'rawvideo', "-"]
        result = run(cmd, capture_output=True, timeout=10)
        if result.returncode != 0:
            raise IOError(f"ffmpeg failed code: {result.returncode} : {result.stderr.decode('utf-8')}")
        arr = array("b")
        arr.frombytes(result.stdout)
        return arr


def ffmpeg_is_installed():
    try:
        invoke(["ffmpeg", "-version"])
        return True
    except FileNotFoundError:
        return False


def ffmpeg_libx264_is_installed():
    output = invoke(["ffmpeg", "-v", "quiet", "-codecs"]).stdout
    libx264s = [x for x in output.split('\n') if "libx264" in x]
    return len(libx264s) > 0


# ffprobe -hide_banner -print_format json -show_packets -select_streams 3 -read_intervals '%+#1'  GH010278.MP4
# {
#     "packets": [
#         {
#             "codec_type": "data",
#             "stream_index": 3,
#             "pts": 0,
#             "pts_time": "0.000000",
#             "dts": 0,
#             "dts_time": "0.000000",
#             "duration": 1001,
#             "duration_time": "1.001000",
#             "size": "4248",
#             "pos": "7867500",
#             "flags": "K_"
#         }
#     ]
# }

class DiscardingBytesIO(BytesIO):

    def __init__(self, initial_bytes: bytes = ...) -> None:
        super().__init__(bytes())

    def write(self, buffer) -> int:
        return len(buffer)


class FFMPEGNull:

    @contextlib.contextmanager
    def generate(self):
        yield DiscardingBytesIO()


class FFMPEGGenerate:

    def __init__(self, output, overlay_size: Dimension, execution=None):
        self.output = output
        self.overlay_size = overlay_size
        self.execution = execution if execution else InProcessExecution()

    @contextlib.contextmanager
    def generate(self):
        cmd = [
            "ffmpeg",
            "-hide_banner",
            "-y",
            "-loglevel", "info",
            "-f", "rawvideo",
            "-framerate", "10.0",
            "-s", f"{self.overlay_size.x}x{self.overlay_size.y}",
            "-pix_fmt", "rgba",
            "-i", "-",
            "-r", "30",
            "-vcodec", "libx264",
            "-preset", "veryfast",
            self.output
        ]

        yield from self.execution.execute(cmd)


class FFMPEGOptions:

    def __init__(self, input=None, output=None):
        self.input = input if input is not None else []
        self.output = output if output is not None else ["-vcodec", "libx264", "-preset", "veryfast"]
        self.general = ["-hide_banner", "-loglevel", "info"]

    def set_input_options(self, options):
        self.input = options

    def set_output_options(self, options):
        self.output = options


class FFMPEGOverlay:

    def __init__(self, input, output, overlay_size: Dimension, options: FFMPEGOptions = None, vsize=1080,
                 execution=None):
        self.output = output
        self.input = input
        self.options = options if options else FFMPEGOptions()
        self.overlay_size = overlay_size
        self.vsize = vsize
        self.execution = execution if execution else InProcessExecution()

    @contextlib.contextmanager
    def generate(self):
        if self.vsize == 1080:
            filter_extra = ""
        else:
            filter_extra = f",scale=-1:{self.vsize}"
        cmd = flatten([
            "ffmpeg",
            "-y",
            self.options.general,
            self.options.input,
            "-i", self.input,
            "-f", "rawvideo",
            "-framerate", "10.0",
            "-s", f"{self.overlay_size.x}x{self.overlay_size.y}",
            "-pix_fmt", "rgba",
            "-i", "-",
            "-filter_complex", f"[0:v][1:v]overlay{filter_extra}",
            self.options.output,
            self.output
        ])

        yield from self.execution.execute(cmd)


if __name__ == "__main__":
    print(ffmpeg_libx264_is_installed())
