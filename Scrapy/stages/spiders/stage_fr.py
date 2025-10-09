import scrapy

class StagesSpider(scrapy.Spider):
    name = "stage_fr"
    allowed_domains = ["stage.fr"]
    start_urls = [
        "https://www.stage.fr/jobs/?q=stage"
    ]

    def parse(self, response):
        cards = response.css("article.listing-item__jobs")  # chaque offre est dans une balise article
        print(f"📌 {len(cards)} offres trouvées sur cette page.")

        for card in cards:
            link = card.css("a.btn-view-offers::attr(href)").get()
            if link :
                link = response.urljoin(link)

                print(f"➡️ Lien trouvé: {link}")
                # suivre le lien pour scraper la page de détails
                yield scrapy.Request(url=link, callback=self.parse_details)

    def parse_details(self, response):
        date = response.css("li.listing-item__info--item-date::text").get()
        if date:
            date = date.strip()
        else:
            date = None
        full_text = " ".join(response.css("div.details-body__left *::text").getall()).strip()
        yield {
            "date_pub":date,
            "url": response.url,
            "raw_text": full_text
        }
