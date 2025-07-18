import os

class LDController:
    def __init__(self, adb_address="127.0.0.1:5555"):
        self.adb_address = adb_address

    def bind(self):
        os.system(f'adb connect {self.adb_address}')
        print(f"✔️ 已連接到模擬器 {self.adb_address}")

    def screenshot(self, save_as="screen.png"):
        os.system(f'adb -s {self.adb_address} shell screencap -p /sdcard/{save_as}')
        os.system(f'adb -s {self.adb_address} pull /sdcard/{save_as} .')
        return save_as

    def click(self, x, y):
        os.system(f'adb -s {self.adb_address} shell input tap {x} {y}')
