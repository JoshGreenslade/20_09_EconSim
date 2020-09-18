from econsim.Agent import logging_test
import logging

logging.basicConfig(filename='./log.log',
                    level=logging.DEBUG,
                    filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.debug('Hello!')

logging_test()
