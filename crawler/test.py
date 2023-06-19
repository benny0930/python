import requests
from selenium.webdriver.common.by import By
import base

from datetime import datetime

# 获取当前时间
now = datetime.now()

# 获取分钟数
minute = now.minute

# 输出分钟数
print(minute)
