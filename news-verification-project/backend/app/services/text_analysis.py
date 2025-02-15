import jieba
import numpy as np
from collections import Counter
import re
from datetime import datetime

def analyze_text(content):
    """
    分析文本内容的真实性
    """
    # 初始化分析结果
    factors = {}
    analysis_data = {}
    
    # 1. 关键词分析
    keywords = analyze_keywords(content)
    factors['关键词分析'] = keywords['score']
    
    # 2. 内容逻辑性
    logic_score = analyze_logic(content)
    factors['内容逻辑性'] = logic_score
    
    # 3. 来源可靠性
    source_score = analyze_source(content)
    factors['来源可靠性'] = source_score
    
    # 4. 语言特征
    language_score = analyze_language(content)
    factors['语言特征'] = language_score
    
    # 深度分析数据
    analysis_data['主题相关性'] = analyze_topic_relevance(content)
    analysis_data['关键词权重'] = keywords['weight']
    analysis_data['情感倾向'] = analyze_sentiment(content)
    analysis_data['时效性'] = analyze_timeliness(content)
    
    # 计算总体可信度
    confidence = np.mean(list(factors.values()))
    
    return {
        'isReal': confidence > 0.5,
        'confidence': confidence,
        'type': 'text',
        'content': content,
        'reason': generate_reason(factors, confidence),
        'timestamp': datetime.now().isoformat(),
        'factors': factors,
        'analysisData': analysis_data
    }

def analyze_keywords(text):
    """关键词分析
    检测文本中的关键词特征，包括：
    1. 标题党关键词
    2. 新闻常用词汇
    3. 专业术语
    """
    # 分词
    words = list(jieba.cut(text))
    
    # 标题党关键词列表（示例）
    clickbait_words = {'震惊', '惊呆', '爆炸', '狂热', '疯狂', '惊人'}
    
    # 新闻常用词汇（示例）
    news_words = {'报道', '消息', '新闻', '记者', '采访', '表示'}
    
    # 计算得分
    clickbait_count = sum(1 for word in words if word in clickbait_words)
    news_terms_count = sum(1 for word in words if word in news_words)
    
    # 评分计算
    score = 1.0 - (clickbait_count / len(words)) * 2 + (news_terms_count / len(words))
    score = max(0, min(1, score))  # 确保分数在0-1之间
    
    # 计算关键词权重
    word_freq = Counter(words)
    total_words = len(words)
    weight = sum(count/total_words for word, count in word_freq.items() if word in news_words) 
    
    return {
        'score': score,
        'weight': min(1.0, weight * 2)  # 归一化权重
    }

def analyze_logic(text):
    """内容逻辑性分析
    检查文本的逻辑连贯性：
    1. 句子间的连接词使用
    2. 段落结构
    3. 时间顺序
    """
    # 连接词列表
    connectives = {'因此', '所以', '但是', '然而', '并且', '而且'}
    
    # 分句
    sentences = re.split('[。！？]', text)
    sentences = [s for s in sentences if s.strip()]
    
    # 计算连接词使用率
    connective_count = sum(1 for s in sentences if any(c in s for c in connectives))
    logic_score = connective_count / len(sentences) if sentences else 0
    
    return min(1.0, logic_score * 1.5)  # 归一化分数

def analyze_source(text):
    """来源可靠性分析
    检查文本中的信息来源：
    1. 官方来源引用
    2. 具体数据引用
    3. 专家观点引用
    """
    # 可靠来源关键词
    reliable_sources = {'专家', '研究表明', '数据显示', '官方', '报道'}
    
    # 计算可靠来源引用次数
    source_count = sum(1 for source in reliable_sources if source in text)
    
    return min(1.0, source_count * 0.2)  # 归一化分数

def analyze_language(text):
    """语言特征分析
    分析文本的语言使用特征：
    1. 情感词使用
    2. 标点符号使用
    3. 句子长度分布
    """
    # 计算标点符号使用
    punctuation_ratio = len(re.findall('[，。！？]', text)) / len(text)
    
    # 计算平均句子长度
    sentences = re.split('[。！？]', text)
    sentences = [s for s in sentences if s.strip()]
    avg_sentence_length = np.mean([len(s) for s in sentences]) if sentences else 0
    
    # 评分计算
    score = 1.0 - abs(punctuation_ratio - 0.1) - abs(avg_sentence_length - 30) / 100
    
    return max(0, min(1, score))

def analyze_topic_relevance(text):
    """主题相关性分析"""
    # 简单实现：检查关键主题词的重复度
    words = list(jieba.cut(text))
    word_freq = Counter(words)
    most_common = word_freq.most_common(5)
    
    return min(1.0, sum(count/len(words) for word, count in most_common) * 2)

def analyze_sentiment(text):
    """情感倾向分析"""
    # 简单的情感词典方法
    positive_words = {'好', '优秀', '成功', '发展', '进步'}
    negative_words = {'差', '失败', '问题', '困难', '危机'}
    
    words = list(jieba.cut(text))
    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)
    
    total = positive_count + negative_count
    if total == 0:
        return 0.5
    
    return positive_count / total

def analyze_timeliness(text):
    """时效性分析"""
    # 检查时间相关词汇
    time_words = {'今天', '昨天', '本月', '最近', '日前'}
    date_patterns = r'\d{4}年\d{1,2}月\d{1,2}日|\d{4}-\d{1,2}-\d{1,2}'
    
    time_words_count = sum(1 for word in time_words if word in text)
    date_count = len(re.findall(date_patterns, text))
    
    return min(1.0, (time_words_count + date_count) * 0.3)

def generate_reason(factors, confidence):
    """生成分析原因说明"""
    high_scores = [k for k, v in factors.items() if v >= 0.7]
    low_scores = [k for k, v in factors.items() if v < 0.3]
    
    if confidence > 0.7:
        return f"基于{', '.join(high_scores)}等方面的强有力表现，判定该内容可信度较高"
    elif confidence < 0.3:
        return f"基于{', '.join(low_scores)}等方面的不足，判定该内容可信度较低"
    else:
        return "综合多个维度分析，该内容真实性有待进一步验证" 