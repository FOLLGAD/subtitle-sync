import re, json

output_path = "./subtitles.ass"


def format_timestamp(time_in_seconds):
    """Converts a timestamp in seconds to ASS format (hours:minutes:seconds.centiseconds)."""
    hours, remainder = divmod(time_in_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    centiseconds = int((seconds - int(seconds)) * 100)
    return f"{int(hours):01}:{int(minutes):02}:{int(seconds):02}.{centiseconds:02}"


def highlight_current_word(sentence: str, start_index: int, current_word: str):
    """Returns the sentence with the current word highlighted."""

    highlighted_sentence = sentence[:start_index] + sentence[start_index:].replace(
        current_word, f"{{\\c&H00FF8877&}}{current_word}{{\\c&HFFFFFF&}}", 1
    )

    return highlighted_sentence


def create_subtitles(data):
    """Creates subtitles with highlighted current word within the sentence."""
    subtitles = "[Events]\n"
    subtitles += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    full_text = data["text"]

    # Split the full text into sentences based on full stops followed by a space or the end of text
    sentences = re.split(r"(?<=[。.,、，])\s*", full_text)

    # Initialize a variable to keep track of the sentence currently being processed
    current_sentence = sentences.pop(0)
    ca = 0

    for chunk in data["chunks"]:
        start_time = format_timestamp(chunk["timestamp"][0])
        end_time = format_timestamp(chunk["timestamp"][1])
        # If the chunk text is not in the current sentence, move to the next sentence

        chunk_no_punctuation = re.sub(r"[。.,、，]", "", chunk["text"])
        if chunk_no_punctuation not in current_sentence[ca:]:
            current_sentence = sentences.pop(0)
            ca = 0

        highlighted_sentence = highlight_current_word(
            current_sentence, ca, chunk["text"]
        )

        ca = current_sentence.find(chunk["text"], ca)

        subtitles += f"Dialogue: 0,{start_time},{end_time},Default,,0000,0000,0000,,{highlighted_sentence}\n"

    return subtitles


def subtitle_sync(whisper_data, chinese=False):
    # Hanzi-Pinyin-Font: https://github.com/parlr/hanzi-pinyin-font
    font = "Hanzi-Pinyin-Font" if chinese else "Arial"

    ass_header = f"""[Script Info]
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0
PlayResY: 1080
PlayResX: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font},64,&H00FFFFFF,&H00000000,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,1,0,2,10,10,20,1
    """

    # Write the ASS subtitle file
    with open(output_path, "w") as file:
        file.write(ass_header)
        file.write(create_subtitles(whisper_data))

    return output_path
