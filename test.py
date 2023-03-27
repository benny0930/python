
import requests

proxies = {
  "http": "183.233.96.44:33080",
  "https": "183.233.96.44:33080",
}


# 檢查IP-------------------------------------------------------------------
ip = requests.get('https://api.ipify.org', proxies=proxies, timeout=10, verify=False).text
print("IP :")
print(ip)
# if ip == "61.61.91.28":
#     print('要換IP!!!!!')
#     # base.time.sleep(30)
#     exit()