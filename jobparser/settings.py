SPIDER_MODULES = ['jobparser.spiders']
NEWSPIDER_MODULE = 'jobparser.spiders'
USER_AGENT = 'Mozilla/5.0'
ROBOTSTXT_OBEY = False
LOG_ENABLED = False
LOG_LEVEL = 'DEBUG'  # INFO ERROR
# LOG_FILE = 'log.txt'
MONGO_URI = 'localhost'
MONGO_DATABASE = 'hhjp'  # Имя базы данных.
ITEM_PIPELINES = {'jobparser.pipeline.JobparserPipeline': 300}
