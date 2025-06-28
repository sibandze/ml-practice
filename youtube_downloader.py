import yt_dlp as YOUTUBE
import os
import shutil
import re
DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), ".youtube_downloader")
def download_video(url, output_dir):
    title = get_filename(url)
    temp_dir = os.path.join(DOWNLOAD_DIR, slugify(title))
    os.makedirs(temp_dir, exist_ok=True)
    with open(os.path.join(temp_dir, ".url"), "w") as f:
        f.write(url)
    with open(os.path.join(temp_dir, ".title"), "w") as f:
        f.write(title)
    ydl_opts = {
        'format': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'progress_hooks': [lambda d: progress_hook(d, temp_dir, output_dir)],
        'retries': 10,
        'fragment_retries': 10,
    }
    try:
        with YOUTUBE.YoutubeDL(ydl_opts) as ydl:
            print()
            print(f"  Downloading: {title}")
            print()
            ydl.download([url])
        post_processed(temp_dir, output_dir)
    except Exception as e:
        print(f"Error downloading video: {e}")

def slugify(s):
    return re.sub(r'\W+', '_', s)
    
def get_filename(url):
    with YOUTUBE.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['title']
        
def progress_hook(d, temp_dir, output_dir):
    if d['status'] == 'downloading':
        percent = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1)
        print(f"\rDownloading: {percent*100:.2f}%", end='')
    elif d['status'] == 'finished':
        print("\nPartial download finished. Finalizing...")
    else:
        print("Status: ",d['status'])
        
def post_processed(temp_dir, output_dir):
        print("\nPostprocessing complete. Moving to output directory...")
        try:        
            for file in os.listdir(temp_dir):
                if file != ".url" and file != ".title":
                    shutil.move(os.path.join(temp_dir, file), os.path.join(output_dir, file))
            os.remove(os.path.join(temp_dir, ".url"))
            os.remove(os.path.join(temp_dir, ".title"))
            os.rmdir(temp_dir)
            print("Download complete.")
        except Exception as e:
            print(f"Error moving files: {e}")
    
    

def resume_download(output_dir):
    temp_dirs = [d for d in os.listdir(DOWNLOAD_DIR) if os.path.isdir(os.path.join(DOWNLOAD_DIR, d))]
    if not temp_dirs:
        print("No partial downloads found.")
        return
    titles = []
    for i, temp_dir in enumerate(temp_dirs):
        title = open(os.path.join(DOWNLOAD_DIR,temp_dir, ".title"), "r").read().strip()
        titles.append(title)
        print(f"{i+1}. {title}")
    choice = input("Enter the number of the download to resume, or 'all' to resume all: ")
    if not choice or choice.lower() == 'all':
        for idx, temp_dir in enumerate(temp_dirs):
            temp_dir = os.path.join(DOWNLOAD_DIR, temp_dir)
            url = open(os.path.join(temp_dir, ".url"), "r").read().strip()
            ydl_opts = {
                'format': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
                'noplaylist': True,
                'quiet': True,
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'progress_hooks': [lambda d: progress_hook(d, temp_dir, output_dir)],
                'retries': 10,
                'fragment_retries': 10,
            }
            try:
                with YOUTUBE.YoutubeDL(ydl_opts) as ydl:
                    print()
                    print(f"  Downloading: {titles[idx]}")
                    print()
                    ydl.download([url])
                post_processed(temp_dir, output_dir)
            except Exception as e:
                print(f"Error resuming download: {e}")
    else:
        try:
            choice = int(choice)
            if 1 <= choice <= len(temp_dirs):
                temp_dir = os.path.join(DOWNLOAD_DIR, temp_dirs[choice - 1])
                url = open(os.path.join(temp_dir, ".url"), "r").read().strip()
                ydl_opts = {
                    'format': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
                    'noplaylist': True,
                    'quiet': True,
                    'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                    'progress_hooks': [lambda d: progress_hook(d, os.path.join(DOWNLOAD_DIR, temp_dir), output_dir)],
                    'retries': 10,
                    'fragment_retries': 10,
                }
                try:
                    with YOUTUBE.YoutubeDL(ydl_opts) as ydl:
                        print()
                        print(f"  Downloading: {titles[choice-1]}")
                        print()
                        ydl.download([url])
                    post_processed(temp_dir, output_dir)
                        
                except Exception as e:
                    print(f"Error resuming download: {e}")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")

def main():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
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
