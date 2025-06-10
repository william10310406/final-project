# 導入所需的模組
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

# 創建 MongoDB 客戶端
client = MongoClient('mongodb://localhost:27017/')
db = client.flask_app

# User 集合操作類
class User:
    collection = db.users

    def __init__(self, username, email, created_at=None):
        self.username = username
        self.email = email
        self.created_at = created_at or datetime.utcnow()

    def save(self):
        if not hasattr(self, '_id'):
            user_data = {
                'username': self.username,
                'email': self.email,
                'created_at': self.created_at
            }
            result = self.collection.insert_one(user_data)
            self._id = result.inserted_id
        return self

    @classmethod
    def find_by_username(cls, username):
        user_data = cls.collection.find_one({'username': username})
        if user_data:
            user = cls(
                username=user_data['username'],
                email=user_data['email'],
                created_at=user_data['created_at']
            )
            user._id = user_data['_id']
            return user
        return None

    @classmethod
    def find_all(cls):
        return [cls(
            username=user_data['username'],
            email=user_data['email'],
            created_at=user_data['created_at']
        ) for user_data in cls.collection.find()]

# Post 集合操作類
class Post:
    collection = db.posts

    def __init__(self, title, content, user_id, created_at=None):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.created_at = created_at or datetime.utcnow()

    def save(self):
        if not hasattr(self, '_id'):
            post_data = {
                'title': self.title,
                'content': self.content,
                'user_id': self.user_id,
                'created_at': self.created_at
            }
            result = self.collection.insert_one(post_data)
            self._id = result.inserted_id
        return self

    @classmethod
    def find_all(cls):
        return [cls(
            title=post_data['title'],
            content=post_data['content'],
            user_id=post_data['user_id'],
            created_at=post_data['created_at']
        ) for post_data in cls.collection.find().sort('created_at', -1)]

    @classmethod
    def find_by_user_id(cls, user_id):
        return [cls(
            title=post_data['title'],
            content=post_data['content'],
            user_id=post_data['user_id'],
            created_at=post_data['created_at']
        ) for post_data in cls.collection.find({'user_id': user_id}).sort('created_at', -1)] 