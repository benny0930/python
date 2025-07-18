from PIL import Image

class ColorChecker:
    def __init__(self, controller):
        self.controller = controller

    def get_color_at(self, x, y, screenshot_path="screen.png"):
        self.controller.screenshot(screenshot_path)
        img = Image.open(screenshot_path)
        color = img.getpixel((x, y))
        print(f"座標 ({x}, {y}) 的顏色是：{color}")
        return color

    def click_if_color_match(self, check_x, check_y, target_rgb, click_x, click_y):
        color = self.get_color_at(check_x, check_y)
        print(f"🎯 取得顏色 {color}，目標為 {target_rgb}")
        if color == target_rgb:
            print("✅ 顏色符合，進行點擊")
            self.controller.click(click_x, click_y)
        else:
            print("❌ 顏色不符，不執行點擊")


