import argparse, json
from fix_punctuation import fix_punctuation
from subtitle_sync import subtitle_sync
from video import ffmpeg_add_subs


def main():
    parser = argparse.ArgumentParser(description="Process some files.")
    parser.add_argument("video_file", help="Path to the input video to add subtitles to")
    parser.add_argument("out_file", help="Path to the output video")

    parser.add_argument(
        "--whisper_data", help="The whisper JSON data. Must have word-level timestamps."
    )
    parser.add_argument(
        "--chinese", action="store_true", help="Process Chinese subtitles"
    )

    parser.add_argument(
        "--fix-punctuation",
        action="store_true",
        help="Fix punctuation in subtitles using OpenAI",
    )

    args = parser.parse_args()

    data = json.load(open(args.whisper_data, encoding="utf-8"))

    if args.fix_punctuation:
        data["text"] = fix_punctuation(data["text"])

    print(f"Processing file: {args.video_file}")
    subtitle_file = subtitle_sync(data, chinese=args.chinese)
    outfile = ffmpeg_add_subs(args.video_file, subtitle_file, args.out_file)

    print(f"Subtitles added to {outfile}")


if __name__ == "__main__":
    main()
