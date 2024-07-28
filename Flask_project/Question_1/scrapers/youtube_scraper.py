from googleapiclient.discovery import build

API_KEY = 'AIzaSyAlUrbV1HDmUJ-2WzT6wa4UtkCl2L5BkoI'

def scrape_youtube(query, max_results=10):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    request = youtube.search().list(
        q=query,
        type='video',
        part='id,snippet',
        maxResults=max_results
    )
    response = request.execute()
    
    videos = []
    for item in response['items']:
        video = {
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'thumbnail': item['snippet']['thumbnails']['default']['url'],
            'video_id': item['id']['videoId']
        }
        videos.append(video)
    
    return videos