BOT_NAME = "stages"

SPIDER_MODULES = ["stages.spiders"]
NEWSPIDER_MODULE = "stages.spiders"

ADDONS = {}
ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 5

custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.csv': { 'format': 'csv',}}
        }


ITEM_PIPELINES = {
    'stages.pipelines.JsonWriterPipeline': 1,
}

FEED_EXPORT_ENCODING = 'utf-8'