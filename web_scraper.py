from dataclasses import dataclass, asdict
import requests
from bs4 import BeautifulSoup
import re
import json
import time
from urllib.parse import urlparse
import os

@dataclass
class ArticleData:
    url: str
    post_id: str
    title: str
    keywords: list
    thumbnail: str
    video_duration: str
    word_count: int
    lang: str
    published_time: str
    last_updated: str
    description: str
    author: str
    classes: list
    full_text: str

class SitemapParser:
    def __init__(self, index_url):
        self.index_url = index_url

    def get_monthly_sitemaps(self):
        response = requests.get(self.index_url, timeout=20)
        soup = BeautifulSoup(response.content, 'lxml')
        sitemap_urls = [loc.text for loc in soup.find_all('loc')]
        return sitemap_urls

    def get_article_urls(self, sitemap_url):
        response = requests.get(sitemap_url, timeout=20)
        soup = BeautifulSoup(response.content, 'lxml')
        article_urls = [loc.text for loc in soup.find_all('loc')]
        return article_urls

class ArticleScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        })

    def scrape_article(self, url: str, retries=3, backoff_factor=1) -> ArticleData:
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=20)
                response.raise_for_status()
                break
            except requests.exceptions.HTTPError as http_err:
                if response.status_code == 404:
                    print(f"404 Error: The URL {url} was not found. Skipping...")
                    return None
                else:
                    print(f"HTTP error occurred: {http_err}")
                    return None
            except (requests.ConnectionError, requests.Timeout) as e:
                wait_time = backoff_factor * (2 ** attempt)
                print(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue
        else:
            print(f"Failed to fetch the article after {retries} attempts.")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        tawsiyat_metadata_script = soup.find('script', type='text/tawsiyat')
        if not tawsiyat_metadata_script:
            print("No text/tawsiyat script found")
            return None

        tawsiyat_data = json.loads(tawsiyat_metadata_script.string)

        article_body_tags = soup.find_all('p')
        full_text = ''.join([tag.get_text(strip=True) for tag in article_body_tags])

        article = ArticleData(
            url=tawsiyat_data.get('url'),
            post_id=tawsiyat_data.get('postid'),
            title=tawsiyat_data.get('title'),
            keywords=tawsiyat_data.get('keywords').split(',') if tawsiyat_data.get('keywords') else [],
            thumbnail=tawsiyat_data.get('thumbnail'),
            video_duration=tawsiyat_data.get('video_duration'),
            word_count=int(tawsiyat_data.get('word_count')) if tawsiyat_data.get('word_count') else 0,
            lang=tawsiyat_data.get('lang'),
            published_time=tawsiyat_data.get('published_time'),
            last_updated=tawsiyat_data.get('last_updated'),
            description=tawsiyat_data.get('description'),
            author=tawsiyat_data.get('author'),
            classes=tawsiyat_data.get('classes'),
            full_text=full_text
        )
        return article

class FileUtility:
    @staticmethod
    def save_to_json(data, year, month):
        month = month.zfill(2)
        filename = f'articles_{year}_{month}.json'
        file_path = os.path.join(os.getcwd(), filename)
        print(f"Attempting to save file: {file_path}")

        try:
            json_data = [asdict(article) for article in data]
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(json_data, file, ensure_ascii=False, indent=4)
            print(f"File saved successfully: {file_path}")
        except Exception as e:
            print(f"Error saving file: {e}")

def extract_year_month_from_url(sitemap_url):
    match = re.search(r'sitemap-(\d{4})-(\d{1,2})\.xml', sitemap_url)
    if match:
        year = match.group(1)
        month = match.group(2).zfill(2)
        print(f"Extracted year: {year}, month: {month}")
        return year, month
    else:
        print(f"Could not extract year and month from URL: {sitemap_url}")
        return 'unknown_year', 'unknown_month'

def main():
    sitemap_parser = SitemapParser('https://www.almayadeen.net/sitemaps/all.xml')
    monthly_sitemaps = sitemap_parser.get_monthly_sitemaps()

    article_count = 0
    max_articles = 10000

    for sitemap_url in monthly_sitemaps:
        if article_count >= max_articles:
            break

        article_urls = sitemap_parser.get_article_urls(sitemap_url)
        articles = []

        for url in article_urls:
            if article_count >= max_articles:
                break

            scraper = ArticleScraper()
            article_data = scraper.scrape_article(url)
            if article_data:
                articles.append(article_data)
                article_count += 1

        year, month = extract_year_month_from_url(sitemap_url)

        if articles:
            print(f"Saving {len(articles)} articles for {year}-{month}")
            FileUtility.save_to_json(articles, year=year, month=month)
        else:
            print(f"No articles found for {sitemap_url}. Skipping file creation.")

if __name__ == "__main__":
    main()
