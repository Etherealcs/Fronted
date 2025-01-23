from flask import Blueprint, request, jsonify
from services.text_analysis import analyze_text
from services.image_analysis import analyze_image
from services.video_analysis import analyze_video
from services.spark_analysis import get_spark_analysis
import time

verification_bp = Blueprint('verification', __name__)

@verification_bp.route('/text', methods=['POST'])
def verify_text():
    content = request.json.get('content')
    if not content:
        return jsonify({'error': '未提供文本内容'}), 400
    
    result = analyze_text(content)
    result['timestamp'] = time.time()
    result['analysisData'] = get_spark_analysis(content)
    
    return jsonify(result)

@verification_bp.route('/image', methods=['POST'])
def verify_image():
    if 'file' not in request.files:
        return jsonify({'error': '未提供图片文件'}), 400
    
    file = request.files['file']
    result = analyze_image(file)
    result['timestamp'] = time.time()
    
    return jsonify(result)

@verification_bp.route('/video', methods=['POST'])
def verify_video():
    if 'file' not in request.files:
        return jsonify({'error': '未提供视频文件'}), 400
    
    file = request.files['file']
    result = analyze_video(file)
    result['timestamp'] = time.time()
    
    return jsonify(result) 