# Crypto News Scraper

A comprehensive web scraping project built with Scrapy that automatically collects cryptocurrency news articles from multiple sources and stores them in a PostgreSQL database.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Data Sources](#data-sources)
- [Database Schema](#database-schema)
- [Output Files](#output-files)
- [Technical Details](#technical-details)

## 🎯 Overview

This project is a Scrapy-based web scraper designed to collect cryptocurrency news articles from 30+ major crypto news websites. The scraper extracts article titles, content, publication dates, and URLs, then stores this data in a PostgreSQL database for further analysis or consumption.

## ✨ Features

- **Multi-source scraping**: Collects news from 30+ cryptocurrency news websites
- **Intelligent date parsing**: Handles various date formats and normalizes them to ISO format
- **Content extraction**: Extracts article titles and full content from news pages
- **Database storage**: Automatically stores scraped data in PostgreSQL database
- **Duplicate prevention**: Uses URL-based conflict resolution to avoid duplicate entries
- **Robust error handling**: Graceful handling of parsing errors and database issues
- **Respectful crawling**: Follows robots.txt rules and implements proper delays

## 📁 Project Structure

```
crypto_news/
├── crypto_news/                 # Main Scrapy project directory
│   ├── __init__.py
│   ├── items.py                 # Data models for scraped items
│   ├── middlewares.py           # Spider and downloader middlewares
│   ├── pipelines.py             # Data processing pipelines
│   ├── settings.py              # Scrapy configuration settings
│   └── spiders/                 # Spider implementations
│       ├── __init__.py
│       └── crypto_spider.py     # Main spider for crypto news
├── crypto_articles.json         # JSON output of scraped articles
├── crypto_news_rows.csv         # CSV export of scraped data
├── s.csv                        # Sample CSV data
└── scrapy.cfg                   # Scrapy deployment configuration
```

## 🚀 Installation

### Prerequisites

- Python 3.7+
- PostgreSQL database
- pip (Python package manager)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ujjwalredd/Crypto-News-Scraper.git
   cd crypto_news
   ```

2. **Install dependencies**:
   ```bash
   pip install scrapy psycopg2-binary python-dateutil
   ```

3. **Set up PostgreSQL database**:
   ```sql
   CREATE TABLE crypto_news (
       id SERIAL PRIMARY KEY,
       url VARCHAR(500) UNIQUE NOT NULL,
       title TEXT,
       date TIMESTAMP,
       content TEXT,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

## ⚙️ Configuration

### Database Configuration

The database connection is configured in `crypto_news/pipelines.py`. Update the following parameters:

```python
self.connection = psycopg2.connect(
    host='your-database-host',
    user='your-username',
    password='your-password',
    dbname='your-database-name'
)
```

### Scrapy Settings

Key settings in `crypto_news/settings.py`:

- `ROBOTSTXT_OBEY = True` - Respects robots.txt rules
- `ITEM_PIPELINES` - Configured to use PostgreSQL pipeline
- `REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"` - Modern request fingerprinting
- `TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"` - Async reactor

## 🎮 Usage

### Running the Spider

1. **Basic run**:
   ```bash
   scrapy crawl crypto_news
   ```

2. **Save output to JSON**:
   ```bash
   scrapy crawl crypto_news -o crypto_articles.json
   ```

3. **Save output to CSV**:
   ```bash
   scrapy crawl crypto_news -o crypto_news_rows.csv
   ```

4. **Run with custom settings**:
   ```bash
   scrapy crawl crypto_news -s DOWNLOAD_DELAY=2
   ```

### Monitoring and Logging

The spider provides detailed logging information:
- Request/response statistics
- Database insertion status
- Error handling and recovery
- Crawl progress and timing

## 📰 Data Sources

The spider targets 30+ cryptocurrency news websites:

### Major Sources
- **CoinDesk** (coindesk.com)
- **Cointelegraph** (cointelegraph.com)
- **Decrypt** (decrypt.co)
- **Bitcoin.com News** (news.bitcoin.com)
- **BeInCrypto** (beincrypto.com)
- **The Block** (theblock.co)
- **CryptoNews** (cryptonews.com)
- **CryptoSlate** (cryptoslate.com)
- **CryptoBriefing** (cryptobriefing.com)
- **CryptoPotato** (cryptopotato.com)

### Additional Sources
- **U.Today** (u.today)
- **CryptoNews.net** (cryptonews.net)
- **Coinpedia** (coinpedia.org)
- **DailyCoin** (dailycoin.com)
- **AMB Crypto** (ambcrypto.com)
- **Blockworks** (blockworks.co)
- **Bitcoin Magazine** (bitcoinmagazine.com)
- **The Defiant** (thedefiant.io)
- **CryptoPanic** (cryptopanic.com)
- **CoinGape** (coingape.com)
- **The Crypto Basic** (thecryptobasic.com)
- **CoinCodex** (coincodex.com)
- **Messari** (messari.io)
- **CryptoFlies** (cryptoflies.com)
- **NFT Evening** (nftevening.com)
- **Unchained Crypto** (unchainedcrypto.com)
- **Global Crypto Press** (globalcryptopress.com)
- **DataWallet** (datawallet.com)
- **Holder.io** (holder.io)

## 🗄️ Database Schema

The scraped data is stored in a PostgreSQL table with the following structure:

```sql
CREATE TABLE crypto_news (
    id SERIAL PRIMARY KEY,
    url VARCHAR(500) UNIQUE NOT NULL,
    title TEXT,
    date TIMESTAMP,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Data Fields

- **url**: Article URL (unique identifier)
- **title**: Article headline
- **date**: Publication date (normalized to ISO format)
- **content**: Full article text content
- **created_at**: Timestamp when record was inserted

## 📊 Output Files

### JSON Output (`crypto_articles.json`)
Contains all scraped articles in JSON format:
```json
[
  {
    "url": "https://example.com/article",
    "title": "Article Title",
    "date": "2023-01-01T12:00:00",
    "content": "Article content..."
  }
]
```

### CSV Output (`crypto_news_rows.csv`)
Contains scraped data in CSV format with headers:
```csv
id,url,title,date,content
1,https://example.com/article,Article Title,2023-01-01 12:00:00,"Article content..."
```

## 🔧 Technical Details

### Spider Implementation

The main spider (`CryptoNewsSpider`) uses Scrapy's `CrawlSpider` with the following features:

- **Link Extraction**: Uses `LinkExtractor` to find article links
- **Date Parsing**: Multiple fallback methods for date extraction:
  - `time::attr(datetime)`
  - `meta[property="article:published_time"]`
  - `meta[name="pubdate"]`
  - `meta[name="date"]`
- **Content Extraction**: Extracts article paragraphs using CSS selectors
- **Data Validation**: Only yields items with both title and content

### Pipeline Processing

The `PostgresPipeline` handles:
- Database connection management
- Data insertion with conflict resolution
- Error handling and rollback
- Connection cleanup

### Middleware

Standard Scrapy middleware implementation for:
- Request/response processing
- Exception handling
- Spider lifecycle management

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This scraper is for educational and research purposes. Please ensure you comply with:
- Website terms of service
- Robots.txt directives
- Rate limiting requirements
- Data usage policies

Always respect the websites you're scraping and implement appropriate delays between requests. 