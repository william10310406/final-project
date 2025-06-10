# 導入必要的 Flask 模組
# Flask: 主要的應用程式類別
# render_template: 用於渲染 HTML 模板
from flask import Flask, render_template

# 創建 Flask 應用程式實例
# __name__ 代表目前模組的名稱
app = Flask(__name__)

# 定義首頁路由
# 當用戶訪問根目錄 '/' 時執行此函數
@app.route('/')
def home():
    # 渲染 index.html 模板並返回給用戶
    return render_template('index.html')

# 定義關於頁面路由
# 當用戶訪問 '/about' 時執行此函數
@app.route('/about')
def about():
    # 渲染 about.html 模板並返回給用戶
    return render_template('about.html')

# 只有當直接執行此檔案時才會執行以下程式碼
# 如果此檔案被當作模組導入則不會執行
if __name__ == '__main__':
    # 啟動 Flask 開發伺服器
    # debug=True 表示開啟除錯模式，可以看到詳細的錯誤訊息
    app.run(debug=True) 