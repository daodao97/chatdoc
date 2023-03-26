import os
import shutil
import requests
from bs4 import BeautifulSoup

url = "https://www.jianshu.com/p/474f4713753ct"
response = requests.get(url)

# 创建目录
path = "example"
if not os.path.exists(path):
    os.mkdir(path)

# 解析 HTML 页面
soup = BeautifulSoup(response.text, "html.parser")

# 保存 HTML 页面
with open(f"{path}/index.html", "w") as f:
    f.write(soup.prettify())

# 保存 CSS 文件
for link in soup.find_all("link"):
    if link.get("rel") == ["stylesheet"]:
        css_url = link.get("href")
        css_response = requests.get(css_url)
        css_path = f"{path}/{css_url.split('/')[-1]}"
        with open(css_path, "wb") as f:
            f.write(css_response.content)

# 保存 JavaScript 文件
for script in soup.find_all("script"):
    if script.get("src"):
        js_url = script.get("src")
        js_response = requests.get(js_url)
        js_path = f"{path}/{js_url.split('/')[-1]}"
        with open(js_path, "wb") as f:
            f.write(js_response.content)

# 复制所有图片文件
for img in soup.find_all("img"):
    img_url = img.get("src")
    img_response = requests.get(img_url)
    img_path = f"{path}/{img_url.split('/')[-1]}"
    with open(img_path, "wb") as f:
        f.write(img_response.content)

# 复制所有媒体文件
for source in soup.find_all("source"):
    media_url = source.get("src")
    media_response = requests.get(media_url)
    media_path = f"{path}/{media_url.split('/')[-1]}"
    with open(media_path, "wb") as f:
        f.write(media_response.content)

# 复制所有字体文件
for font in soup.find_all("link"):
    if font.get("rel") == ["stylesheet"] and "font" in font.get("href"):
        font_url = font.get("href")
        font_response = requests.get(font_url)
        font_path = f"{path}/{font_url.split('/')[-1]}"
        with open(font_path, "wb") as f:
            f.write(font_response.content)

# 复制所有其他文件
for link in soup.find_all("link"):
    if not link.get("rel") == ["stylesheet"]:
        file_url = link.get("href")
        if file_url and "." in file_url:
            file_extension = file_url.split(".")[-1]
            if file_extension not in ["css", "js"]:
                file_response = requests.get(file_url)
                file_path = f"{path}/{file_url.split('/')[-1]}"
                with open(file_path, "wb") as f:
                    f.write(file_response.content)
