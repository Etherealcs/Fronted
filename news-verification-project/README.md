# 新闻真假检测系统

一个基于深度学习的新闻真假检测系统，支持文本、图像和视频的真实性验证。

## 功能特点

- 文本新闻真假检测
- 图像新闻真假检测
- 视频新闻真假检测
- 基于Spark的大数据分析
- 可视化分析结果展示

## 技术栈

### 前端
- Vue 3 + Vite
- Element Plus UI
- ECharts 数据可视化
- Axios 网络请求

### 后端
- Python Flask
- TensorFlow
- OpenCV
- PySpark

## 环境要求

- Node.js 16+
- Python 3.8+
- Java Runtime Environment (JRE) 8+ (用于PySpark)

## 安装说明

1. 克隆项目
```bash
git clone https://github.com/yourusername/news-verification-project.git
cd news-verification-project
```

2. 安装前端依赖
```bash
cd frontend
npm install
```

3. 安装后端依赖
```bash
cd ../backend
pip install -r requirements.txt
```

## 运行说明

1. 启动前端服务
```bash
cd frontend
npm run dev
```
访问 http://localhost:5173 查看前端页面

2. 启动后端服务
```bash
cd backend
python app/main.py
```
后端服务将在 http://localhost:5000 运行

## API文档

### 文本验证
- 端点：`/api/verify/text`
- 方法：POST
- 请求体：`{ "content": "新闻文本内容" }`

### 图像验证
- 端点：`/api/verify/image`
- 方法：POST
- 请求体：图像文件

### 视频验证
- 端点：`/api/verify/video`
- 方法：POST
- 请求体：视频文件

## 开发说明

- 前端开发时修改 `frontend/src` 目录下的文件
- 后端开发时修改 `backend/app` 目录下的文件
- API接口统一在 `backend/app/controllers` 目录下管理
- 机器学习模型存放在 `backend/app/models` 目录下

## 许可证

MIT License 