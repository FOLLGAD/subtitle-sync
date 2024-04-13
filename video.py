import subprocess


def ffmpeg_add_subs(video_file, subtitle_file, outfile):
    """Add subtitles using ffmpeg"""
    print("Adding subtitles to video file... Might take a while...")
    quiet = False
    loglevel = "panic" if quiet else "info"
    command = f"""ffmpeg -y -loglevel {loglevel} -i {video_file} -vf "ass={subtitle_file}" -c:v libx264 -c:a copy {outfile}"""
    subprocess.run(command, shell=True)

    return outfile
