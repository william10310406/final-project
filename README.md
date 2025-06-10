# Flask 部落格系統

這是一個使用 Flask 和 MongoDB 建立的簡單部落格系統。

## 功能特點

- 文章管理
  - 查看所有文章
  - 創建新文章
  - 按時間排序顯示
- 用戶系統
  - 用戶資料頁面
  - 查看用戶發布的文章
- 捷運資料爬蟲
  - 自動抓取捷運車廂擁擠度資料
  - 資料儲存為 CSV 格式
  - 完整的日誌記錄

## 技術棧

- 後端框架：Flask
- 資料庫：MongoDB
- 前端框架：Bootstrap
- 其他工具：
  - requests（HTTP 請求）
  - pymongo（MongoDB 驅動）
  - python-dotenv（環境變數管理）

## 安裝說明

1. 克隆專案：
```bash
git clone [專案網址]
cd [專案資料夾]
```

2. 建立虛擬環境：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows
```

3. 安裝依賴：
```bash
pip install -r requirements.txt
```

4. 設定環境變數：
- 複製 `.env.example` 為 `.env`
- 修改 `.env` 中的設定

5. 啟動 MongoDB：
```bash
brew services start mongodb-community
```

6. 運行應用：
```bash
python app.py
```

## 專案結構

```
.
├── app.py              # 主應用程式
├── config.py           # 配置文件
├── models.py           # 資料模型
├── requirements.txt    # 依賴套件
├── crawler/            # 爬蟲程式
│   └── carriage.py    # 捷運車廂爬蟲
├── static/            # 靜態文件
│   └── css/          # CSS 樣式
├── templates/         # HTML 模板
│   ├── base.html     # 基礎模板
│   ├── index.html    # 首頁
│   └── about.html    # 關於頁面
└── README.md         # 說明文件
```

## 使用說明

1. 瀏覽文章：
   - 訪問首頁查看所有文章
   - 文章按發布時間排序

2. 發布文章：
   - 點擊 "Create New Post"
   - 填寫標題和內容
   - 提交表單

3. 查看用戶資料：
   - 點擊用戶名稱
   - 查看用戶資料和發布的文章

4. 爬取捷運資料：
   - 運行 `python crawler/carriage.py`
   - 資料將保存在指定目錄

## 開發說明

- 使用 `debug=True` 運行以獲取詳細錯誤訊息
- 檢查 `logs` 目錄中的日誌文件
- 遵循 PEP 8 程式碼風格指南

## 注意事項

- 確保 MongoDB 服務正在運行
- 定期備份資料庫
- 在生產環境中更改預設密鑰

## 授權

MIT License 

# 捷運資料視覺化系統

這個專案是一個使用 Flask 框架開發的捷運資料視覺化系統，可以顯示即時的捷運人流量和車廂擁擠度資訊。

## 環境設置

1. 安裝 Python 套件：
```bash
pip install -r requirements.txt
```

2. 連接資料庫：
   - 如果你是在本機運行（資料庫在你自己的電腦上）：
     - 確保 MongoDB 服務已啟動
     - 使用預設的連接設置即可

   - 如果你要連接到其他人的資料庫：
     - 在 `models.py` 中修改連接字符串：
     ```python
     MONGODB_URI = 'mongodb://其他人的IP:27017/'
     ```
     - 詳細說明請參考 `CONNECT.md`

3. 運行應用：
```bash
python app.py
```

## 注意事項

- 確保已安裝所有必要的 Python 套件
- 確保 MongoDB 服務正在運行
- 如果要連接遠端資料庫，確保在同一個網路環境下

## 資料結構

系統包含兩個主要的資料集：
1. 捷運人流量資料
2. 車廂擁擠度資料

每個資料集都包含時間戳記和相關的測量值。

## 需要幫助？

如果遇到連接問題，請參考：
1. `CONNECT.md` 中的連接指南
2. 聯繫資料庫管理員 