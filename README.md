# Flask 部落格與捷運資訊系統

這是一個使用 Flask 和 MongoDB 建立的網站，結合了部落格功能和台北捷運即時資訊。

## 功能特點

- 用戶系統（註冊、登入、個人頁面）
- 文章發布系統
- 留言功能
- 捷運車廂擁擠度顯示
- 捷運站點人流量統計

## 技術棧

- Python 3.x
- Flask
- MongoDB
- Bootstrap 5
- JavaScript

## 安裝與設置

1. 克隆專案：
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. 安裝依賴：
   ```bash
   pip install -r requirements.txt
   ```

3. 配置：
   - 所有配置都在 `config.py` 文件中
   - 如需修改設置（如數據庫連接），請編輯該文件

4. 運行應用：
   ```bash
   python run.py
   ```

5. 訪問網站：
   - 打開瀏覽器訪問 `http://localhost:8080`

## 開發說明

- 主要配置在 `config.py`
- 數據模型在 `models.py`
- 路由和視圖在 `app.py`
- 模板文件在 `templates/` 目錄
- 靜態文件在 `static/` 目錄

## 注意事項

- 這是一個示範項目，用於學習目的
- 生產環境部署時請更改密鑰和數據庫設置
- 建議使用虛擬環境運行專案

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