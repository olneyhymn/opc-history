import re
import datetime as dt
import twitter as tw
import json


def update_facebook(title, url):
    import facebook
    with open('facebook.txt', 'r') as f:
        access_token = f.read().strip()
    api = facebook.GraphAPI(access_token)

    try:
        api.put_wall_post("", attachment={"link": url, "name": title})
        return "Successfully posted to Facebook"
    except facebook.GraphAPIError as e:
        return "Error", e


def get_today():
    import requests
    r = requests.request("GET", "http://opc.org/today.html?target=archive")
    for date, path, title in re.findall(r'<p>([A-Za-z]+ [0-9]+)<br /><a href="(.*?)">(.*?)</a></p>', r.text):
        if date == dt.datetime.now().strftime("%B %-d"):
            return title, "http://www.opc.org{}".format(path)


def get_image(url):
    import requests
    r = requests.request("GET", url)
    m = re.search(r'img src="(.*?)".*historyimage', r.text)
    return "http://www.opc.org{}".format(m.group(1))


def update_twitter(title, url):
    image_url = get_image(url)
    with open("twitter.json", "r") as f:
        credentials = json.load(f)
    t = tw.Api(**credentials)
    try:
        status = "{} {}".format(title, url)
        t.PostMedia(status, image_url)
        return "Tweeted {}".format(status)
    except Exception as e:
        return e.message[0]['message']


def update(event=None, context=None):
    title, url = get_today()
    fb_log = update_facebook(title, url)
    twitter_log = update_twitter(title, url)
    return "; ".join([fb_log, twitter_log])


if __name__ == '__main__':
    print update()
