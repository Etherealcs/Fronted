from flask import Flask
from flask_cors import CORS
from controllers.verification_controller import verification_bp

app = Flask(__name__)
CORS(app)

# 注册蓝图
app.register_blueprint(verification_bp, url_prefix='/api/verify')

if __name__ == '__main__':
    app.run(debug=True) 