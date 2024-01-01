# 基于 Python 官方镜像构建
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制应用程序代码到容器中
COPY . /app

# 安装应用程序所需的依赖
RUN pip install -r requirements.txt

# 安装 MySQL 客户端
RUN apt-get update && apt-get install -y default-mysql-client

# 设置环境变量（数据库连接信息）
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=142857
ENV MYSQL_HOST=127.0.0.1
ENV MYSQL_DB=fnav

# 启动应用程序
CMD ["python", "app.py"]
