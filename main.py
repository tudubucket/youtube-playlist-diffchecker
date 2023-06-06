from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

api_key = 'AIzaSyAvOJy1TRvrU2uaFqLe-75dPnU5t2ib-2o' 
youtube = build('youtube', 'v3', developerKey=api_key)

playlist1_id = 'PLV2M9Tvv_Ru7PS05zvBNhAfW8_FMK4G0f' 
playlist2_id = 'PLV2M9Tvv_Ru7czZvf0YRTDUTYwKv6ebFz'  

playlist1_videos = []
playlist1_page_tokens = []
next_page_token = None

def get_all_playlist_videos(playlist_id):
    videos = []
    next_page_token = None
    while True:
        try:
            playlist_response = youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            for item in playlist_response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                videos.append(video_id)

            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token:
                break
        except HttpError as e:
            print(f'An error occurred: {e}')
            break
    return videos

def chunk_list(lst, chunk_size):
    return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]

while True:
    try:
        playlist_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist1_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in playlist_response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            playlist1_videos.append(video_id)

        next_page_token = playlist_response.get('nextPageToken')
        if next_page_token:
            playlist1_page_tokens.append(next_page_token)

        if not next_page_token:
            break
    except HttpError as e:
        print(f'An error occurred: {e}')
        break

playlist2_videos = []
playlist2_page_tokens = []
next_page_token = None
while True:
    try:
        playlist_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist2_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in playlist_response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            playlist2_videos.append(video_id)

        next_page_token = playlist_response.get('nextPageToken')
        if next_page_token:
            playlist2_page_tokens.append(next_page_token)

        if not next_page_token:
            break
    except HttpError as e:
        print(f'An error occurred: {e}')
        break

for page_token in playlist1_page_tokens:
    try:
        playlist_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist1_id,
            maxResults=50,
            pageToken=page_token
        ).execute()

        for item in playlist_response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            playlist1_videos.append(video_id)
    except HttpError as e:
        print(f'An error occurred: {e}')
        break

for page_token in playlist2_page_tokens:
    try:
        playlist_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist2_id,
            maxResults=50,
            pageToken=page_token
        ).execute()

        for item in playlist_response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            playlist2_videos.append(video_id)
    except HttpError as e:
        print(f'An error occurred: {e}')
        break

only_in_playlist1 = set(playlist1_videos) - set(playlist2_videos)
only_in_playlist2 = set(playlist2_videos) - set(playlist1_videos)

print(f'Videos only in playlist 1: {only_in_playlist1}')
print(f'Videos only in playlist 2: {only_in_playlist2}')
