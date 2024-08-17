from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urlparse


@dataclass
class ArticleData:
    url: str
    post_id: str
    title: str
    keywords: list
    thumbnail: str
    publication_date: str
    last_updated_date: str
    author: str
    full_text: str


class SitemapParser:
    def __init__(self, index_url):
        self.index_url = index_url

    def get_monthly_sitemaps(self):
        response = requests.get(self.index_url)
        soup = BeautifulSoup(response.content, 'lxml')
        sitemap_urls = [loc.text for loc in soup.find_all('loc')]
        return sitemap_urls

    def get_article_urls(self, sitemap_url):
        response = requests.get(sitemap_url)
        soup = BeautifulSoup(response.content, 'lxml')
        article_urls = [loc.text for loc in soup.find_all('loc')]
        return article_urls


class ArticleScraper:
    def __init__(self, article_url):
        self.article_url = article_url

    def scrape_article(self):
        response = requests.get(self.article_url)
        soup = BeautifulSoup(response.content, 'lxml')

        # Extracting the fields
        type_content = 'article'  # Default to article unless specified elsewhere
        title = soup.find('meta', {'property': 'og:title'}) or soup.find('title')
        title = title['content'] if title else 'No title found'

        post_id = soup.find('meta', {'name': 'postid'})
        post_id = post_id['content'] if post_id else 'No ID found'

        keywords = soup.find('meta', {'name': 'keywords'})
        keywords = keywords['content'].split(',') if keywords else []

        thumbnail = soup.find('meta', {'property': 'og:image'})
        thumbnail = thumbnail['content'] if thumbnail else 'No thumbnail found'

        video_duration = soup.find('meta', {'property': 'video:duration'})
        video_duration = video_duration['content'] if video_duration else 'No video duration found'

        paragraphs = soup.find_all('p')
        full_text = '\n'.join([p.get_text() for p in paragraphs]) if paragraphs else 'No content found'
        word_count = len(full_text.split())

        lang = soup.find('html')['lang'] if soup.find('html') else 'No language found'

        published_time = soup.find('meta', {'property': 'article:published_time'})
        published_time = published_time['content'] if published_time else 'No published time found'

        last_updated = soup.find('meta', {'property': 'article:modified_time'})
        last_updated = last_updated['content'] if last_updated else 'No last updated time found'

        description = soup.find('meta', {'name': 'description'})
        description = description['content'] if description else 'No description found'

        author = soup.find('meta', {'name': 'author'})
        author = author['content'] if author else 'No author found'

        body_classes = soup.find('body')['class'] if soup.find('body') else 'No classes found'

        return {
            'type': type_content,
            'post_id': post_id,
            'title': title,
            'url': self.article_url,
            'keywords': keywords,
            'thumbnail': thumbnail,
            'video_duration': video_duration,
            'word_count': word_count,
            'lang': lang,
            'published_time': published_time,
            'last_updated': last_updated,
            'description': description,
            'author': author,
            'classes': body_classes,
        }


from urllib.parse import urlparse
import re
import os
import json

class FileUtility:
    @staticmethod
    def save_to_json(data, year, month):
        # Ensure month is two digits
        month = month.zfill(2)
        filename = f'articles_{year}_{month}.json'
        print(f"Attempting to save file: {filename}")  # Debugging statement
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print(f"File saved successfully: {filename}")  # Confirm success
        except Exception as e:
            print(f"Error saving file: {e}")  # Catch any errors

def extract_year_month_from_url(sitemap_url):
    # Assuming the sitemap URL contains the year and month in the format "sitemap-YYYY-MM.xml"
    match = re.search(r'sitemap-(\d{4})-(\d{1,2})\.xml', sitemap_url)
    if match:
        year = match.group(1)
        month = match.group(2).zfill(2)  # Ensure month is two digits
        print(f"Extracted year: {year}, month: {month}")  # Debugging statement
        return year, month
    else:
        print(f"Could not extract year and month from URL: {sitemap_url}")  # Debugging statement
        return 'unknown_year', 'unknown_month'

def main():
    sitemap_parser = SitemapParser('https://www.almayadeen.net/sitemaps/all.xml')
    monthly_sitemaps = sitemap_parser.get_monthly_sitemaps()

    article_count = 0  # Initialize the article counter
    max_articles = 2 # Set the maximum number of articles

    for sitemap_url in monthly_sitemaps:
        if article_count >= max_articles:
            break  # Stop if we've already processed the maximum number of articles

        article_urls = sitemap_parser.get_article_urls(sitemap_url)
        articles = []

        for url in article_urls:
            if article_count >= max_articles:
                break  # Stop if we've already processed the maximum number of articles

            scraper = ArticleScraper(url)
            article_data = scraper.scrape_article()
            articles.append(article_data)

            article_count += 1  # Increment the article counter

        # Extract year and month from sitemap_url
        year, month = extract_year_month_from_url(sitemap_url)

        if articles:
            print(f"Saving {len(articles)} articles for {year}-{month}")  # Debugging statement
            FileUtility.save_to_json(articles, year=year, month=month)
        else:
            print(f"No articles found for {sitemap_url}. Skipping file creation.")  # Inform no articles

if __name__ == "__main__":
    main()
