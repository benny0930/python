# coding: utf-8
import yaml
import os
import schedule
import time
from crawler import Crawler
from argparse import ArgumentParser
from functools import partial


def parse_args():
    parser = ArgumentParser('Benny爬蟲')
    parser.add_argument('--config', '-c', default='config.yml', help='設定檔路徑')
    parser.add_argument('--test', '-t', default=False, action='store_true', help='測試模式')
    parser.add_argument('--type', '-tp', default="", help='類型')
    return parser.parse_args()


def check_and_create():
    os.makedirs("images", exist_ok=True)
    if not os.path.exists('config.yml'):
        with open('config.yml', 'w') as config_file:
            yaml.dump({}, config_file, default_flow_style=False)


def run_crawler(crawler, crawler_type):
    crawler.run(crawler_type)


if __name__ == '__main__':
    check_and_create()
    args = parse_args()
    with open(args.config, 'r', encoding='utf-8') as config_file:
        config = yaml.safe_load(config_file)
    config.update({'is_test': args.test, 'type': args.type})
    crawler = Crawler(config)
    crawler.setup()

    crawler_mapping = {
        "PTT": "PTT",
        "clickme": "clickme",
        "51": "51",
        "happy": "happy",
        "currency": "currency",
        "pttLogin": "pttLogin",
        "delete": "delete"
    }

    if config['type']:
        crawler_type = crawler_mapping.get(config['type'])
        if crawler_type:
            run_crawler(crawler, crawler_type)
        else:
            print(f"錯誤: 沒有找到對應的爬蟲函數 'crawler_{config['type']}'")
    else:
        for crawler_type in ["delete", "PTT", "clickme", "51", "currency"]:
            run_crawler(crawler, crawler_type)

        schedule.every(5).minutes.do(partial(run_crawler, crawler, "PTT"))
        schedule.every(60).minutes.do(partial(run_crawler, crawler, "clickme"))
        schedule.every(60).minutes.do(partial(run_crawler, crawler, "51"))
        schedule.every().day.at("00:00").do(partial(run_crawler, crawler, "currency"))
        schedule.every().day.at("03:00").do(partial(run_crawler, crawler, "pttLogin"))
        schedule.every().day.at("12:00").do(partial(run_crawler, crawler, "currency"))
        schedule.every().day.at("02:00").do(partial(run_crawler, crawler, "delete"))

        while True:
            schedule.run_pending()
            time.sleep(1)
