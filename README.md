# Flask 網站專案

這是一個基本的 Flask 網站專案，包含首頁和關於頁面。

## 安裝需求

1. Python 3.x
2. pip（Python 套件管理器）

## 安裝步驟

1. 建立虛擬環境（推薦）：
```bash
python -m venv venv
source venv/bin/activate  # 在 macOS/Linux
# 或
venv\Scripts\activate  # 在 Windows
```

2. 安裝相依套件：
```bash
pip install -r requirements.txt
```

## 執行專案

1. 確保你已經啟動虛擬環境
2. 執行 Flask 應用程式：
```bash
python app.py
```
3. 在瀏覽器中開啟 http://localhost:5000

## 專案結構

```
.
├── app.py              # Flask 應用程式主檔案
├── requirements.txt    # Python 套件相依性
├── static/            # 靜態檔案（CSS、JS、圖片等）
│   └── css/
│       └── style.css
└── templates/         # HTML 模板
    ├── base.html     # 基礎模板
    ├── index.html    # 首頁
    └── about.html    # 關於頁面
``` 