import scrapy
from datetime import datetime, timezone

class StagesSpider(scrapy.Spider):
    name = "welcome_to_the_jungle"
    allowed_domains = ["welcometothejungle.com"]
    start_urls = [
        "https://www.welcometothejungle.com/fr/jobs?refinementList%5Boffices.country_code%5D%5B%5D=FR&query=stages&page=1"
    ]

    def parse(self, response):
        cards = response.css("li[data-testid='search-results-list-item-wrapper']")  # chaque offre est dans une balise article
        print(f"📌 {len(cards)} offres trouvées sur cette page.")

        for card in cards:
            link = card.css("a.sc-ipqUab doMQLj::attr(href)").get()
            if link :
                link = response.urljoin(link)

                print(f"➡️ Lien trouvé: {link}")
                # suivre le lien pour scraper la page de détails
                yield scrapy.Request(url=link, callback=self.parse_details)

    def parse_details(self, response):
    
        # Extraire la date depuis le datetime
        date_str = response.css('i[name="date"] + p time::attr(datetime)').get()
        if date_str:
            # Convertir la string ISO en objet datetime
            post_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

            # Calculer la différence avec la date actuelle
            now = datetime.now(timezone.utc)
            days_since_posted = (now - post_date).days
        else:
            days_since_posted = None
        full_text = " ".join(response.css("div[data-testid='job-section-description'] *::text").getall()).strip()
        yield {
            "date_pub":days_since_posted,
            "url": response.url,
            "raw_text": full_text
        }
