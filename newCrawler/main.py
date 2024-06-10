# coding: utf-8
import yaml
import os
import schedule
import time
from crawler import Crawler
from argparse import ArgumentParser
from functools import partial
import subprocess
import sys


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


def update_code():
    try:
        result = subprocess.run(["git", "pull"], check=True, capture_output=True, text=True)
        if 'Already up to date' not in result.stdout:
            print("Code updated, restarting...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            print("No updates available.")
    except subprocess.CalledProcessError as e:
        print("Failed to update code:", e)


def run_crawler(crawler, crawler_type):
    crawler.run(crawler_type)


def schedule_tasks(config, crawler):
    if config['type'] == "ZH":
        task_list = [
            (60, run_crawler, "happy"),
            ("03:00", run_crawler, "pttLogin")
        ]
    else:
        task_list = [
            (5, update_code, None),
            (5, run_crawler, "PTT"),
            (60, run_crawler, "clickme"),
            (60, run_crawler, "51"),
            ("00:00", run_crawler, "currency"),
            ("03:00", run_crawler, "delete"),
            ("06:00", run_crawler, "currency"),
            ("12:00", run_crawler, "currency"),
            ("18:00", run_crawler, "currency")
        ]

    for interval, func, arg in task_list:
        if isinstance(interval, int):
            schedule.every(interval).minutes.do(partial(func, crawler, arg) if arg else func)
        else:
            schedule.every().day.at(interval).do(partial(func, crawler, arg) if arg else func)


if __name__ == '__main__':
    check_and_create()
    args = parse_args()
    with open(args.config, 'r', encoding='utf-8') as config_file:
        config = yaml.safe_load(config_file)
    config.update({'is_test': args.test, 'type': args.type})
    print(config)

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

    if config['type'] in crawler_mapping:
        run_crawler(crawler, crawler_mapping[config['type']])
    elif config['type'] == "detail":
        url = "https://www.51cg1.com/archives/146075/"
        crawler.scrape_51_detail("Beauty", "-1001911277875", "test", url)
    else:
        update_code()
        for crawler_type in ["delete", "PTT", "clickme", "51", "currency"]:
            run_crawler(crawler, crawler_type)

        schedule_tasks(config, crawler)

        while True:
            schedule.run_pending()
            time.sleep(1)
