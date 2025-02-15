import sys
import os

# 添加父目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from models.user import User
from config import Config
from extensions import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def view_users():
    with app.app_context():
        users = User.query.all()
        print("\n=== 数据库中的用户 ===")
        if not users:
            print("没有找到任何用户")
        for user in users:
            print(f"\nID: {user.id}")
            print(f"用户名: {user.username}")
            print(f"邮箱: {user.email}")
            print(f"创建时间: {user.created_at}")

if __name__ == '__main__':
    view_users() 