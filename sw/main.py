# coding: utf-8

import yaml
import time
import schedule
import asyncio
from argparse import ArgumentParser
from crawler import Crawler
from functools import partial


def crawler_run(crawler):
    asyncio.run(crawler.run())


def parse_args():
    parser = ArgumentParser('Benny爬蟲')
    parser.add_argument('--config', '-c', default='config.yml', help='設定擋路徑')
    parser.add_argument('--sample', '-s', default='test', help='test')
    return parser.parse_args()


def main():
    args = parse_args()
    with open(args.config, 'r', encoding='utf-8') as config_file:
        config = yaml.safe_load(config_file)
    config.update({
        'sample': args.sample,
    })
    crawler = Crawler(config)
    crawler.setup()

    # 初始执行一次
    crawler_run(crawler)
    crawler_with_args = partial(crawler_run, crawler)
    schedule.every().day.at("01:00").do(crawler_with_args)
    schedule.every().day.at("05:00").do(crawler_with_args)
    schedule.every().day.at("09:00").do(crawler_with_args)
    schedule.every().day.at("13:00").do(crawler_with_args)
    schedule.every().day.at("17:00").do(crawler_with_args)
    schedule.every().day.at("21:00").do(crawler_with_args)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(f"An error main : {e}")
        time.sleep(1)
