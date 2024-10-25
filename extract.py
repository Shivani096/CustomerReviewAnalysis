import requests
from bs4 import BeautifulSoup
import pandas as pd

class Extract:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }

    def ReviewUrl(self, productUrl):
        reviewUrl = productUrl.replace("dp", "product-reviews") + "?pageNumber=" + str(1)
        return reviewUrl

    def total_reviews(self, reviewUrl):
        response = requests.get(reviewUrl, headers=self.HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        reviews = soup.findAll("div", {"data-hook": "review"})
        return reviews

    def extractReview(self, item):
            review = {
                "Title": item.find("a", {"data-hook": "review-title"}).text.strip(),
                "Rating": item.find("i", {"data-hook": "review-star-rating"})
                .text.strip()
                .split(" ")[0],
                "Body": item.find("span", {"data-hook": "review-body"}).text.strip(),
            }
            print(review)
            return review
    
    def exportToExcel(self, reviewList):
        df = pd.DataFrame(reviewList)
        df.to_excel("output.xlsx", index=False)