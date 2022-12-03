import random
import base
import db
import gc
import comic
import actor
import requests
import threading
import numpy as np
import datetime as dt
import telegram

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

bot = telegram.Bot(token='5652787798:AAHiBgILVoZG-pL55Me7XBJwODWPm7ho1BM')
chat_id = '-695426401'
url = 'https://www.jkforum.net/thread-15850270-1-1.html'

title = 'Gamesale'
results = db.select(" SELECT id, title, is_active FROM fa_is_open WHERE `title` = '%s'" % (title))
[id, title, is_active] = results[0]
print([id, title, is_active] )