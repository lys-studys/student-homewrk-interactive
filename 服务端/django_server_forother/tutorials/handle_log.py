import logging

from tutorials.config import LOG_FILE_PATH


class HandleLog:

    def __init__(self):
        LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d]: %(message)s'
        DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.ERROR)

        fh = logging.FileHandler(filename=LOG_FILE_PATH, mode='a', encoding='utf-8')  # 不拆分日志文件，a指追加模式,w为覆盖模式
        fh.setLevel(logging.ERROR)
        formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def error_log(self, msg):
        self.logger.error(msg)

    def exception_log(self, pre_msg, e):
        """
        记录异常信息
        :param pre_msg: 自定义信息
        :param e: 异常对象
        :return:
        """
        error_msg = '{}：{} | File {}, line {}'.format(
            pre_msg,
            repr(e),
            e.__traceback__.tb_frame.f_globals["__file__"],
            e.__traceback__.tb_lineno
        )
        self.logger.error(error_msg)
