import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
import os.path
import os

from dotenv import load_dotenv

load_dotenv()


def main(url):
    print("Running...")
    if not os.path.exists(os.path.join(os.getcwd(), "id.txt")):
        new_file = open("id.txt", "w")
        new_file.close()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    }
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html5lib")
    # print(soup.prettify())
    all_content_container = soup.find('div', attrs={'id': 'jupiterx-primary'})
    all_content = all_content_container.find(
        'div', attrs={'class': 'jupiterx-content'})
    contents = all_content.findAll('article', attrs={'class': 'jupiterx-post'})
    f_present = open("id.txt", "r")
    if contents[0]['id'] == f_present.read():
        f = open("id.txt", "w")
        f.write(contents[0]['id'])
        f.close()
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()

        SUBJECT = "DPS Notices Updated: " + contents[0].find(
            'header').find('h2').find('a')['title']
        TEXT = "DPS Notices Updated\n" + contents[0].find('header').find('h2').find('a')['href'] + "\n" + contents[0].find(
            'header').find('h2').find('a')['title'] + "\n\nhttps://dpsrkp.net/category/notices"
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

        # Authentication
        s.login(os.environ.get("EMAIL"), os.environ.get("PASSWORD"))
        to = ["r21350kavin@dpsrkp.net", "r21389aniket@dpsrkp.net", "r21321aditi@dpsrkp.net",
              "e10459manya@dpsrkp.net", "v07834maisha@dpsrkp.net", "v07726aarav@dpsrkp.net"]
        for person in to:
            s.sendmail("kavinvalli@gmail.com",
                       person, message)
        s.quit()


# while True:
main("https://dpsrkp.net/category/notices")
