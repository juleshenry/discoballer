import subprocess
import threading
import queue

def get_playlist_urls(playlist_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
        'forceurl': True,
        'simulate': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)
        if 'entries' in result:
            return [f"https://www.youtube.com/watch?v={entry['url']}" for entry in result['entries']]

MAX_CONCURRENT_CALLS = 8

def system_call(command):
    subprocess.call(command, shell=True)

def worker(queue):
    while True:
        command = queue.get()
        if command is None:
            break
        system_call(command)
        queue.task_done()

def make_system_calls(commands):
    qu = queue.Queue()
    threads = []

    for _ in range(MAX_CONCURRENT_CALLS):
        thread = threading.Thread(target=worker, args=(qu,))
        thread.start()
        threads.append(thread)

    for command in commands:
        qu.put(command)

    # Wait for all commands to finish
    qu.join()

    # Stop worker threads
    for _ in range(MAX_CONCURRENT_CALLS):
        qu.put(None)

    for thread in threads:
        thread.join()



def get_urls_from_txt(file):
    with open(file) as s:
        urls = s.readlines()
    return urls

def get_urls_from_playlist_url(playlist_url):
    from pytube import Playlist
    """
    May have to run this:
    '/Applications/Python 3.12/Install\ Certificates.command 
    """

    playlist = Playlist(playlist_url)
    return playlist.video_urls

if __name__=='__main__':
    # Example usage
    commands = []
    # get_urls_from_txt('urls.txt')
    playlist_url = 'https://youtube.com/playlist?list=PLVahv1rzEuwXMIxfsF2hftWYdyKdt-ukz&feature=shared'
    urls = get_urls_from_playlist_url(playlist_url)
    print(f'got { len(urls)} urls',)
    commands = [f"yt-dlp -x --ignore-errors --audio-format 'mp3' {x}" for x in urls]
    make_system_calls(commands)






