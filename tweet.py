import requests
import re
import datetime as dt
import twitter as tw
import json

r = requests.request("GET", "http://opc.org/today.html?target=archive")


def get_today():
    for date, path, title in re.findall(r'<p>([A-Za-z]+ [0-9]+)<br /><a href="(.*?)">(.*?)</a></p>', r.text):
        if date == dt.datetime.now().strftime("%B %-d"):
            return "{} http://www.opc.org{}".format(title, path)


def tweet(event, context):
    with open("twitter.json", "r") as f:
        credentials = json.load(f)
    t = tw.Api(**credentials)
    try:
        status = get_today()
        t.PostUpdate(status=status)
        return "Tweeted {}".format(status)
    except Exception as e:
        return e.message


if __name__ == '__main__':
    print tweet(None, None)
