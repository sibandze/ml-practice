import yt_dlp as YOUTUBE
import os

def download_video(url, output_dir):
    ydl_opts = {
        'format': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
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
    default_dir = os.path.expanduser("~/storage/downloads")
    if not os.path.exists(default_dir):
        os.makedirs(default_dir)

    output_dir = input(f"Enter the output directory (default={default_dir}): ")
    if not output_dir:
        output_dir = default_dir
    elif not os.path.exists(output_dir):
        os.makedirs(output_dir)

    download_video(url, output_dir)

if __name__ == "__main__":
    main()
