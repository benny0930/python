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
    parser.add_argument('--config', '-c', default='config.yml', help='設定擋路徑')
    parser.add_argument('--test', '-t', default=False, action='store_true', help='測試模式')
    return parser.parse_args()


def check_and_create():
    folder_path = "images"
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            print(f"資料夾 '{folder_path}' 新增成功。")
        except OSError as e:
            print(f"無法新增資料夾 '{folder_path}': {e}")

    config_path = 'config.yml'
    if not os.path.exists(config_path):
        try:
            # 如果檔案不存在，創建一個新的 config.yaml
            with open(config_path, 'w') as config_file:
                yaml.dump({}, config_file, default_flow_style=False)
            print(f"配置檔 '{config_path}' 新增成功。")
        except OSError as e:
            print(f"無法新增配置檔 '{config_path}': {e}")


def crawler_PTT(crawler):
    crawler.run("PTT")


def crawler_clickme(crawler):
    crawler.run("clickme")


def crawler_happy(crawler):
    crawler.run("happy")


def crawler_delete():
    crawler.run("delete")


if __name__ == '__main__':
    check_and_create()
    args = parse_args()
    with open(args.config, 'r', encoding='utf-8') as config_file:
        config = yaml.safe_load(config_file)
    config.update({
        'is_test': args.test,
    })
    crawler = Crawler(config)
    crawler.setup()

    # 測試
    crawler.run("happy")
    exit()

    # 创建一个带有参数的部分应用函数
    crawler_PTT_with_args = partial(crawler_PTT, crawler)
    crawler_clickme_with_args = partial(crawler_clickme, crawler)
    crawler_happy_with_args = partial(crawler_happy, crawler)

    # 初始执行一次
    crawler_delete()
    crawler_PTT_with_args()
    crawler_clickme_with_args()
    crawler_happy_with_args()

    schedule.every(5).minutes.do(crawler_PTT_with_args)
    schedule.every(60).minutes.do(crawler_clickme_with_args)
    schedule.every(360).minutes.do(crawler_happy_with_args)
    schedule.every().day.at("02:00").do(crawler_delete)
    #
    while True:
        schedule.run_pending()
        time.sleep(1)
