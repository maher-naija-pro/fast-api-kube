import logging

class AppFilter(logging.Filter):
    def filter(self, record):
      #  set custom record attribute values   
      #  record.app_name = 'Super App'
      # filter message 
       return record.getMessage().startswith('')

def init_log(logger_name="root",extra=None):
  logging.basicConfig(level=logging.DEBUG,  format='[%(asctime)s] %(name)s %(levelname)s  [%(funcName)s:%(lineno)s] %(message)s')
  logger = logging.getLogger(logger_name)
  adapter=logging.LoggerAdapter(logger, extra)
  logger.addFilter(AppFilter())
  return logger

