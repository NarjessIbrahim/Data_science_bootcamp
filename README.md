Al Mayadeen Data Scraping, Storage, and Analysis
This project involves scraping articles from Al Mayadeen, storing them in MongoDB, creating APIs to access and analyze the data, and visualizing trends using amCharts.

Table of Contents
About the Project
Technology Stack
Getting Started
Prerequisites
Installation
Usage
Scraping Data (Task 1)
Storing Data (Task 2)
API Development (Task 2)
Data Visualization (Task 3)
Advanced Data Analysis (Task 4)
File Structure
Contributing
License
Contact
About the Project
This project focuses on data collection, storage, and visualization for articles from Al Mayadeen. It involves scraping article metadata and content, storing it in MongoDB, creating APIs to query the data, and providing visualizations using amCharts.

Features
Scrapes articles and stores them in JSON files.
Stores collected data in MongoDB.
Provides Flask APIs for querying and aggregating data.
Creates various interactive charts using amCharts.
Technology Stack
Python: For web scraping and API development.
Flask: To create APIs.
MongoDB: For data storage.
amCharts: For visualizing data.
TextBlob and Stanza: For text analysis.
Getting Started
Prerequisites
Before you begin, ensure you have the following:

Python installed on your machine.
MongoDB installed locally.
Basic knowledge of Python, Flask, and web scraping techniques.
Installation
Install the required libraries:
pip install requests beautifulsoup4 lxml pymongo flask amcharts-python
Set up MongoDB and ensure it's running.
Usage
Scraping Data (Task 1)
To scrape articles and save them as JSON files:

Copy code
python web_scraper.py
JSON files will be saved.

Storing Data (Task 2)
To store the scraped data in MongoDB:

Copy code
python data_storage.py
Data will be stored in the articles collection in MongoDB.

API Development (Task 2)
To start the Flask server and access the API:

Copy code
python app.py
Access the endpoints via http://127.0.0.1:5000/.

API Endpoints:
/top_keywords: Get top 10 keywords.
/top_authors: Get top 10 authors.
/articles_by_date: Get article counts by date.
/articles_by_word_count: Get article counts by word count.
etc..

Data Visualization (Task 3)
To visualize the data, start the Flask server and open the dashboard.html file in the browser. It will display interactive charts for various metrics such as top keywords, articles by date, and more.

Advanced Data Analysis (Task 4)
In this task, sentiment analysis and entity recognition are performed using TextBlob/Stanza. To run sentiment analysis and extract entities:


New endpoints include:

 /articles_by_sentiment/<sentiment_type>: /articles_by_sentiment/positive Get articles with positive sentiment.
/articles_by_entity/<entity>: Get articles mentioning .
/sentiment_trends: Visualize sentiment trends over time.
/keyword_trends/<keyword>: Visualize keyword trends over time

File Structure

project-directory/
│
├── charts/              # Contains individual chart HTML files
│   ├── chart1.html      # Top Keywords
│   ├── chart2.html      # Top Authors
│   ├── ...              # Other charts
│
├── dashboard.html       # Main dashboard file
├── web_scraper.py       # Script for scraping articles
├── data_storage.py      # Script for storing data in MongoDB
├── app.py               # Flask API for querying data
├── sentiment.py         # sentiment analysis and trend visualization
├── entity recognition.py# entity recognition and visualization
├── README.md            # This file
Screenshots

![Articles by Keyword](images/articles by keyword.png)

![longest articles](https://github.com/user-attachments/assets/99051e74-2ebb-4267-82db-560d42b65335)


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
Narjess Ibrahim - ibrahimnarjess@gmail.com

Project Link: https://github.com/NarjessIbrahim/Data_science_bootcamp


