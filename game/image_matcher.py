import cv2
import numpy as np

class ImageMatcher:
    def __init__(self, controller):
        self.controller = controller

    def click_image_match(self, template_path, threshold=0.9):
        screenshot_path = self.controller.screenshot()
        big_img = cv2.imread(screenshot_path)
        template = cv2.imread(template_path)

        result = cv2.matchTemplate(big_img, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        print(f"📷 圖片比對相似度：{max_val:.4f}")
        if max_val >= threshold:
            h, w = template.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            print(f"✅ 找到圖像！點擊 ({center_x}, {center_y})")
            self.controller.click(center_x, center_y)
            return True
        else:
            print("❌ 圖像未匹配")
            return False
