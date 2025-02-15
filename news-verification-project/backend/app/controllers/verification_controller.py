from flask import Blueprint, request, jsonify
from services.text_analysis import analyze_text
from services.image_analysis import analyze_image
from services.video_analysis import analyze_video
from services.spark_analysis import get_spark_analysis
import time
from test_return import TEXT_VERIFICATION_EXAMPLES,IMAGE_VERIFICATION_EXAMPLES,VIDEO_VERIFICATION_EXAMPLES
verification_bp = Blueprint('verification', __name__)

@verification_bp.route('/text', methods=['POST'])
def verify_text():
    content = request.json.get('content')
    print(content)
    print(type(content))
    if not content:
        return jsonify({'error': '未提供文本内容'}), 400
    


    result = analyze_text(content)
    result['timestamp'] = time.time()
    # result = {
    #     'type':'text',
    #     'data':"你也好"
    # }
    result = TEXT_VERIFICATION_EXAMPLES[0]
    # result['analysisData'] = get_spark_analysis(content)
    print(result,'--------')
    return jsonify(result)

@verification_bp.route('/image', methods=['POST'])
def verify_image():
    if 'file' not in request.files:
        return jsonify({'error': '未提供图片文件'}), 400
    
    # file = request.files['file']
    # result = analyze_image(file)
    # result['timestamp'] = time.time()
    # result ={
    #     'type':'image',
    #     'data':"你也好图像"
    # } 
    # print(result,'--------')
    result = IMAGE_VERIFICATION_EXAMPLES[1]
    return jsonify(result)

@verification_bp.route('/video', methods=['POST'])
def verify_video():
    if 'file' not in request.files:
        return jsonify({'error': '未提供视频文件'}), 400
    
    # file = request.files['file']
    # result = analyze_video(file)
    # result['timestamp'] = time.time()
    result = VIDEO_VERIFICATION_EXAMPLES[0]
    
    return jsonify(result) 