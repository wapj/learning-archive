import os
import json
import httpx
from bs4 import BeautifulSoup


def read_meta_data():
    with open("./news_metadata.json") as f:
        data = json.load(f)
        return data


def get_content_from_url(url):
    response: httpx.Response = httpx.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    article_div = soup.find("div", attrs={"data-tiara-layer": "article_body"})
    return article_div.get_text().replace("\n", "")


def save_news_data():
    data: dict = read_meta_data()
    news_data = []
    for d in data:
        content = get_content_from_url(d.get("url"))
        d["content"] = content
        news_data.append(d)

    # news_data를 json파일로 저장
    with open("./news_data.json", "w") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # news_data.json 이 없을 때만 실행
    if os.path.exists("./news_data.json"):
        print("뉴스데이터가 있습니다.")
    else:
        save_news_data()

    # 요약
