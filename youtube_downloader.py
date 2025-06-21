import yt_dlp as YOUTUBE
import os

def get_video_info(url):
    ydl_opts = {
        'noplaylist': True,
    }
    with YOUTUBE.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info

def get_available_formats(info):
    formats = info['formats']
    available_formats = {}
    for f in formats:
        format_id = f['format_id']
        format_note = f.get('format_note', '')
        ext = f.get('ext', '')
        available_formats[format_id] = f"{format_note} - {ext}"
    return available_formats

def download_video(url, format_id, output_dir):
    ydl_opts = {
        'format': format_id,
        'noplaylist': True,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'retries': 10,
        'fragment_retries': 10,
    }
    with YOUTUBE.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1)
        print(f"\rDownloading: {percent*100:.2f}%", end='')
    elif d['status'] == 'finished':
        print("\nDownload finished.")

def main():
    url = input("Enter the YouTube video URL: ")
    info = get_video_info(url)
    available_formats = get_available_formats(info)
    if not available_formats:
        print("No formats available.")
        return

    print("Available formats:")
    for i, (format_id, format_note) in enumerate(available_formats.items(), start=1):
        print(f"{i}. {format_note} ({format_id})")

    choice = input("Enter the number of the format you want to download: ")
    try:
        choice = int(choice)
        if choice < 1 or choice > len(available_formats):
            raise ValueError
    except ValueError:
        print("Invalid choice.")
        return

    format_id = list(available_formats.keys())[choice - 1]
    default_dir = os.path.expanduser("~/storage/downloads")
    if not os.path.exists(default_dir):
        os.makedirs(default_dir)

    output_dir = input(f"Enter the output directory (default={default_dir}): ")
    if not output_dir:
        output_dir = default_dir
    elif not os.path.exists(output_dir):
        os.makedirs(output_dir)

    download_video(url, format_id, output_dir)

if __name__ == "__main__":
    main()
