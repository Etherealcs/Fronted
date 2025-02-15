from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from extensions import db
import jwt
import datetime
from config import Config
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        logger.info(f"Received registration request: {data}")
        
        # 验证必要字段
        if not all(k in data for k in ['username', 'password', 'email']):
            return jsonify({'error': '缺少必要字段'}), 400
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': '用户名已存在'}), 400
        
        # 检查邮箱是否已存在
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': '邮箱已被注册'}), 400
        
        # 创建新用户
        hashed_password = generate_password_hash(data['password'])
        new_user = User(
            username=data['username'],
            password=hashed_password,
            email=data['email']
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            logger.info(f"Successfully registered user: {data['username']}")
            return jsonify({'message': '注册成功'}), 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Database error during registration: {str(e)}")
            return jsonify({'error': f'注册失败: {str(e)}'}), 500
            
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        return jsonify({'error': f'注册失败: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        logger.info(f"Received login request for user: {data.get('username')}")
        
        if not all(k in data for k in ['username', 'password']):
            return jsonify({'error': '缺少必要字段'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'error': '用户名或密码错误'}), 401
        
        # 生成JWT令牌
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }, Config.SECRET_KEY, algorithm='HS256')
        
        logger.info(f"User logged in successfully: {user.username}")
        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return jsonify({'error': f'登录失败: {str(e)}'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # 由于使用JWT，服务器端不需要处理登出
    return jsonify({'message': '登出成功'})

@auth_bp.route('/user', methods=['GET'])
def get_user_info():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未提供认证令牌'}), 401
    
    try:
        token = token.split(' ')[1]  # Bearer token
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        user = User.query.get(payload['user_id'])
        
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })
    except jwt.ExpiredSignatureError:
        return jsonify({'error': '令牌已过期'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': '无效的令牌'}), 401 