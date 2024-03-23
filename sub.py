import subprocess
import threading
import queue
import youtube_dl

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



if __name__=='__main__':
    # Example usage
    commands = []
    playlist_url = "https://www.youtube.com/playlist?list=PLQeroY7XkiFH5KX5HmoAirEvluDtPhRpd"
    urls = get_playlist_urls(playlist_url)
    print(urls[0])
    commands = [f"youtube-dl -x --audio-format 'mp3' {x}" for x in urls]
    make_system_calls(commands)






