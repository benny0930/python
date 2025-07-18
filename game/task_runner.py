def run_tasks(ld):
    print(f"開始對模擬器 {ld.adb_port} 執行任務")

    # 範例任務流程
    ld.click(100, 200)  # 點擊A點
    ld.click(300, 400)  # 點擊B點
    ld.click(500, 600)  # 點擊C點

    print("任務完成")
