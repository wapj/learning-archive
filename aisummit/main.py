from dotenv import load_dotenv
from langchain.chat_models import BaseChatModel, init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
import json
import httpx

from bs4 import BeautifulSoup

load_dotenv()


def call_model():
    model: BaseChatModel = init_chat_model(
        "gemini-2.5-flash-lite", model_provider="google_genai"
    )

    template = ChatPromptTemplate(
        [
            (
                "system",
                "당신은 뉴스요약 전문가입니다. 100자 이내로 내용을 요약해주세요.",
            ),
            ("human", "제목 : {title}\n내용: {content}\n 주어진 뉴스를 요약하세요."),
        ]
    )

    chain = template | model

    result: AIMessage = chain.invoke(
        {
            "title": "구글이 제미나이 3.0을 출시했다.",
            "content": "2025년 11월에 출시했다. ",
        }
    )

    print(result.content)


def read_data():
    with open("./news_metadata.json") as f:
        data = json.load(f)
        return data


def write_content():
    news_metas = read_data()

    news_data = []

    for data in news_metas[0:]:
        url = data.get("url")
        result = httpx.get(url)
        html_content = result.text
        soup = BeautifulSoup(html_content, "html.parser")
        article_div = soup.find("div", attrs={"data-tiara-layer": "article_body"})
        content = article_div.get_text().replace("\n", "")
        data["content"] = content
        news_data.append(data)

    print(news_data)
    with open("./news_data.json", "w") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)


def read_news_data():
    with open("./news_data.json") as f:
        data = json.load(f)
        return data


def get_prompt_template(system, human):
    return ChatPromptTemplate([("system", system), ("human", human)])


def get_model():
    return init_chat_model("gemini-2.5-flash-lite", model_provider="google_genai")


def summarize_news(title, content):
    prompt = get_prompt_template(
        system="당신은 뉴스요약 전문가입니다. 100자 이내로 내용을 요약해주세요",
        human="제목: {title}\n 내용: {content}\n 주어진 뉴스를 요약해주세요",
    )

    chain = prompt | get_model()
    result: AIMessage = chain.invoke({"title": title, "content": content})
    return result.content


def categorize_news(content):
    prompt = get_prompt_template(
        system="주어진 뉴스를 다음의 카테고리중 하나로 분류하세요. 카테고리만 반환하세요.\n카테고리 : 정치,경제,사회,문화,IT,국제,스포츠,기타",
        human="{content}",
    )

    chain = prompt | get_model()
    result: AIMessage = chain.invoke({"content": content})
    return result.content


def make_report(data):
    prompt = get_prompt_template(
        system="주어진 뉴스의 보고서를 마크다운으로 만들어주세요. ",
        human="{data}",
    )

    chain = prompt | get_model()
    result: AIMessage = chain.invoke({"data": data})
    return result.content


if __name__ == "__main__":
    news_data = read_news_data()
    report_data = []
    for data in news_data:
        title = data.get("title")
        content = data.get("content")

        summary = summarize_news(title, content)
        data["summary"] = summary
        category = categorize_news(summary)
        data["category"] = category
        report_data.append(data)

    report = make_report(report_data)
    print(summary)
    print(category)
