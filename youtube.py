from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd


browser = webdriver.Chrome()

browser.get('http://www.youtube.com')

#click to accept cookies
browser.find_element_by_xpath('/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[2]/div[2]/div[5]/div[2]/ytd-button-renderer[2]/a/tp-yt-paper-button').click()

time.sleep(2)
prev_height = browser.execute_script("return document.documentElement.scrollHeight")

#scrolling to the bottom of the page
while True:
    browser.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
    time.sleep(2)

    new_height = browser.execute_script("return document.documentElement.scrollHeight")

    if new_height == prev_height:
        print("We have reached the bottom of the page successfully!")
        break
    prev_height = new_height

bs = BeautifulSoup(browser.page_source, "lxml")

channel = []
title = []
views = []
upload = []

divTag = bs.find_all('ytd-rich-item-renderer', {'class': 'style-scope ytd-rich-grid-renderer'})

for tag in divTag:
    titles = tag.findAll('yt-formatted-string', {'id': 'video-title'})
    
    if len(titles)==1:
        title.append(titles[0].text)
        

for tag in divTag:
    channel_raw = tag.findAll('a', {'class': 'yt-simple-endpoint style-scope yt-formatted-string'})
    if len(channel_raw)==1:
        channel.append(channel_raw[0].text)

views_raw = []

for tag in divTag:
    v = tag.findAll('span', {'class': 'style-scope ytd-video-meta-block'})
    
    for i in range(len(v)):
    #if the video is a live stream, then the page doesn't show since when the video has been uploaded,
    #to handle this I appended 'élő' to the views text
        if "aktív néző" in v[i].text:
            views.append(v[i].text)
            views.append('élő')
        #if the video is a stream before premier without any waiting user, we have to write something to the number of views,
        #to handle this I appended 'premier előtt'
        elif "Premier" in v[i].text and "várakozik" not in v[i-1].text:
            views.append('premier előtt')
            views.append(v[i])
        #and if there are none of the special cases, then just simply append the text to the result list
        else:
            views.append(v[i].text)


view_final = []

#we have to divide the views list to 2 parts, starting from the first element, every second element is the number of views
for i in range(0,len(views),2):
    view_final.append(views[i])

#this loop gets the amount of time has passed since upload
for i in range(1,len(views),2):
    upload.append(views[i])


final = pd.DataFrame()

'''print(len(channel))
print(len(title))
print(len(views))'''


final['channel'] = channel
final['title'] = title
final['views'] = view_final
final['since_upload'] = upload
final.to_excel('results.xlsx', index=False)

