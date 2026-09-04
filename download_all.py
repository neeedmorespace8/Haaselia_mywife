import os
import re
import time
import requests

# 你的網頁檔案名稱，請確認是否為 index.html
HTML_FILE = "index.html" 
SAVE_DIR = "voice"

# 如果資料夾不存在，就建立一個
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# 用 Set 來裝網址，可以自動過濾掉重複的檔案 (例如 v_022)
download_urls = set()

# 1. 產生 ASMR 的 372 個網址
base_asmr_url = "https://prd-game-a-granbluefantasy.akamaized.net/assets/sound/voice/3040168000_v_{:03d}.mp3"
for i in range(1, 373):
    download_urls.add(base_asmr_url.format(i))

# 2. 讀取你的 HTML 檔案，把寫在陣列裡的其他節慶、戰鬥語音都抓出來
if os.path.exists(HTML_FILE):
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        content = f.read()
        # 利用正規表達式，抓出所有官方的 mp3 網址
        pattern = r'https://prd-game-a-granbluefantasy\.akamaized\.net/assets/sound/voice/[a-zA-Z0-9_]+\.mp3'
        found_urls = re.findall(pattern, content)
        
        for url in found_urls:
            download_urls.add(url)
    print(f"✅ 成功從 {HTML_FILE} 提取所有額外的語音網址！")
else:
    print(f"⚠️ 找不到 {HTML_FILE}，請確認檔名是否正確。目前將只下載 ASMR 語音。")

print(f"🔍 總共找到 {len(download_urls)} 個不重複的語音檔案，準備下載到 '{SAVE_DIR}' 資料夾...\n")

# 3. 開始下載
for index, url in enumerate(download_urls, 1):
    file_name = url.split("/")[-1]
    save_path = os.path.join(SAVE_DIR, file_name)

    # 已經存在就跳過 (防呆/斷線續傳)
    if os.path.exists(save_path):
        print(f"[{index}/{len(download_urls)}] ⏭️ 已存在，跳過：{file_name}")
        continue

    print(f"[{index}/{len(download_urls)}] ⬇️ 正在下載 {file_name}...")
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        else:
            print(f"  ❌ 下載失敗，狀態碼：{response.status_code}")
    except Exception as e:
        print(f"  ❌ 發生錯誤：{e}")
    
    # 稍微暫停，避免請求太快被伺服器阻擋
    time.sleep(0.1)

print("\n🎉 所有語音下載完畢！老婆已經安全抵達你的硬碟了！")