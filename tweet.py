import re
import datetime as dt
import twitter as tw
import os
import requests


def update_facebook(title, url):
    import facebook
    api = facebook.GraphAPI(os.environ["FACEBOOK_SECRET"].strip())

    try:
        api.put_object(
            parent_object="me",
            connection_name="feed",
            message=f"Today in OPC History: {title}",
            link=url
        )
        return "Successfully posted to Facebook"
    except facebook.GraphAPIError as e:
        return "Error", e

    
def get_today():
    r = requests.request("GET", "http://opc.org/today.html", verify=False)
    previous = re.findall(r'<a class="navButton" href="(.*?)">Previous</a>', r.text)
    title = re.findall(r'<h2>(.*)</h2>', r.text)[0]
    r = requests.request("GET", f"http://opc.org{previous[0]}", verify=False)
    link = "http://opc.org/" + re.findall(r'<a class="navButton" href="(.*?)">Next</a>', r.text)[0]
    return title, link

    
def get_image(url):
    import requests
    r = requests.request("GET", url, verify=False)
    m = re.search(r'img src="(.*?)".*historyimage', r.text)
    return "http://www.opc.org{}".format(m.group(1))


def update_twitter(title, url):
    cred = {
        "consumer_key": os.environ["CONSUMER_KEY"].strip(),
        "consumer_secret": os.environ["CONSUMER_SECRET"].strip(),
        "token": os.environ["TOKEN"].strip(),
        "token_secret": os.environ["TOKEN_SECRET"].strip(),
    }
    auth = tw.OAuth(**cred)
    t = tw.Twitter(auth=auth)

    status = f"{title} {url} #OPChistory"
    t.statuses.update(status=status)


def update(event=None, context=None):
    title, url = get_today()
    fb_log = update_facebook(title, url)
    twitter_log = update_twitter(title, url)
    return "{}; {}".format(fb_log, twitter_log)


if __name__ == '__main__':
    print(update())
