import pyautogui
import time
import pygetwindow as gw

class ClickColorPicker:
    def __init__(self, window_title_keyword):
        """
        window_title_keyword: 模擬器視窗標題中包含的關鍵字 (用來定位視窗)
        """
        self.window_title_keyword = window_title_keyword
        self.window = None
        self.update_window()

    def update_window(self):
        # 找到視窗（取第一個符合標題關鍵字的視窗）
        windows = [w for w in gw.getWindowsWithTitle(self.window_title_keyword) if w.isVisible]
        if windows:
            self.window = windows[0]
        else:
            self.window = None

    def wait_for_click(self):
        print(f"請點擊「{self.window_title_keyword}」視窗內任意位置，Ctrl+C 結束")
        try:
            while True:
                self.update_window()
                if not self.window:
                    print("找不到指定視窗，請確認模擬器視窗是否已開啟")
                    time.sleep(2)
                    continue

                # 監聽滑鼠左鍵點擊
                if pyautogui.mouseDown(button='left'):
                    x, y = pyautogui.position()
                    # 計算視窗左上角座標
                    win_left, win_top = self.window.left, self.window.top
                    rel_x, rel_y = x - win_left, y - win_top

                    # 擷取螢幕顏色
                    rgb = pyautogui.screenshot().getpixel((x, y))

                    print(f"視窗相對座標：({rel_x}, {rel_y}), 螢幕絕對座標：({x}, {y}), 顏色：{rgb}")

                    # 等滑鼠放開避免連續輸出
                    while pyautogui.mouseDown(button='left'):
                        time.sleep(0.1)

                time.sleep(0.05)
        except KeyboardInterrupt:
            print("\n結束監聽。")
