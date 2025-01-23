from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, HashingTF, IDF
from pyspark.ml.classification import LogisticRegression

def get_spark_analysis(content):
    """
    使用Spark进行文本分析
    """
    # 创建SparkSession
    spark = SparkSession.builder \
        .appName("NewsVerification") \
        .getOrCreate()
    
    # 创建DataFrame
    data = [(content,)]
    df = spark.createDataFrame(data, ["text"])
    
    # 文本处理管道
    tokenizer = Tokenizer(inputCol="text", outputCol="words")
    wordsData = tokenizer.transform(df)
    
    hashingTF = HashingTF(inputCol="words", outputCol="rawFeatures", numFeatures=20)
    featurizedData = hashingTF.transform(wordsData)
    
    idf = IDF(inputCol="rawFeatures", outputCol="features")
    idfModel = idf.fit(featurizedData)
    rescaledData = idfModel.transform(featurizedData)
    
    # 模拟分析结果
    analysis_result = {
        'factors': {
            '情感倾向': 0.85,
            '主题相关性': 0.75,
            '时效性': 0.9,
            '关键词权重': 0.8
        }
    }
    
    # 关闭SparkSession
    spark.stop()
    
    return analysis_result 