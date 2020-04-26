# YT-DL-MP3
A small command-line tool with a simple set of options for downloading MP3s using youtube-dl.

## Usage
YT-DL-MP3 can download an MP3 from a YouTube link provided as an argument or display a full menu of available options when launched without arguments
- Download one link: `python yt-dl-mp3.py https://www.youtube.com/watch?v=dv13gl0a-FA`
- Display all options: `python yt-dl-mp3.py`

## Download Options
Default download options are included in `options.json`. Options that can be changed at runtime are:
- File bitrate (`192`/`256`/`320`)
- Embed thumbnail (`true`/`false`)

## Planned Work
- Batch download (using a text file containing links)
- More download options