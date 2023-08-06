import time
import colorlog
import logging


class Logger:
    def __init__(self, name: str, debug: bool = False, logfile: str = None, logAllFile: str = None):
        """Logger(
        name : The main name of the logger and by default is the filename of the logfile
        subname : A subname of the logger to individualize logs
        debug : Whether you want to have debugging on
        logfile : Optional name for the logfile, by default it is loggerName.log
        ).getLogger()"""
        filename = None
        self.name = name
        if logfile is not None:
            filename = logfile
        else:
            filename = f"logs/{name}.log"
        self.format = f'%(levelname)s [%(asctime)s] %(message)s'
        # logging.basicConfig(filename=f"logs/logs.log", encoding="utf-8", datefmt='%m/%d/%Y %H:%m:%S', format=self.format)
        self.handler = colorlog.StreamHandler()
        self.fileHandler = logging.FileHandler(filename=filename, encoding="utf-8")
        self.fileHandler.setFormatter(logging.Formatter(self.format, datefmt='%m/%d/%Y %H:%m:%S'))
        if logAllFile is not None:
            self.allFileHandler = logging.FileHandler(filename=logAllFile, encoding="utf-8")
            self.allFileHandler.setFormatter(
                logging.Formatter(f'%(levelname)s [%(asctime)s] ({name}) %(message)s',
                                  datefmt='%m/%d/%Y %H:%m:%S'))
        self.handler.setFormatter(
            colorlog.ColoredFormatter(f"%(log_color)s %(levelname)s [%(asctime)s] ({name}) %(message)s",
                                      datefmt='%m/%d/%Y %H:%m:%S'))
        self.debug = debug
        self.__logger : logging.Logger = logging.getLogger(name)
        self.__logger.addHandler(self.handler)
        self.__logger.addHandler(self.fileHandler)
        if logAllFile is not None:
            self.__logger.addHandler(self.allFileHandler)
        if debug:
            self.__logger.setLevel(colorlog.DEBUG)
        else:
            self.__logger.setLevel(colorlog.INFO)

    def getLogger(self):
        """Returns you the logger object"""
        return self.__logger

