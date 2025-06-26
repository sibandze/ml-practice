import yt_dlp as YOUTUBE
import os
import re

def download_video(url, output_dir):
    temp_dir = os.path.join(os.getcwd(), f".youtube_downloader/.{get_filename(url)}")
    os.makedirs(temp_dir, exist_ok=True)
    with open(os.path.join(temp_dir, ".url"), "w") as f:
        f.write(url)
    ydl_opts = {
        'format': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
        'noplaylist': True,
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'progress_hooks': [lambda d: progress_hook(d, temp_dir, output_dir)],
        'retries': 10,
        'fragment_retries': 10,
    }
    try:
        with YOUTUBE.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Error downloading video: {e}")

def slugify(s):
    return re.sub(r'\W+', '_', s)

def get_filename(url):
    with YOUTUBE.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        return slugify(info['title'])
def progress_hook(d, temp_dir, output_dir):
    if d['status'] == 'downloading':
        percent = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1)
        print(f"\rDownloading: {percent*100:.2f}%", end='')
    elif d['status'] == 'finished':
        print("\nDownload finished. Finalizing...")
    else:
        print(d['status'])
    if d['status'] == 'postprocessed':
        print("\nPostprocessing complete. Moving to output directory...")
        for file in os.listdir(temp_dir):
            if file != ".url" and file != ".title":
                os.replace(os.path.join(temp_dir, file), os.path.join(output_dir, file))
        os.remove(os.path.join(temp_dir, ".url"))
        os.remove(os.path.join(temp_dir, ".title"))
        os.rmdir(temp_dir)
        print("Download complete.")

def resume_download(output_dir):
    temp_dirs = [d for d in os.listdir(os.path.join(os.getcwd(), ".youtube_downloader")) if os.path.isdir(os.path.join(os.getcwd(), ".youtube_downloader", d))]
    if not temp_dirs:
        print("No partial downloads found.")
        return
    for i, temp_dir in enumerate(temp_dirs):
        print(f"{i+1}. {temp_dir}")
    choice = input("Enter the number of the download to resume, or 'all' to resume all: ")
    if not choice or choice.lower() == 'all':
        for temp_dir in temp_dirs:
            url = open(os.path.join(os.getcwd(), ".youtube_downloader", temp_dir, ".url"), "r").read().strip()
            ydl_opts = {
                'format': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
                'noplaylist': True,
                'outtmpl': os.path.join(os.getcwd(), ".youtube_downloader", temp_dir, '%(title)s.%(ext)s'),
                'progress_hooks': [lambda d: progress_hook(d, os.path.join(os.getcwd(), ".youtube_downloader", temp_dir), output_dir)],
                'retries': 10,
                'fragment_retries': 10,
            }
            try:
                with YOUTUBE.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            except Exception as e:
                print(f"Error resuming download: {e}")
    else:
        try:
            choice = int(choice)
            if 1 <= choice <= len(temp_dirs):
                temp_dir = temp_dirs[choice - 1]
                url = open(os.path.join(os.getcwd(), ".youtube_downloader", temp_dir, ".url"), "r").read().strip()
                ydl_opts = {
                    'format': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
                    'noplaylist': True,
                    'outtmpl': os.path.join(os.getcwd(), ".youtube_downloader", temp_dir, '%(title)s.%(ext)s'),
                    'progress_hooks': [lambda d: progress_hook(d, os.path.join(os.getcwd(), ".youtube_downloader", temp_dir), output_dir)],
                    'retries': 10,
                    'fragment_retries': 10,
                }
                try:
                    with YOUTUBE.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                except Exception as e:
                    print(f"Error resuming download: {e}")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")

def main():
    os.makedirs(os.path.join(os.getcwd(), ".youtube_downloader"), exist_ok=True)
    while True:
        print("   1.Download a new video")
        print("   2. Resume a partial download")
        print("   q. QUIT")
        choice = input("   Enter your choice: ")
        if choice == '1':
            url = input("Enter the YouTube video URL: ")
            default_dir = os.path.expanduser("~/storage/downloads")
            if not os.path.exists(default_dir):
                os.makedirs(default_dir)
            
            download_video(url, default_dir)
        elif choice == '2':
            default_dir = os.path.expanduser("~/storage/downloads")
            if not os.path.exists(default_dir):
                os.makedirs(default_dir)
            resume_download(default_dir)

        elif choice.lower() == 'q':
             print("   Stopping application...")
             break
            
        else:
            print("   Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
