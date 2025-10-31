# coding: utf-8
import os
import hashlib
import requests
import traceback
import shutil
import mimetypes


class Base:
    url = []

    def __init__(self, config, ):
        self._config: dict = config

    # proxy
    def get_proxy1(self):
        url = 'http://172.104.85.146'  # X1
        port = 3128
        return f'{url}:{port}'

    def get_proxy2(self):
        url = 'http://172.104.80.118'
        port = 3128
        return f'{url}:{port}'

    def clear_images_folder(self):
        images_folder = 'images'

        # 檢查資料夾是否存在
        if not os.path.exists(images_folder):
            print(f"The folder '{images_folder}' does not exist.")
            return

        # 清空資料夾
        try:
            # 遍歷資料夾中的所有檔案與子資料夾
            for filename in os.listdir(images_folder):
                file_path = os.path.join(images_folder, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # 刪除檔案或符號鏈結
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # 刪除非空資料夾
            print(f"Folder '{images_folder}' has been cleared.")
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {str(e)}")

    def upload_to_laptop_up(self, img_path):
        url = "http://benny.test:8081/api/common/upload"

        if not os.path.isfile(img_path):
            print(f"File does not exist: {img_path}")
            return None

        # 根據副檔名自動判斷 MIME type
        mime_type, _ = mimetypes.guess_type(img_path)
        if not mime_type:
            mime_type = "application/octet-stream"  # fallback

        with open(img_path, "rb") as f:
            # 注意要傳 tuple: (filename, fileobj, mimetype)
            files = {"file": (img_path.split("\\")[-1], f, mime_type)}

            try:
                res = requests.post(url, files=files)
                data = res.json()
                print("Upload response:", data)
                if data.get("code") in (0, 1):  # 根據 FastAdmin 回傳
                    return data.get("data", {}).get("fullurl")  # 回傳 fullurl
                else:
                    print("Upload failed:", data)
                    return None
            except Exception as e:
                print("Upload failed, not JSON or error:", e, res.text[:200])
                return None

    def save_image_to_file(self, image_src, save_path="python_ptt.png"):
        """
        將遠端圖片或超長 src 存成本地檔案
        - image_src: 圖片 URL 或 base64 資料
        - save_path: 要存的本地檔案路徑
        回傳: 存檔路徑，失敗返回 None
        """
        try:
            # 如果是 URL，下載
            if image_src.startswith("http"):
                resp = requests.get(image_src, timeout=10)
                resp.raise_for_status()
                with open(save_path, "wb") as f:
                    f.write(resp.content)
            # 如果是 base64 字串
            elif image_src.startswith("data:image"):
                import base64
                header, encoded = image_src.split(",", 1)
                data = base64.b64decode(encoded)
                with open(save_path, "wb") as f:
                    f.write(data)
            else:
                print("不支援的圖片來源")
                return None
            return save_path
        except Exception as e:
            print("存圖片失敗:", e)
            return None

    def delete_to_laptop_up(self, day=7):
        """
        呼叫 FastAdmin /api/common/delete 刪除 day 天前的上傳檔案
        - day: int, 要刪除的天數，預設 7
        回傳: API 回傳的 JSON dict，失敗返回 None
        """
        url = "http://benny.test:8081/api/common/delete"
        params = {"day": day}

        try:
            res = requests.get(url, params=params, timeout=10)
            data = res.json()
            print("Delete response:", data)
            return data
        except Exception as e:
            print("Delete request failed:", e, getattr(res, "text", "")[:200])
            return None

    def md5_hash(self, text: str) -> str:
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    def contains_video_key(self, title):
        for key in self._config.get('video_key', []):
            # 將 key 以逗號拆分成子條件
            sub_keys = key.split(",")
            # title 必須包含所有子條件
            if all(sub_key in title for sub_key in sub_keys):
                return True  # 找到符合條件立即返回
        return False  # 全部檢查完沒有符合的
