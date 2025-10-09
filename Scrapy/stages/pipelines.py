# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class StagePipeline:
    def process_item(self, item, spider):
        return item

# pipelines.py
import json

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('/Users/mac/Documents/Projects/internship_analysis/data/raw/stages.json', 'w', encoding='utf-8')
        self.file.write("[\n")  # start JSON array
        self.first_item = True

    def close_spider(self, spider):
        self.file.write("\n]")
        self.file.close()

    def process_item(self, item, spider):
        if not self.first_item:
            self.file.write(",\n")
        self.first_item = False
        json.dump(item, self.file, ensure_ascii=False, indent=4)
        return item

# import psycopg2

# class NeonPipeline:
#     def open_spider(self, spider):
#         self.conn = psycopg2.connect(
#             host="ep-old-mountain-adsihkzq-pooler.c-2.us-east-1.aws.neon.tech",
#             dbname="jobs",
#             user="neon_db",
#             password="npg_Bd6AGq8uisfX",
#             sslmode="require"
#         )
#         self.cur = self.conn.cursor()

#     def process_item(self, item, spider):
#         self.cur.execute("""
#             INSERT INTO internships (title, company, location, link)
#             VALUES (%s, %s, %s, %s)
#         """, (item['title'], item['company'], item['location'], item['link']))
#         self.conn.commit()
#         return item

#     def close_spider(self, spider):
#         self.cur.close()
#         self.conn.close()
