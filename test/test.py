from bs4 import BeautifulSoup

#I saved some part of YouTube to html files, because the content of YouTube is dynamic and a playlist is not always present in
#the content of the main page. We want to ignore playlists because its structure is different and would cause problems in 
#exporting data. One of them is the code of a video element and the other is the code of a playlist element.

#This is a the test case if the input is a video element.
def video_test():
    with open('video.html', encoding="utf-8") as f:
        data = f.read()

    bs = BeautifulSoup(data, "lxml")

    title = []

    divTag = bs.find_all('ytd-rich-item-renderer', {'class': 'style-scope ytd-rich-grid-renderer'})

    for tag in divTag:
        titles = tag.findAll('yt-formatted-string', {'id': 'video-title'})
        if len(titles)==1:
            title.append(titles[0].text)

    if len(title)==1:
        print(title)
        print('Test OK!')
    else:
        print('Something went wrong!')


#testing if the input is a playlist, the code should ignore the playlist, so the test case is if the input is a playlist,
#the code ignores it or not
def playlist_test():
    with open('playlist.html', encoding="utf-8") as f:
        data = f.read()

    bs = BeautifulSoup(data, "lxml")

    title = []

    divTag = bs.find_all('ytd-rich-item-renderer', {'class': 'style-scope ytd-rich-grid-renderer'})

    for tag in divTag:
        titles = tag.findAll('yt-formatted-string', {'id': 'video-title'})
        if len(titles)==1:
            title.append(titles[0].text)

    if len(title)==0:
        print('Test OK!')
    else:
        print('Something went wrong!')


video_test()
playlist_test()