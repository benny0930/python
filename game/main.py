from ld_controller import LDController
from color_checker import ColorChecker
from image_matcher import ImageMatcher
from template_selector import TemplateSelector
import task_runner

def development_mode(ld):
    print("=== 開發模式 ===")
    checker = ColorChecker(ld)
    checker.click_if_color_match(100, 200, (255, 0, 0), 300, 400)

    matcher = ImageMatcher(ld)
    matcher.click_image_match("template.png", threshold=0.9)

    TemplateSelector(ld, save_path="new_template.png")

def execution_mode(ld):
    print("=== 執行模式 ===")
    task_runner.run_tasks(ld)

def main():
    # 輸入模式
    mode = input("請輸入執行模式 (dev:開發 / run:執行): ").strip().lower()
    port = input("請輸入模擬器 ADB 連接埠（如127.0.0.1:5555）: ").strip()
    ld = LDController(port)
    ld.bind()

    if mode == "dev":
        development_mode(ld)
    elif mode == "run":
        execution_mode(ld)
    else:
        print("輸入錯誤，請輸入 'dev', 'run' 或 'multi'")

if __name__ == "__main__":
    main()
