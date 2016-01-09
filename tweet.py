import requests
import re
import datetime as dt
import twitter as tw
import json

r = requests.request("GET", "http://opc.org/today.html?target=archive")


def update_facebook(title, url):
    import facebook
    with open('facebook.txt', 'r') as f:
        access_token = f.read().strip()
    api = facebook.GraphAPI(access_token)

    try:
        api.put_wall_post("", attachment={"link": url, "name": title})
    except facebook.GraphAPIError as e:
        print "Error", e


def get_today():
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
    update_facebook(title, url)
    update_twitter(title, url)


if __name__ == '__main__':
    update()
