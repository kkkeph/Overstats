FROM python:3.12-slim

# 安装系统依赖（Pillow 需要 freetype，中文字体渲染需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    libfreetype6 \
    libjpeg62-turbo \
    libopenjp2-7 \
    libwebp7 \
    libtiff6 \
    libimagequant0 \
    libraqm0 \
    && rm -rf /var/lib/apt/lists/*

# 创建非 root 用户
RUN useradd --create-home --shell /bin/bash overstats

WORKDIR /opt/overstats

# 先装依赖（利用 Docker 缓存层）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY --chown=overstats:overstats . .

# 创建运行时缓存目录
RUN mkdir -p cache res/cache_img res/query_tool_assets \
    src/modules/dashen_summary/runtime/cache \
    && chown -R overstats:overstats cache res/ src/

# Entrypoint 在容器启动时修正挂载卷的权限（Docker volumes 会覆盖构建时的目录）
COPY deploy/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

USER overstats

EXPOSE 18080

CMD ["python", "run.py"]
