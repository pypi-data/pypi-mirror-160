# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FileDownloader(scrapy.Item):
    """
    Attributes are:
    * 'file_urls': stores the urls used for downloading files. Do not rename this.
    * 'docname': document name.
    * 'docext': document extension. (e.g.: .csv, .xml, .zip)
    """
    
    file_urls = scrapy.Field()
    docname = scrapy.Field()
    docext = scrapy.Field()
