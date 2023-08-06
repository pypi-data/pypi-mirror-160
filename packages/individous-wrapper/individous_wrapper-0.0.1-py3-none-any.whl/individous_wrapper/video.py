from bs4 import BeautifulSoup
import requests
def page(video_id, instance = "invidious.sethforprivacy.com"):
    page = requests.get(f"https://{instance}/watch?v={video_id}")
    return {"page": page, "video_id": video_id}
def views(page):
    soup = BeautifulSoup(page["page"].content, 'html.parser')
    views = soup.find('p',attrs={'id':'views'})
    views = str(views)
    views = views.split()
    views = views[4].replace("</p>","").replace(",","")
    return int(views)
def likes(page):
    soup = BeautifulSoup(page["page"].content, 'html.parser')
    likes = soup.find('p',attrs={'id':'likes'})
    likes = str(likes)
    likes = likes.split()
    likes = likes[4].replace("</p>","")
    likes = likes.replace(",","")
    return int(likes)
def title(page):
    soup = BeautifulSoup(page["page"].content, 'html.parser')
    title = soup.find('h1')
    title = str(title)
    title = title.replace(f'\n        \n            <a href="/watch?v={page["video_id"]}&amp;listen=1" title="Audio mode">\n<i class="icon ion-md-headset"></i>\n</a>\n</h1>',"")
    title = title.replace('<h1>\n        ',"")
    title = title.replace('&amp;', '')
    return str(title)
def channel(page):
    soup = BeautifulSoup(page["page"].content, 'html.parser')
    span = soup.find('span',attrs={'id':'channel-name'})
    channel = str(span)
    channel = channel.replace('<span id="channel-name">',"")
    channel = channel.replace('</span>',"")
    channel = channel.replace('&amp;', '')
    return str(channel)
def get_all(vid_id, instance = "invidious.sethforprivacy.com"):
    _page = page(vid_id, instance = "invidious.sethforprivacy.com")
    return {"views": views(_page), "likes": likes(_page), "title": title(_page), "channel": channel(_page)}
