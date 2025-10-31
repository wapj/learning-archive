import os
import json
import httpx
from bs4 import BeautifulSoup

from langchain.chat_models import BaseChatModel, init_chat_model
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate


def read_meta_data():
    with open("./news_metadata.json") as f:
        data = json.load(f)
        return data


def read_news_data():
    with open("./news_data.json") as f:
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


def get_model():
    return init_chat_model("gemini-2.5-flash-lite", model_provider="google_genai")


def get_prompt_template(system_prompt, human_prompt):
    return ChatPromptTemplate(
        [
            ("system", system_prompt),
            ("human", human_prompt),
        ]
    )


def summarize_news(title, content):
    prompt = get_prompt_template(
        system_prompt="당신은 뉴스요약 전문가입니다. 100자 이내로 내용을 요약해주세요.",
        human_prompt="제목 : {title}\n내용: {content}\n 주어진 뉴스를 요약해주세요.",
    )

    chain = prompt | get_model()
    result: AIMessage = chain.invoke({"title": title, "content": content})
    return result.content


if __name__ == "__main__":
    # news_data.json 이 없을 때만 실행
    if os.path.exists("./news_data.json"):
        print("뉴스데이터가 있습니다.")
    else:
        save_news_data()

    # 요약
    data: dict = read_news_data()
    for d in data[:1]:
        summary_data = summarize_news(d.get("title"), d.get("content"))
        print(summary_data)
