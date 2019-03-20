from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose

class LeopardItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    title_in = MapCompose(str.strip)
    date_in = MapCompose(str.strip)
    link_in = MapCompose(str.strip)