from flask import Flask
from flask_cors import CORS
from controllers.verification_controller import verification_bp
from controllers.auth_controller import auth_bp
from extensions import db, migrate
from config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化扩展
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    # 注册蓝图
    app.register_blueprint(verification_bp, url_prefix='/api/verify')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # 创建上传目录
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 确保所有数据库表都已创建
    with app.app_context():
        db.create_all()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 