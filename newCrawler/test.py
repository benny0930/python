import instaloader
from telegram import Bot
import os


# 配置 Instagram 爬取
def download_instagram_content(username):
    L = instaloader.Instaloader()
    L.download_profile(username, profile_pic_only=False)


# 配置 Telegram Bot
def send_to_telegram(bot_token, chat_id, file_path):
    bot = Bot(token=bot_token)
    with open(file_path, 'rb') as file:
        if file_path.endswith('.mp4'):
            bot.send_video(chat_id=chat_id, video=file)
        else:
            bot.send_photo(chat_id=chat_id, photo=file)


def main(instagram_username, telegram_bot_token, telegram_chat_id):
    L = instaloader.Instaloader()
    L.download_profile(instagram_username, profile_pic_only=False)
    content_dir = os.path.join(os.getcwd(), instagram_username)
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            # 假設下載的檔案以 "https://instagram.com/username/" 開頭
            ig_url = f"https://instagram.com/{instagram_username}/"

            file_name = file
            file_extension = os.path.splitext(file)[1]
            file_url = ig_url + "/" + file
        # file_path = os.path.join(root, file)
        # send_to_telegram(telegram_bot_token, telegram_chat_id, file_path)


if __name__ == "__main__":
    instagram_username = 'my._.chuuu'  # 替换为你想要爬取的 Instagram 用户名
    telegram_bot_token = '5652787798:AAHiBgILVoZG-pL55Me7XBJwODWPm7ho1BM'  # 替换为你的 Telegram 机器人 Token
    telegram_chat_id = '-1001911277875'  # 替换为你的 Telegram 聊天 ID

    main(instagram_username, telegram_bot_token, telegram_chat_id)
