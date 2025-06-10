# 導入所需的 Flask 相關模組
from flask import Flask, render_template, request, redirect, url_for, flash, session
# 導入自定義的資料模型
from models import User, Post
# 導入日期時間處理模組
from datetime import datetime
from functools import wraps

# 創建 Flask 應用程式實例
app = Flask(__name__)
# 設定應用程式密鑰，用於會話管理和訊息閃現
app.config['SECRET_KEY'] = 'your-secret-key'  # 用於 flash 訊息

# 登入要求裝飾器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('請先登入', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# @app.route('/'): 定義根路由，處理網站首頁的訪問
# methods 默認為 ['GET']，表示只接受 GET 請求
@app.route('/')
def index():
    """顯示所有文章的首頁"""
    # 獲取所有文章並按時間排序
    posts = Post.find_all()
    return render_template('index.html', posts=posts)

# @app.route('/about'): 定義關於頁面的路由
# 當用戶訪問 /about 時顯示關於頁面
@app.route('/about')
def about():
    """顯示關於頁面"""
    return render_template('about.html')

# @app.route('/user/<username>'): 定義用戶資料頁面的路由
# <username> 是一個 URL 變數，會被傳遞給視圖函數
@app.route('/user/<username>')
def user_profile(username):
    """
    顯示特定用戶的個人資料頁面
    參數:
        username: 用戶名稱
    """
    # 查找用戶
    user = User.find_by_username(username)
    if user:
        # 獲取該用戶的所有文章
        posts = Post.find_by_user_id(user._id)
        return render_template('user_profile.html', user=user, posts=posts)
    return redirect(url_for('index'))

# @app.route('/post/create'): 定義創建文章的路由
# methods=['GET', 'POST'] 表示這個路由可以處理 GET 和 POST 請求
# @login_required 確保只有登入用戶才能訪問此頁面
@app.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """處理文章的創建"""
    if request.method == 'POST':
        # 從表單獲取文章資料
        title = request.form.get('title')
        content = request.form.get('content')
        
        # 使用當前登入用戶
        user_id = session['user_id']
        
        # 創建並儲存新文章
        post = Post(title=title, content=content, user_id=user_id)
        post.save()
        
        # 顯示成功訊息並重定向到首頁
        flash('文章發布成功！', 'success')
        return redirect(url_for('index'))
    
    # GET 請求時顯示創建文章的表單
    return render_template('create_post.html')

# @app.route('/login'): 定義登入頁面的路由
# methods=['GET', 'POST'] 允許顯示登入表單(GET)和處理登入請求(POST)
@app.route('/login', methods=['GET', 'POST'])
def login():
    """處理用戶登入"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.find_by_username(username)
        if user and user.check_password(password):
            session['user_id'] = str(user._id)
            session['username'] = user.username
            flash('登入成功！', 'success')
            return redirect(url_for('index'))
        
        flash('用戶名或密碼錯誤', 'danger')
    
    return render_template('login.html')

# @app.route('/register'): 定義註冊頁面的路由
# methods=['GET', 'POST'] 允許顯示註冊表單(GET)和處理註冊請求(POST)
@app.route('/register', methods=['GET', 'POST'])
def register():
    """處理用戶註冊"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # 驗證密碼
        if password != confirm_password:
            flash('兩次輸入的密碼不一致', 'danger')
            return render_template('register.html')
        
        # 檢查用戶名是否已存在
        if User.find_by_username(username):
            flash('用戶名已被使用', 'danger')
            return render_template('register.html')
        
        # 檢查電子郵件是否已存在
        if User.find_by_email(email):
            flash('電子郵件已被使用', 'danger')
            return render_template('register.html')
        
        # 創建新用戶
        user = User(username=username, email=email, password=password)
        user.save()
        
        flash('註冊成功！請登入', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# @app.route('/logout'): 定義登出路由
# 不需要 methods 參數，因為只處理 GET 請求
@app.route('/logout')
def logout():
    """處理用戶登出"""
    session.clear()
    flash('您已成功登出', 'success')
    return redirect(url_for('index'))

# 只在直接執行此檔案時運行應用程式
if __name__ == '__main__':
    # debug=True 啟用調試模式，顯示詳細的錯誤信息
    # port=5001 指定使用 5001 端口（避免與 AirPlay 衝突）
    app.run(debug=True, port=5001) 