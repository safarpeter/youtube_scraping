from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import pandas as pd


browser = webdriver.Chrome()

browser.get('http://www.youtube.com')

#click to accept cookies
browser.find_element_by_xpath('/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[2]/div[2]/div[5]/div[2]/ytd-button-renderer[2]/a/tp-yt-paper-button').click()

time.sleep(2)
prev_height = browser.execute_script("return document.documentElement.scrollHeight")

while True:
    browser.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
    time.sleep(2)

    new_height = browser.execute_script("return document.documentElement.scrollHeight")

    if new_height == prev_height:
        print("Végiggörgettük az oldalt!")
        break
    prev_height = new_height

bs = BeautifulSoup(browser.page_source, "lxml")
#bs = BeautifulSoup(data, "lxml")

channel = []
title = []
views = []
upload = []
    

channel_raw = bs.findAll('a', {'class': 'yt-simple-endpoint style-scope yt-formatted-string'})
#We have to drop the last 3 results, because they have the same class like the channel names, and it would make length unmatch issues
#with the titles
channel_raw = channel_raw[:-3]
for i in range(len(channel_raw)):
    channel.append(channel_raw[i].text)

#video titles from youtube
titles_raw = bs.findAll('yt-formatted-string', {'id': 'video-title'})
print(type(titles_raw))

for i in range(len(titles_raw)):
    title.append(titles_raw[i].text)
        
'''for i in title:
    if i[:10] == "Egyveleg –":
        ch = "Egyveleg"
        channel_1half = channel[:i]
        channel_2half = channel[i:]
        channel = channel_1half + ch + channel_2half'''


    
views_raw = bs.findAll('span', {'class': 'style-scope ytd-video-meta-block'})
for i in range(len(views_raw)):
    if "aktív néző" in views_raw[i].text:
        views.append(views_raw[i].text)
        views.append('élő')
    elif "Premier" in views_raw[i].text and "várakozik" not in views_raw[i-1].text:
        views.append('premier előtt')
        views.append(views_raw[i])
    else:
        views.append(views_raw[i].text)
    #print(views_raw[i])

view_final = []


for i in range(0,len(views),2):
    view_final.append(views[i])

for i in range(1,len(views),2):
    upload.append(views[i])


final = pd.DataFrame()
#final1 = pd.DataFrame()

'''for i in views:
    print(i)'''
print(len(channel))
print(len(title))
print(len(views))

final['channel'] = channel
final['title'] = title
final['views'] = view_final
final['since_upload'] = upload
final.to_excel('results.xlsx', index=False)

