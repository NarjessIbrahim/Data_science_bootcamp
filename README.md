# Al Mayadeen Web Scraper

This project is a web scraping tool designed to extract article metadata and content from the Al Mayadeen website. The scraper parses the website's sitemap, retrieves article URLs, and saves the extracted data into JSON files organized by year and month.

## Table of Contents

- [About the Project](#about-the-project)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## About the Project

The goal of this project is to familiarize users with web scraping using Python. It scrapes articles from the Al Mayadeen website, gathering relevant metadata such as URLs, titles, keywords, authors, and full article text, and saves this information into structured JSON files.

### Features

- Parse and extract monthly sitemaps from the Al Mayadeen website.
- Scrape individual articles for metadata and full text.
- Save scraped data into JSON files, organized by year and month.
- Handles up to 10,000 articles.

## Technology Stack

- **Python**: Programming language used for scripting.
- **Requests**: For making HTTP requests to the website.
- **BeautifulSoup**: For parsing HTML content.
- **lxml**: XML parser.
- **JSON**: For storing and organizing scraped data.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following:

- Python installed on your machine. You can download it from [Python's official website](https://www.python.org/downloads/).
- Basic understanding of Python programming.
- Willingness to explore web scraping techniques.

### Installation

Install the required libraries:
pip install requests beautifulsoup4 lxml


Usage
1. Run the scraper:

The main script to execute is web_scraper.py.
The script will automatically start parsing the sitemap and scraping articles.
python web_scraper.py

2. Check the output:

The JSON files will be saved in the same directory as the script, named according to the year and month (e.g., articles_2024_08.json).


File Structure
web_scraper.py: Main script containing the logic for sitemap parsing, article scraping, and file saving.
ArticleData: Dataclass to define the structure for storing article metadata and content.
SitemapParser: Class to handle the parsing of the sitemap index and extraction of URLs.
ArticleScraper: Class to handle the scraping of individual articles.
FileUtility: Utility class to handle saving the extracted data to JSON files.
Contributing
Contributions are welcome! Please fork the repository and use a feature branch. Pull requests are warmly welcome.

Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request
License
This project is licensed under the MIT License - see the LICENSE file for details.



Contact
Narjess Ibrahim  - ibrahimnarjess@gmail.com

Project Link: https://github.com/NarjessIbrahim/Data_science_bootcamp

