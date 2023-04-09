# Zack Jarski - jarskiz

import sys
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build


if __name__ == '__main__':
    api_key = <YouTube API Key>
    yt = build('youtube', 'v3', developerKey=api_key)

    # Add URLs here
    URLs = [
        'https://www.youtube.com/watch?v=YbJOTdZBX1g'
    ]
    
    vids = []
    titles = []

    for url in URLs:
        response = yt.search().list(
                part='snippet',
                maxResults=1,
                q=url
            ).execute()
        vids.append(response['items'][0]['id']['videoId'])
        titles.append(response['items'][0]['snippet']['title'])

    resultCnt = 50
    for n in range(len(URLs)):
        request = yt.commentThreads().list(
                part='snippet',
                maxResults=resultCnt,
                order='relevance',
                textFormat='plainText',
                videoId=vids[n]
            )
        response = request.execute()

        # print(response['pageInfo']['totalResults'])
        with open('commentdata.output', 'w', encoding='utf8') as f:
            f.write('Video Title: '+titles[n]+'\nVideo URL: '+URLs[n]+'\nVideo ID: '+vids[n]+'\nComments:\n')
            for i in range(resultCnt):
                f.write('\t'+str(i+1)+'.) '+str(response['items'][i]['snippet']['topLevelComment']['snippet']['likeCount'])+' Likes | '+response['items'][i]['snippet']['topLevelComment']['snippet']['textDisplay']+'\n')
    
    yt.close()