import subprocess


def ffmpeg_add_subs(video_file, subtitle_file, outfile):
    """Add subtitles using ffmpeg"""
    command = f"""ffmpeg -y -loglevel panic -i {video_file} -vf "ass={subtitle_file}" -c:v libx264 -c:a copy {outfile}"""
    subprocess.run(command, shell=True)

    return outfile
