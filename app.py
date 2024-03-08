
from pathlib import Path
import requests
from datetime import datetime
from bs4 import BeautifulSoup

def fxstreet_news_download(url):
        page = requests.get(url)

        soup = BeautifulSoup(page.content, "html.parser")
        section = soup.find('section')
        headline = section.find('h1').text
        time = datetime.strptime(section.find('time').text, "%m/%d/%Y %H:%M:%S %Z")
        url = section['fxs_it_url']

        directory = f".news/{time.year}/{time.isocalendar().week}"
        directory_path = Path(directory)
        directory_path.mkdir(parents=True, exist_ok=True)

        path = f"{directory}/{url}.md"
        print(f"Path: {path}")
        with open(path, "w+") as f:
                f.write(f"# {headline}\n")
                f.write(f"\nURL: {url}\n")
                f.write(f"Time: {time}\n")

                content = soup.find(id="fxs_article_content")
                for c in content.children:
                        if c.name is None:
                                continue
                        if c.name != 'h2' and c.get('class') is not None:
                                continue
                        if c.name == 'ul':
                                f.write("\n")
                                lis = c.find_all('li')
                                for li in lis:
                                        f.write(f"* {li.text.rstrip().lstrip()}\n")
                        text = c.text.rstrip().lstrip()

                        if len(text) > 0 and c.name == 'h2':
                                f.write(f"\n## {text}\n")
                        if len(text) > 0 and (c.name == 'p' or c.name == 'blockquote'):
                                f.write(f"\n{text}\n")

if __name__ == "__main__":
        # fxstreet_news_download("https://www.fxstreet.com/analysis/fed-chair-will-be-speaking-again-might-he-give-better-guidance-202403071311")
        # fxstreet_news_download("https://www.fxstreet.com/news/lagarde-speech-we-will-not-wait-until-we-are-at-2-to-make-a-decision-202403071336")
        # fxstreet_news_download("https://www.fxstreet.com/news/european-central-bank-decision-preview-interest-rates-expected-to-remain-unchanged-as-inflation-weakens-202403070800")
        # fxstreet_news_download("https://www.fxstreet.com/news/usd-cad-to-stay-rangebound-in-the-short-term-before-a-usd-decline-emerges-ing-202403071434?utm_source=telegram&utm_medium=channel&utm_campaign=-1001510625232")
        # fxstreet_news_download("https://www.fxstreet.com/analysis/us-trade-deficit-widens-sharply-at-start-of-the-year-202403071444?utm_source=telegram&utm_medium=channel&utm_campaign=-1001510625232")
        # fxstreet_news_download("https://www.fxstreet.com/news/gold-price-forecast-xau-usd-to-suffer-a-correction-in-the-coming-days-and-weeks-commerzbank-202403081218?utm_source=telegram&utm_medium=channel&utm_campaign=-1001510625232")
        fxstreet_news_download("https://www.fxstreet.com/analysis/key-events-in-developed-markets-next-week-202403081258")
        