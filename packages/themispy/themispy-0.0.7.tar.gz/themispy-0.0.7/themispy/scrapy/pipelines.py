from scrapy.pipelines.files import FilesPipeline

from themispy.project.utils import PROJECT_TITLE

    
class FileDownloaderPipeline(FilesPipeline):
    """
    Default filename after download:\n
    * {PROJECT_TITLE}_{docname}.{docext}
    """
    def file_path(self, request, response=None, info=None, *, item=None):
        return f"{PROJECT_TITLE}_{item.get('docname')}{item.get('docext')}"
