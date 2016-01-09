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


def update_twitter(title, url):
    with open("twitter.json", "r") as f:
        credentials = json.load(f)
    t = tw.Api(**credentials)
    try:
        status = "{} {}".format(title, url)
        t.PostUpdate(status=status)
        return "Tweeted {}".format(status)
    except Exception as e:
        return e.message


def update(event=None, context=None):
    title, url = get_today()
    fb_log = update_facebook(title, url)
    twitter_log = update_twitter(title, url)

    return "; ".join([fb_log, twitter_log[0]['message']])


if __name__ == '__main__':
    print update()
