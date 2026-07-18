import hashlib
from pathlib import Path

import requests
from bs4 import BeautifulSoup

URL = "https://mensa.jp/exam/"
HASH_FILE = Path("last_hash.txt")

# ページを取得
response = requests.get(URL, timeout=30)
response.raise_for_status()

# HTMLを整理
soup = BeautifulSoup(response.text, "html.parser")
text = soup.get_text(separator="\n", strip=True)

# ハッシュを作成
current_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

# 前回のハッシュを読む
if HASH_FILE.exists():
    old_hash = HASH_FILE.read_text().strip()
else:
    old_hash = ""

if current_hash == old_hash:
    print("変更なし")
else:
    print("★★ MENSAページが更新されました ★★")
    HASH_FILE.write_text(current_hash)

