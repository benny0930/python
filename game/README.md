# LD Tool - 雷電模擬器自動操作工具

本專案是一組使用 Python 控制 LDPlayer（雷電模擬器）的工具模組，可實現以下功能：

- 綁定模擬器
- 擷取螢幕顏色、自動點擊
- 根據圖像比對自動點擊
- 使用 GUI 框選螢幕區域建立模板圖像

>
>- ld_controller.py # 控制模擬器連線、螢幕截圖、基本點擊
>-  color_checker.py # 擷取座標顏色，條件點擊
>-  image_matcher.py # 圖片比對自動點擊
>-  template_selector.py # GUI 框選畫面存為模板小圖
>-  main.py # 主程式，提供示範用法
>

