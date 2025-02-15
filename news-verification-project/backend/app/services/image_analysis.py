import cv2
import numpy as np
from datetime import datetime
import os
from PIL import Image
from PIL.ExifTags import TAGS

def analyze_image(file):
    """
    分析图片的真实性
    """
    # 读取图片
    img_array = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    # 保存临时文件用于EXIF分析
    temp_path = 'temp_image.jpg'
    file.seek(0)
    file.save(temp_path)
    
    try:
        # 初始化分析结果
        factors = {}
        analysis_data = {}
        
        # 1. 元数据完整性
        metadata_score = analyze_metadata(temp_path)
        factors['元数据完整性'] = metadata_score
        
        # 2. 图像质量
        quality_score = analyze_quality(image)
        factors['图像质量'] = quality_score
        
        # 3. 内容一致性
        consistency_score = analyze_consistency(image)
        factors['内容一致性'] = consistency_score
        
        # 4. 篡改检测
        tampering_score = detect_tampering(image)
        factors['篡改检测'] = tampering_score
        
        # 深度分析数据
        analysis_data['EXIF数据'] = analyze_exif(temp_path)
        analysis_data['像素分析'] = analyze_pixels(image)
        analysis_data['压缩特征'] = analyze_compression(image)
        analysis_data['光照一致性'] = analyze_lighting(image)
        
        # 计算总体可信度
        confidence = np.mean(list(factors.values()))
        
        return {
            'isReal': confidence > 0.5,
            'confidence': confidence,
            'type': 'image',
            'imageUrl': '/uploads/images/' + os.path.basename(file.filename),
            'reason': generate_reason(factors, confidence),
            'timestamp': datetime.now().isoformat(),
            'factors': factors,
            'analysisData': analysis_data
        }
    finally:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.remove(temp_path)

def analyze_metadata(image_path):
    """元数据完整性分析
    检查图片的EXIF信息完整性
    """
    try:
        image = Image.open(image_path)
        exif = image.getexif()
        if not exif:
            return 0.3
        
        # 检查关键EXIF字段
        key_fields = ['DateTime', 'Make', 'Model']
        field_count = sum(1 for tag, value in exif.items() 
                         if TAGS.get(tag) in key_fields)
        
        return min(1.0, field_count / len(key_fields))
    except:
        return 0.3

def analyze_quality(image):
    """图像质量分析
    分析图像的清晰度、噪点等特征
    """
    # 计算图像清晰度
    laplacian = cv2.Laplacian(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.CV_64F)
    sharpness = np.var(laplacian)
    
    # 计算噪点水平
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    noise = np.std(gray)
    
    # 评分计算
    sharpness_score = min(1.0, sharpness / 1000)
    noise_score = 1.0 - min(1.0, noise / 50)
    
    return (sharpness_score + noise_score) / 2

def analyze_consistency(image):
    """内容一致性分析
    检查图像内容的一致性特征
    """
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 计算图像的梯度
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
    
    # 计算梯度一致性
    consistency = 1.0 - np.std(gradient_magnitude) / np.mean(gradient_magnitude)
    
    return max(0, min(1, consistency))

def detect_tampering(image):
    """篡改检测
    检测图像是否被篡改的特征
    """
    # 错误等级分析（ELA）
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
    
    # 检查不自然的边缘
    score = 1.0 - edge_density
    
    return max(0, min(1, score))

def analyze_exif(image_path):
    """EXIF数据分析"""
    try:
        image = Image.open(image_path)
        exif = image.getexif()
        if not exif:
            return 0.3
        
        # 计算EXIF数据完整度
        total_fields = len(TAGS)
        existing_fields = len(exif.items())
        
        return min(1.0, existing_fields / (total_fields * 0.3))
    except:
        return 0.3

def analyze_pixels(image):
    """像素分析"""
    # 计算像素值分布
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    hist_norm = hist.flatten() / hist.sum()
    
    # 计算分布的均匀性
    uniformity = 1.0 - np.std(hist_norm)
    
    return max(0, min(1, uniformity))

def analyze_compression(image):
    """压缩特征分析"""
    # 计算DCT系数
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    dct = cv2.dct(np.float32(gray))
    
    # 分析高频系数
    high_freq = np.abs(dct[5:, 5:])
    compression_score = 1.0 - np.mean(high_freq) / np.max(high_freq)
    
    return max(0, min(1, compression_score))

def analyze_lighting(image):
    """光照一致性分析"""
    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 分析亮度分量
    v_channel = hsv[:, :, 2]
    brightness_std = np.std(v_channel)
    
    # 计算光照一致性得分
    score = 1.0 - brightness_std / 128
    
    return max(0, min(1, score))

def generate_reason(factors, confidence):
    """生成分析原因说明"""
    high_scores = [k for k, v in factors.items() if v >= 0.7]
    low_scores = [k for k, v in factors.items() if v < 0.3]
    
    if confidence > 0.7:
        return f"基于{', '.join(high_scores)}等方面的分析，该图片真实性较高"
    elif confidence < 0.3:
        return f"基于{', '.join(low_scores)}等方面的分析，该图片可能被篡改"
    else:
        return "图片真实性需要进一步验证" 