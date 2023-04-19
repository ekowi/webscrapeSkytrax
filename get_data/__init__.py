from bs4 import BeautifulSoup
import requests

urls = "https://www.airlinequality.com/airline-reviews/british-airways"
review = requests.get(urls).content
soup = BeautifulSoup(review, 'html.parser')
tittles = soup.findAll('h2', {'class': 'text_header'})
# for tittle in tittles:
    # print(tittle.text)

details = soup.findAll('div', {'itemprop': 'reviewBody'})
for detail in details:
    comment = detail.text.split('|')
    detail = comment[1]
    print(detail)