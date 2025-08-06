import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import dateutil.parser

class CryptoNewsSpider(CrawlSpider):
    name = 'crypto_news'
    allowed_domains = [
        'coindesk.com',
        'cointelegraph.com',
        'decrypt.co',
        'bitcoin.com',
        'beincrypto.com',
        'theblock.co',
        'cryptonews.com',
        'u.today',
        'cryptoslate.com',
        'cryptobriefing.com',
        'cryptopotato.com',
        'cryptonews.net',
        'coinpedia.org',
        'dailycoin.com',
        'ambcrypto.com',
        'blockworks.co',
        'bitcoinmagazine.com',
        'thedefiant.io',
        'cryptopanic.com',
        'coingape.com',
        'thecryptobasic.com',
        'coincodex.com',
        'messari.io',
        'cryptoflies.com',
        'nftevening.com',
        'unchainedcrypto.com',
        'globalcryptopress.com',
        'datawallet.com',
        'holder.io'
    ]

    start_urls = [
        'https://www.coindesk.com/',
        'https://cointelegraph.com/',
        'https://decrypt.co/',
        'https://news.bitcoin.com/',
        'https://beincrypto.com/',
        'https://www.theblock.co/',
        'https://cryptonews.com/',
        'https://u.today/',
        'https://cryptoslate.com/',
        'https://cryptobriefing.com/',
        'https://cryptopotato.com/',
        'https://cryptonews.net/',
        'https://coinpedia.org/',
        'https://dailycoin.com/',
        'https://ambcrypto.com/',
        'https://blockworks.co/',
        'https://bitcoinmagazine.com/',
        'https://thedefiant.io/',
        'https://cryptopanic.com/',
        'https://coingape.com/',
        'https://thecryptobasic.com/',
        'https://coincodex.com/',
        'https://messari.io/',
        'https://cryptoflies.com/',
        'https://nftevening.com/',
        'https://unchainedcrypto.com/',
        'https://www.globalcryptopress.com/',
        'https://datawallet.com/',
        'https://holder.io/'
    ]


    rules = (
        Rule(LinkExtractor(allow=(), deny=()), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        title = response.css('h1::text').get()
        date = (
        response.css('time::attr(datetime)').get() or
        response.css('meta[property="article:published_time"]::attr(content)').get() or
        response.css('meta[name="pubdate"]::attr(content)').get() or
        response.css('meta[name="date"]::attr(content)').get()
    )

        # Normalize date if it's found
        if date:
            try:
                date = dateutil.parser.parse(date).isoformat()
            except Exception:
                pass
        paragraphs = response.css('article p::text').getall()
        content = ' '.join(paragraphs).strip()

        if title and content:
            yield {
                'url': response.url,
                'title': title,
                'date': date,
                'content': content
            }

