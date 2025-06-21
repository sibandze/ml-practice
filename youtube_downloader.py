import yt_dlp as YOUTUBE
import re as RE
import os

def get_video_info(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'noplaylist': True,
    }
    with YOUTUBE.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info

def get_available_qualities(info):
    formats = info['formats']
    available_qualities = set()
    for f in formats:
      resolution = f.get('resolution', '')
      match = RE.search(r'(\d+)p', resolution)
      if match:
        available_qualities.add(int(match.group(1)))
    return sorted(list(available_qualities))

def get_format_id(info, quality):
    formats = info['formats']
    best_format_id = None
    best_diff = float('inf')
    for f in formats:
            resolution = f.get('resolution', '')
            match = RE.search(r'(\d+)p', resolution)
            if match:
                resolution = int(match.group(1))
                diff = abs(resolution - quality)
                if diff < best_diff:
                    best_diff = diff
                    best_format_id = f['format_id']
    return best_format_id

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
        percent = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1)
        print(f"\rDownloading: {percent*100:.2f}%", end='')
    elif d['status'] == 'finished':
        print("\nDownload finished.")

def main():
    url = input("Enter the YouTube video URL: ")
    info = get_video_info(url)
    available_qualities = get_available_qualities(info)
    if not available_qualities:
        print("No formats available.")
        return

    print("Available qualities:")
    for i, quality in enumerate(available_qualities, start=1):
        print(f"{i}. {quality}p")

    choice = input("Enter the number of the quality you want to download: ")
    try:
        choice = int(choice)
        if choice < 1 or choice > len(available_qualities):
            raise ValueError
    except ValueError:
        print("Invalid choice.")
        return

    quality = available_qualities[choice - 1]
    format_id = get_format_id(info, quality)

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
