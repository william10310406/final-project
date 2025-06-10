# 導入必要的 Flask 模組
# Flask: 主要的應用程式類別
# render_template: 用於渲染 HTML 模板
from flask import Flask, render_template, request, redirect, url_for, flash
from models import User, Post
from datetime import datetime

# 創建 Flask 應用程式實例
# __name__ 代表目前模組的名稱
app = Flask(__name__)

# 載入配置
app.config['SECRET_KEY'] = 'your-secret-key'  # 用於 flash 訊息

@app.route('/')
def index():
    posts = Post.find_all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/user/<username>')
def user_profile(username):
    user = User.find_by_username(username)
    if user:
        posts = Post.find_by_user_id(user._id)
        return render_template('user_profile.html', user=user, posts=posts)
    return redirect(url_for('index'))

@app.route('/post/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        # 這裡假設我們有一個測試用戶
        test_user = User.find_by_username('test_user')
        if not test_user:
            test_user = User(username='test_user', email='test@example.com').save()
        
        post = Post(title=title, content=content, user_id=test_user._id)
        post.save()
        flash('Post created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('create_post.html')

# 只有當直接執行此檔案時才會執行以下程式碼
# 如果此檔案被當作模組導入則不會執行
if __name__ == '__main__':
    # 啟動 Flask 開發伺服器
    # debug=True 表示開啟除錯模式，可以看到詳細的錯誤訊息
    app.run(debug=True) 