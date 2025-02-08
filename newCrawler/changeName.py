import os
import shutil

def copy_and_rename_folder(folder_path, start_number):
    try:
        # 確保起始號碼是整數
        start_number = int(start_number)

        # 確保資料夾存在
        if not os.path.exists(folder_path):
            print(f"Folder does not exist: {folder_path}")
            return

        # 計算新資料夾名稱
        end_number = start_number + 49
        new_folder_name = f"{start_number:04}-{end_number:04}"
        new_folder_path = os.path.join(os.path.dirname(folder_path), new_folder_name)

        # 複製資料夾
        shutil.copytree(folder_path, new_folder_path)
        print(f"Folder copied to: {new_folder_path}")

        # 獲取新資料夾內所有 .md 檔案並排序
        md_files = [f for f in os.listdir(new_folder_path) if f.endswith('.md')]
        md_files.sort()

        # 依序重新命名
        for index, filename in enumerate(md_files):
            new_name = f"{start_number + index:04}.md"
            old_path = os.path.join(new_folder_path, filename)
            new_path = os.path.join(new_folder_path, new_name)

            os.rename(old_path, new_path)
            with open(new_path, 'w') as file:
                file.truncate(0)
            print(f"Renamed: {filename} -> {new_name}")
        print("Folder copied and renaming completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

# 使用範例
if __name__ == "__main__":
    folder_path = input("Enter the folder path: ")
    start_number = input("Enter the starting number: ")
    copy_and_rename_folder(folder_path, start_number)