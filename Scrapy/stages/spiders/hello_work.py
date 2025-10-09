
import scrapy

class StagesSpider(scrapy.Spider):
    name = "hello_work"
    allowed_domains = ["hellowork.com"]
    start_urls = [
        "https://www.hellowork.com/fr-fr/emploi/recherche.html?k=&k_autocomplete=&l=&l_autocomplete=&st=relevance&c=Stage&cod=all&d=all"
    ]

    def parse(self, response):
        cards = response.css("div.tw-h-full.tw-relative.tw-flex.tw-flex-col")  # chaque offre est dans une balise article
        print(f"📌 {len(cards)} offres trouvées sur cette page.")

        for card in cards:
            link = card.css("a[data-cy='offerTitle']::attr(href)").get()
            if link :
                link = response.urljoin(link)

                print(f"➡️ Lien trouvé: {link}")
                # suivre le lien pour scraper la page de détails
                yield scrapy.Request(url=link, callback=self.parse_details)

    def parse_details(self, response):
        # Extract publication date
        date = response.css('p.tw-block.lg\\:tw-hidden::text').get()
        if date:
            date = date.strip()
        else:
            date = None
        full_text = " ".join(response.css("div.tw-flex.tw-flex-col *::text").getall()).strip()
        yield {
            "date_pub":date,
            "url": response.url,
            "raw_text": full_text
        }
