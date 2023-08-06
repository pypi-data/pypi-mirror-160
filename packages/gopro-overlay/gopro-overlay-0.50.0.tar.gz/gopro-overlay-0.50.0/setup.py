import pathlib

from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

requires = [
    "geotiler==0.14.5",
    "gpxpy==1.4.2",
    "geographiclib",
    "pillow==8.3.2",
    "pint==0.17",
    "progressbar2==3.53.3",
    "requests==2.27.1",
]

test_requirements = [
    "pytest"
]

setup(
    name="gopro-overlay",
    version="0.50.0",
    description="Overlay graphics dashboards onto GoPro footage",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/time4tea/gopro-dashboard-overlay",
    author="James Richardson",
    author_email="james+gopro@time4tea.net",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Environment :: Console",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Video",
    ],
    packages=[
        "gopro_overlay",
        "gopro_overlay.icons",
        "gopro_overlay.layouts",
    ],
    install_requires=requires,
    tests_require=test_requirements,
    scripts=[
        "bin/gopro-contrib-data-extract.py",
        "bin/gopro-cut.py",
        "bin/gopro-dashboard.py",
        "bin/gopro-extract.py",
        "bin/gopro-join.py",
        "bin/gopro-rename.py",
        "bin/gopro-to-csv.py",
        "bin/gopro-to-gpx.py",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    entry_points={
        "console_scripts": []
    },
    project_urls={
        'Source': 'https://github.com/time4tea/gopro-dashboard-overlay',
    },
)
