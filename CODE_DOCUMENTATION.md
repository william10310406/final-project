# 專案程式碼詳解

### 文件目的
本文件旨在提供對「Flask 部落格與捷運資訊系統」專案的深入程式碼解釋，幫助您理解系統的架構、設計模式以及各個模組的具體實現。

---

### 1. 系統架構與設計模式

本專案採用經典的 **MVC (Model-View-Controller)** 設計模式，這是一種將應用程式邏輯與用戶介面分離的架構模式。

- **Model (模型)**: `models.py`
  - 負責處理應用程式的數據和業務邏輯。
  - 直接與 MongoDB 資料庫互動，執行增刪改查 (CRUD) 操作。
  - 定義了如 `User`, `Post` 等資料結構。

- **View (視圖)**: `templates/` 目錄
  - 負責展示數據，即用戶介面。
  - 使用 Jinja2 模板引擎，將後端傳遞的數據渲染成 HTML 頁面。

- **Controller (控制器)**: `app.py`
  - 作為模型和視圖之間的中介。
  - 接收用戶請求，調用相應的模型處理數據，然後將結果傳遞給視圖進行渲染。
  - 定義了所有的路由 (URL endpoints)。

---

### 2. 檔案結構與程式碼詳解

#### 2.1 `app.py` - 主應用程式 (控制器)

這是專案的核心，負責處理所有用戶請求和業務流程。

**關鍵部分詳解:**

1.  **模組導入與配置 (L1-L15)**
    ```python
    from flask import Flask, ...
    from models import User, Post, ...
    import os

    # 從環境變數讀取配置
    MONGODB_URI = os.environ.get(...)
    SECRET_KEY = os.environ.get(...)
    DEBUG = os.environ.get(...)
    ```
    - **說明**: 這裡導入所有必要的模組。配置部分利用 `os.environ.get()` 從環境變數讀取敏感資訊（如資料庫連接字串和密鑰），這是一種安全的作法，避免將敏感資訊直接寫在程式碼中。如果環境變數不存在，則使用預設值，方便本地開發。

2.  **資料庫與應用程式初始化 (L17-L24)**
    ```python
    init_db(MONGODB_URI)
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.debug = DEBUG
    ```
    - **說明**: `init_db(MONGODB_URI)` 調用 `models.py` 中的函數來建立與 MongoDB 的連接。接著，創建 Flask 應用實例 `app`，並將前面讀取的配置應用到 `app` 上。

3.  **登入要求裝飾器 (L27-L36)**
    ```python
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('請先登入', 'warning')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    ```
    - **說明**: 這是一個 Python 裝飾器，用於保護需要用戶登入才能訪問的路由。它檢查 `session` 中是否存在 `user_id`。如果不存在，就將用戶重定向到登入頁面。我們將它應用在如 `@app.route('/post/create')` 等路由上。

4.  **路由定義 (L40-L227)**
    - **範例: `index()` 路由 (L40-L45)**
      ```python
      @app.route('/')
      def index():
          posts = Post.find_all()
          return render_template('index.html', posts=posts)
      ```
      - **說明**: 這是網站的首頁。它調用 `Post` 模型中的 `find_all()` 方法從資料庫獲取所有文章，然後使用 `render_template()` 將文章數據傳遞給 `index.html` 模板進行渲染。

    - **範例: `login()` 路由 (L108-L125)**
      ```python
      @app.route('/login', methods=['GET', 'POST'])
      def login():
          if request.method == 'POST':
              user = User.find_by_username(request.form.get('username'))
              if user and user.check_password(request.form.get('password')):
                  session['user_id'] = str(user._id)
                  # ...
                  return redirect(url_for('index'))
          return render_template('login.html')
      ```
      - **說明**: 此路由同時處理 `GET` (顯示登入頁面) 和 `POST` (處理登入表單) 請求。當用戶提交表單時，它會：
        1. 根據用戶名查找用戶。
        2. 使用 `check_password()` 方法（內部使用 `werkzeug` 庫安全地比對密碼雜湊值）驗證密碼。
        3. 如果驗證成功，將用戶的 `_id` 存入 `session`，完成登入。

5.  **API 路由 (L195-L220)**
    ```python
    @app.route('/api/mrt/carriage/<line_name>')
    def get_carriage_data(line_name):
        data = MRTCarriage.get_latest_by_line(line_name)
        return jsonify([...])
    ```
    - **說明**: 這是提供給前端 JavaScript 使用的 API 端點。它不返回 HTML，而是使用 `jsonify()` 將從模型獲取的數據轉換為 JSON 格式。前端頁面可以透過 AJAX 請求這個 API 來獲取數據並動態更新圖表，而無需刷新整個頁面。

---

#### 2.2 `models.py` - 資料模型 (模型)

此檔案定義了所有與資料庫互動的類別和方法，是專案的數據核心。

**關鍵部分詳解:**

1.  **資料庫初始化 (L22-L27)**
    ```python
    client = None
    db = None

    def init_db(mongodb_uri):
        global client, db
        client = MongoClient(mongodb_uri)
        db = client.flask_app
    ```
    - **說明**: 這裡採用了延遲初始化的模式。`db` 變數一開始是 `None`。`init_db` 函數會在 `app.py` 啟動時被調用，建立實際的資料庫連接。`global` 關鍵字確保我們修改的是全域的 `db` 變數。

2.  **模型類別定義 (例如 `User` 類)**
    - **`get_collection()` 方法 (L33-L36)**
      ```python
      @classmethod
      def get_collection(cls):
          return None if db is None else db.users
      ```
      - **說明**: 這是為了解決啟動時序問題而設計的。直接在類別層級定義 `collection = db.users` 會在 `db` 初始化之前執行而導致錯誤。這個類別方法確保只有在 `db` 連接建立後，才返回 `users` 集合的引用。

    - **CRUD 方法 (例如 `find_by_username`) (L91-L107)**
      ```python
      @classmethod
      def find_by_username(cls, username):
          collection = cls.get_collection()
          if collection is None:
              raise RuntimeError("Database not initialized")
          
          user_data = collection.find_one({'username': username})
          if user_data:
              return cls(**user_data) # 簡化版
          return None
      ```
      - **說明**: 所有的數據操作方法都遵循這個模式：
        1.  調用 `get_collection()` 獲取集合對象。
        2.  檢查集合是否存在，如果不存在則拋出錯誤。
        3.  使用 PyMongo 的方法 (如 `find_one`, `insert_one`) 進行資料庫操作。
        4.  將從資料庫獲取的字典數據轉換為類別實例 (物件) 後返回。

3.  **密碼處理 (在 `User` 類中)**
    - **`__init__` (L47)**: `self.password_hash = generate_password_hash(password)`
    - **`check_password` (L86)**: `check_password_hash(self.password_hash, password)`
    - **說明**: 我們從不直接存儲明文密碼。在用戶註冊時，使用 `werkzeug.security` 的 `generate_password_hash` 將密碼轉換為安全的雜湊值。在登入驗證時，使用 `check_password_hash` 來比對用戶輸入的密碼和存儲的雜湊值，確保了密碼的安全性。

---

#### 2.3 `templates/` - HTML 模板 (視圖)

此目錄存放所有用戶看到的 HTML 頁面。

**關鍵部分詳解:**

1.  **`base.html` - 基礎模板**
    ```html
    <!DOCTYPE html>
    <html>
    <head>...</head>
    <body>
        <nav>...</nav>
        {% with messages = get_flashed_messages(with_categories=true) %}
        ...
        {% endwith %}
        
        {% block content %}{% endblock %}
    </body>
    </html>
    ```
    - **說明**: 這是所有頁面的父模板。其他模板 (如 `index.html`) 會繼承它。
      - `{% block content %}`: 定義了一個內容區塊，子模板可以在這裡插入自己的內容。
      - `get_flashed_messages()`: 用於顯示從後端 `flash()` 函數發送的提示訊息（如「登入成功」）。

2.  **`index.html` - 使用 Jinja2 語法**
    ```html
    {% extends "base.html" %}
    {% block content %}
        <h1>所有文章</h1>
        {% for post in posts %}
            <article>
                <h2>{{ post.title }}</h2>
                <p>{{ post.content }}</p>
            </article>
        {% else %}
            <p>目前沒有任何文章。</p>
        {% endfor %}
    {% endblock %}
    ```
    - **說明**:
      - `{% extends "base.html" %}`: 表示此模板繼承自 `base.html`。
      - `{% for post in posts %}`: 這是 Jinja2 的迴圈語法。`posts` 是從 `app.py` 的 `index` 函數傳遞過來的文章列表。我們遍歷這個列表並顯示每篇文章的標題和內容。
      - `{{ post.title }}`: 雙大括號用於將變數的值輸出到 HTML 中。

---

#### 2.4 `render.yaml` - 部署配置檔案

此檔案告訴 Render 雲端平台如何部署我們的應用。

```yaml
services:
  - type: web
    name: mrt-visualization
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn wsgi:app"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: MONGODB_URI
        fromDatabase:
          name: your_db_name
          property: connectionString
```
- **說明**:
  - `type: web`: 表示這是一個 Web 服務。
  - `buildCommand`: 在部署前執行的命令，用於安裝所有依賴。
  - `startCommand`: 啟動應用程式的命令。我們使用 `gunicorn` 這個生產級別的 WSGI 伺服器來運行我們的應用，入口點是 `wsgi.py` 中的 `app` 物件。
  - `envVars`: 在這裡配置生產環境的環境變數。

---

### 總結

本專案透過清晰的 MVC 架構，將數據處理、業務邏輯和用戶介面有效分離。`app.py` 作為控制器，協調 `models.py` (模型) 和 `templates/` (視圖) 的工作。程式碼在安全性 (密碼雜湊、環境變數)、可讀性 (註解、模組化) 和可部署性 (`render.yaml`) 方面都進行了考量，是一個結構完整且符合現代 Web 開發實踐的專案。 