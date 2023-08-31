import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template
import urllib.parse

app = Flask(__name__)

def extract_notif(url):
    print("Extracting Notifications from KTU Site....")
    notifications = []

    response = requests.get(url)
    response_cnt = response.content
    soup = BeautifulSoup(response_cnt, 'html.parser')

    base_url = "https://ktu.edu.in"  # Base URL of the website

    notification_count = 0
    for tag in soup.find_all('li'):
        if notification_count >= 5:
            break
        b_tag = tag.find('b')

        if b_tag:
            notification_count += 1
            link_tag = tag.find('a', target='_blank')
            if link_tag:
                notification_link = urllib.parse.urljoin(base_url, link_tag['href'])
                notification_text = b_tag.get_text(strip=True)
                notifications.append((notification_count, notification_text, notification_link))
            else:
                notification_text = b_tag.get_text(strip=True)
                notifications.append((notification_count, notification_text, " "))

    return notifications

@app.route('/')
def index():
    url = "https://ktu.edu.in/eu/core/announcements.htm"
    notifications = extract_notif(url)
    return render_template('index.html', notifications=notifications)

if __name__ == '__main__':
    app.run(debug=True)
