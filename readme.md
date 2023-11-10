# Subtitle sync (very WIP)

Add timed subtitles to a video, which highlights the current word in the subtitle.

- Whisper to transcribe audio to text with word timestamps.
- Chatgpt to correct punctuation and capitalization.

## Prerequisites

- Whisper
- https://github.com/parlr/hanzi-pinyin-font (for Chinese pinyin subtitles)
- openai

## Usage

```bash
$ python main.py input.mp4 --whisper_data data.json out.mp4
```

## Why?

Why not
