# coding: utf-8
import yaml
import os
import shutil
import schedule
import time
import subprocess
import sys
from crawler import Crawler
from argparse import ArgumentParser
from functools import partial
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, TimeoutError


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


def update_code(config):
    try:
        print("Deleting all contents in images folder")
        delete_all_contents("./images")

        print("Executing git pull")
        result = subprocess.run(["git", "pull"], check=True, capture_output=True, text=True)
        if 'Already up to date' not in result.stdout:
            print("Code updated, restarting...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            print("No updates available.")
    except subprocess.CalledProcessError as e:
        print("Failed to update code:", e)


def run_crawler_with_timeout(crawler, crawler_type, timeout=600):
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(run_crawler, crawler, crawler_type)
        try:
            future.result(timeout=timeout)
        except TimeoutError:
            print(f"run_crawler for {crawler_type} exceeded the timeout of {timeout} seconds and was terminated.")


def run_crawler(crawler, crawler_type):
    crawler.run(crawler_type)


def delete_all_contents(directory):
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
        return

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f"Deleted file: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"Deleted folder: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def schedule_tasks(config, crawler):
    if config['type'] == "ZH":
        task_list = [
            (60, run_crawler_with_timeout, "happy"),
            ("03:00", run_crawler_with_timeout, "pttLogin")
        ]
    else:
        task_list = [
            (1, update_code, None),
            (5, run_crawler_with_timeout, "PTT"),
            (60, run_crawler_with_timeout, "clickme"),
            (60, run_crawler_with_timeout, "51"),
            ("00:00", run_crawler_with_timeout, "currency"),
            ("03:00", run_crawler_with_timeout, "delete"),
            ("06:00", run_crawler_with_timeout, "currency"),
            ("12:00", run_crawler_with_timeout, "currency"),
            ("18:00", run_crawler_with_timeout, "currency")
        ]

    for interval, func, arg in task_list:
        if isinstance(interval, int):
            schedule.every(interval).minutes.do(partial(func, crawler, arg) if arg else func)
        else:
            schedule.every().day.at(interval).do(partial(func, crawler, arg) if arg else func)


def countdown_timer(config, seconds):
    while seconds:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mins, secs = divmod(seconds, 60)
        timer = f'{mins:02}:{secs:02}'
        # print(f"Next task execution in: {timer}", end="\r")
        print(f"{current_time} - {config['version']} - Next task execution in: {timer}", end="\r")
        time.sleep(1)
        seconds -= 1


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
        "TEST": "TEST",
        "PTT": "PTT",
        "clickme": "clickme",
        "51": "51",
        "happy": "happy",
        "currency": "currency",
        "pttLogin": "pttLogin",
        "delete": "delete",
    }

    if config['type'] in crawler_mapping:
        run_crawler_with_timeout(crawler, crawler_mapping[config['type']])
    elif config['type'] == "detail":
        url = "https://www.51cg1.com/archives/146075/"
        crawler.scrape_51_detail("Beauty", "-1001911277875", "test", url)
    else:
        update_code(config)
        crawler_type_arr = ["delete", "PTT", "clickme", "51", "currency"]
        if config['type'] == "ZH":
            crawler_type_arr = ["happy"]
        for crawler_type in crawler_type_arr:
            run_crawler_with_timeout(crawler, crawler_type)

        schedule_tasks(config, crawler)

        while True:
            schedule.run_pending()
            countdown_timer(config, 60)
