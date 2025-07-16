import yt_dlp as YOUTUBE
import sys
import os
import shutil
import re

DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), ".youtube_music_downloader")
default_dir = os.path.expanduser("~/storage/downloads/music")

def download_video_content(title, temp_dir, output_dir, url):
    ydl_opts = {
        'format': 'bestaudio',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'noprogress': True,
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
        }],
        'progress_hooks': [lambda d: progress_hook(d, temp_dir, output_dir)],
        'retries': 100,
        'fragment_retries': 100,
    }
    try:
        with YOUTUBE.YoutubeDL(ydl_opts) as ydl:
            print()
            print(f"   Downloading: {title}")
            print()
            ydl.download([url])
            post_processed(temp_dir, output_dir)
    except Exception as e:
        print(f"   Error downloading video: {e}")
        
def download_video(url, output_dir):
    title = get_filename(url)
    temp_dir = os.path.join(DOWNLOAD_DIR, slugify(title))
    os.makedirs(temp_dir, exist_ok=True)
    with open(os.path.join(temp_dir, ".url"), "w") as f:
        f.write(url)
    with open(os.path.join(temp_dir, ".title"), "w") as f:
        f.write(title)
    remove_url_from_temp_file(url)
    download_video_content(title, temp_dir, output_dir, url)
    
def slugify(s):
    return re.sub(r'\W+', '_', s)
    
def get_filename(url):
    with YOUTUBE.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['title']
        
def toMB(bytes):
    return bytes/(2**20)

def toKB(bytes):
    return bytes/(2**10)

def write_url_to_temp_file(url):
    urls_file = os.path.join(DOWNLOAD_DIR, '.urls')
    with open(urls_file, 'a') as f:
       f.write(url+'/n')

def remove_url_from_temp_file(url):
     urls_file = os.path.join(DOWNLOAD_DIR, '.urls')
     try:
          with open(urls_file, 'r') as f:
               urls = f.readlines()
          with open(urls_file, 'w') as f:
               for u in urls:
                    if u.strip() != url:
                         f.append(u)
     except  FileNotFoundError:
          pass

def progress_hook(d, temp_dir, output_dir):
    if d['status'] == 'downloading':
        percent = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1)
        print(f"\r\033[K   Downloading: {percent*100:.2f}% {toMB(d.get('downloaded_bytes',0)):.2f}MB of {toMB(d.get('total_bytes',1)):.2f}MB at {toKB(d.get('speed',0)):.2f}kbps", end='')
    elif d['status'] == 'finished':
        print("\n   Partial download finished. Finalizing...")
            
def post_processed(temp_dir, output_dir):
        print("\n   Postprocessing complete. Moving to output directory...")
        try:        
            for file in os.listdir(temp_dir):
                if file != ".url" and file != ".title":
                    shutil.move(os.path.join(temp_dir, file), os.path.join(output_dir, file))
            os.remove(os.path.join(temp_dir, ".url"))
            os.remove(os.path.join(temp_dir, ".title"))
            os.rmdir(temp_dir)
            print("   Download complete.")
        except Exception as e:
            print(f"   Error moving files: {e}")
    
    

def resume_download(output_dir):
    temp_dirs = [d for d in os.listdir(DOWNLOAD_DIR) if os.path.isdir(os.path.join(DOWNLOAD_DIR, d))]
    
    titles = []
    for i, temp_dir in enumerate(temp_dirs):
        title = open(os.path.join(DOWNLOAD_DIR,temp_dir, ".title"), "r").read().strip()
        titles.append(title)
        print(f"   {i+1}. {title},")

    with open(os.path.join(DOWNLOAD_DIR, 'urls'), 'r') as f:
         urls = f.readlines()
         if urls:
             print(f"   and {len(urls)} others." if titles else f"   {len(urls)} urls")
    if not temp_dirs and not urls:
        print("   No partial downloads found.")
        return
    choice = input("   Enter the number of the download to resume, or 'all' to resume all: ")
    if not choice or choice.lower() == 'all':
        for idx, temp_dir in enumerate(temp_dirs):
            temp_dir = os.path.join(DOWNLOAD_DIR, temp_dir)
            url = open(os.path.join(temp_dir, ".url"), "r").read().strip()
            download_video_content(titles[idx], temp_dir, output_dir, url)
        for url in urls:
            try:
                download_video(url.strip(), default_dir)
            except Exception as e:
                print(f"   Error downloading {url.strip()}. More details {e}")
                        
    else:
        try:
            choice = int(choice)
            if 1 <= choice <= len(temp_dirs):
                temp_dir = os.path.join(DOWNLOAD_DIR, temp_dirs[choice - 1])
                url = open(os.path.join(temp_dir, ".url"), "r").read().strip()
                download_video_content(titles[choice-1], temp_dir, output_dir, url)
            else:
                print("   Invalid choice.")
        except ValueError:
            print("   Invalid input.")

def main():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    if not os.path.exists(default_dir):
        os.makedirs(default_dir)
    for i in range(1, len(sys.argv)):
        write_url_to_temp_file(sys.argv[i])
    for i in range(1,len(sys.argv)):
        try:
            download_video(sys.argv[i], default_dir)
        except Exception as e:
            print(f"   Error downloading {sys.argv[i]}. More details {e}")
            
            
        
    while True:
        print("   1. Download a new audio")
        print("   2. Resume a partial download")
        print("   q. QUIT")
        choice = input("   Enter your choice: ")
        if choice == '1':
            url = input("   Enter the YouTube video URL: ")
            write_url_to_temp_file(url)
            try:
                download_video(url, default_dir)
            except Exception as e:
                print(f"   Error downloading {url}. More details {e}")


        elif not choice or choice == '2':
            resume_download(default_dir)

        elif choice.lower() == 'q':
             print("   Stopping application...")
             break
            
        else:
            print("   Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
