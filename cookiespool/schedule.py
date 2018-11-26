import time
from multiprocessing import Process
from cookiespool.config import *
from cookiespool.api import app
from cookiespool.spider import Spider


class Scheduler():
    def schedule_getter(self):
        """
        定时获取Cookie
        """
        spider = Spider()
        while True:
            spider.getHTML()
            time.sleep(SLEEPTIME)

    def schedule_api(self):
        """
        开启API
        """
        app.run(API_HOST, API_PORT)

    def run(self):
        print('Cookie池开始运行')

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()
