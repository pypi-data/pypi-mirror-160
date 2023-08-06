from multiprocessing import Process, Queue

from scrapy.crawler import CrawlerRunner
from scrapy.spiders import Spider
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from themispy.project.utils import PROJECT_PATH, PROJECT_TITLE, build_path


# Default Scrapy Settings
DEFAULT_SETTINGS = {
    'ROBOTSTXT_OBEY': False,
    'DEFAULT_REQUEST_HEADERS': {'Accept-Language': 'pt-BR'},
    'ITEM_PIPELINES': {'scraping.scraping.pipelines.FileDownloaderPipeline': 1},
    'FILES_STORE': build_path('temp/')
}


def run_spider(spider: Spider, filename: str = '', settings: dict = None,
               override: bool = False, crawler: bool = False,
               format: str = 'jsonlines', encoding: str = 'utf8',
               overwrite: bool = True) -> None:
    """Process for running spiders."""
    
    # Configure Scrapy Project Settings
    scrapy_settings = get_project_settings()
    scrapy_settings.update(DEFAULT_SETTINGS)
    
    if filename != '':
        scrapy_settings.update({
            'FEEDS': {
                f"{PROJECT_PATH}/temp/{PROJECT_TITLE}_{filename}": {
                    'format': format,
                    'encoding': encoding,
                    'overwrite': overwrite
                }
            }
        })
        
    scrapy_settings.update(settings)
    
    if crawler:
        scrapy_settings.update({
            'FEEDS': {
                f"{PROJECT_PATH}/temp/{PROJECT_TITLE}_crawler.jsonl": {
                    'format': 'jsonlines',
                    'encoding': 'utf8',
                    'overwrite': False
                }
            }
        })
        
    if override and settings is not None:
        scrapy_settings = get_project_settings()
        scrapy_settings.update(settings)
    
    
    def multiprocess(queue: Queue) -> None:
        """Setup incoming spider running call for multiprocessing."""
        try:
            configure_logging(settings=scrapy_settings)
            runner = CrawlerRunner(settings=scrapy_settings)
            deferred = runner.crawl(spider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            queue.put(None)
        except Exception as e:
            queue.put(e)

    queue_ = Queue()
    process = Process(target=multiprocess, args=(queue_,))
    process.start()
    result = queue_.get()
    process.join()

    if result is not None:
        raise result
