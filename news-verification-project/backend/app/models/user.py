from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 验证历史记录关联
    verification_history = db.relationship('VerificationHistory', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class VerificationHistory(db.Model):
    __tablename__ = 'verification_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_type = db.Column(db.String(20), nullable=False)  # text, image, video, mixed
    content = db.Column(db.Text)  # 文本内容或文件路径
    result = db.Column(db.JSON)  # 验证结果
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<VerificationHistory {self.id}>' 