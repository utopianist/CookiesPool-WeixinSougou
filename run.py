from cookiespool.spider import Spider
from cookiespool.schedule import Scheduler

def main():
    s = Scheduler()
    s.run()

if __name__ == '__main__':
    main()