"""
author: Zakkoree
"""
import os
import logging

class Logger():

    CmdLevel = logging.DEBUG
    FileLevel = logging.INFO
    FileName = "out.log"
    FilePath = os.path.dirname(os.path.abspath(__file__))
    
    def __init__(self, LoggerName):
        """
        
        """

        # LoggerName：实例化对象的名字  FileName:外部文件名   CmdLevel:设置控制台中日志输出的级别  FileLevel:设置文件日志输出的级别
        self.logger = logging.getLogger(LoggerName)
        
        # 判断条件，如果存在handlers则不创建，解决日志重复输出问题
        if not self.logger.handlers:
            # 设置日志的级别
            self.logger.setLevel(logging.DEBUG)
            # 设置日志的输出格式
            fmt = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
            # 借助handle将日志输出到文件中
            fh = logging.FileHandler(self.FilePath + "/" + self.FileName)
            fh.setLevel(self.FileLevel)

            # 借助handle将日志输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(self.CmdLevel)

            # 配置logger
            fh.setFormatter(fmt)
            ch.setFormatter(fmt)

            # 给logger添加handle
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)
    


    def debug(self,message):
        self.logger.debug(message)

    def info(self,message):
        self.logger.info(message)

    def warn(self,message):
        self.logger.warning(message)

    def error(self,message):
        self.logger.error(message)

    def critical(self,message):
        self.logger.critical(message)
