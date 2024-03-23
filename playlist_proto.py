# import regex as re 
# with open('cc.html') as o:
#     te = o.read()
#     f = "www.youtube.com/watch?v="
#     fix = 0
#     hot = False
#     for c in te:
#         if c == f[fix]:
#             fix += 1
#             hot = True
#         if fix == len(f) - 1:
#             print(c)

#         o += 1
#         if o > 4200:
#             break

#     # video_links = re.findall(r"www\.youtube\.com/watch\?v=.*{1,110}\"", te)
#     # for v in video_links:
#     #     print(v)

import requests
from bs4 import BeautifulSoup

def get_video_links(playlist_url):
    video_links = []
    
    # Make an HTTP request to the playlist URL
    response = requests.get(playlist_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all the video links in the playlist
        video_tags = soup.select('.yt-simple-endpoint.style-scope.ytd-playlist-video-renderer')
        for video_tag in video_tags:
            link = 'https://www.youtube.com' + video_tag['href']
            video_links.append(link)
            
    return video_links

if __name__ == "__main__":
    playlist_url = "https://www.youtube.com/watch?v=d05K6GRJcq0"
    links = get_video_links(playlist_url)
    
    if links:
        for i, link in enumerate(links, start=1):
            print(f"{i}. {link}")
    else:
        print("No videos found in the playlist.")
