#!/usr/bin/env python3

import argparse
import json

from gopro_overlay.ffmpeg import load_gpmd_from
from gopro_overlay.gpmd import GoproMeta, interpret_item


class DataDumpVisitor:
    def __init__(self, fourcc, converter):
        self._fourcc = fourcc
        self._converter = converter
        self._counter = 0

    def vic_DEVC(self, item, contents):
        return self

    def vic_STRM(self, item, contents):
        return DataDumpStreamVisitor(
            fourcc = self._fourcc,
            visit=lambda fourcc, c: self._converter(self._counter, fourcc, c)
        )

    def v_end(self):
        self._counter += 1
        pass


class DataDumpStreamVisitor:
    def __init__(self, fourcc, visit):
        self._fourcc = fourcc
        self._visit = visit
        self._scale = None

    def vi_SCAL(self, item):
        self._scale = interpret_item(item)

    def __getattr__(self, attr):
        if attr in ['vi_' + self._fourcc, 'vi_GPSU']:
            def vi(item):
                data = interpret_item(item, self._scale)
                self._visit(item.fourcc, data)
                return data
            return vi
        else:
            raise AttributeError(attr)

    def v_end(self):
        pass


class DumpAggregateConverter:
    def __init__(self, file):
        self.time = None
        self.file = file
        self.queue = []

    def output(self, start, end, queue):
        if not queue:
            return

        # assume uniform distribution of values between two timestamps
        delta = (end - start) / len(queue)
        for i, item in enumerate(queue):
            t = start + delta*i
            d = {'timestamp': t.isoformat()}

            if hasattr(item, '_asdict'):
                d |= item._asdict()
            else:
                d['value'] = item

            json.dump(d, self.file)
            self.file.write('\n')

    def convert(self, counter, fourcc, data):
        # Find values we are interested in, bracketed between GPSU time stamps.
        if fourcc == 'GPSU':
            if self.time:
                start = self.time
                end = data
                self.output(start, end, self.queue)
            self.time = data
            self.queue = []
        else:
            if isinstance(data, list):
                self.queue.extend(data)
            else:
                self.queue.append(data)


def dump(input_file, fourcc, output_file):
    gpmd_from = load_gpmd_from(input_file)
    meta = GoproMeta.parse(gpmd_from)

    with open(output_file, 'wt', encoding='utf-8') as file:
        converter = DumpAggregateConverter(file)
        meta.accept(DataDumpVisitor(fourcc=fourcc, converter=converter.convert))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract GoPro metadata - Contributed by https://github.com/gregbaker")
    parser.add_argument("input", help="Input file")
    parser.add_argument("output", help="Output NDJSON file")
    parser.add_argument("--fourcc", "-f", action="store", default='ACCL', help='GPMD fourcc field to extract')

    args = parser.parse_args()
    dump(args.input, args.fourcc, args.output)
