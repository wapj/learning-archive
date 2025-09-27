from datetime import datetime


import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from datas import news_datas

load_dotenv()
llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")


def extract_article_text(html_content):
    """
    HTML에서 data-tiara-layer="article_body" 속성을 가진 div의 텍스트를 추출
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # data-tiara-layer="article_body" 속성을 가진 요소 찾기
    article_div = soup.find("div", attrs={"data-tiara-layer": "article_body"})

    if article_div:
        # 텍스트만 추출 (줄바꿈과 공백 정리)
        text = article_div.get_text(strip=True, separator="\n")

        # 연속된 공백과 줄바꿈 정리
        lines = [line.strip() for line in text.split("\n") if line.strip() != ""]
        clean_text = "\n".join(lines)

        return clean_text
    else:
        return "article_body를 찾을 수 없습니다."


def data_collect():
    datas = []
    for news in news_datas:
        result = httpx.get(news.get("pcUrl"))
        article_text = extract_article_text(result.text)
        news["article_text"] = article_text
        datas.append(news)
    return datas


DEFAULT_MODEL = "gemini-2.5-flash"


def summarize_news(title, content):
    prompt = ChatPromptTemplate(
        [
            (
                "system",
                "당신은 뉴스 요약 전문가 입니다. "
                "주어진 뉴스 데이터를 핵심만 간결하게 두세 문장으로 요약해주세요.",
            ),
            ("human", "제목: {title}\n내용: {content}\n\n 주어진 뉴스를 요약해주세요."),
        ]
    )
    chain = prompt | llm
    result = chain.invoke({"title": title, "content": content})
    # print(result)
    return result.content


NEWS_CATEGORIES: list[str] = [
    "정치",
    "경제",
    "사회",
    "문화/연예",
    "IT/과학",
    "스포츠",
    "국제",
    "생활/건강",
    "기타",
]


def categorize_news(title, content):
    prompt = ChatPromptTemplate(
        [
            (
                "system",
                "당신은 뉴스분류 전문가 입니다."
                f"주어진 뉴스를 다음 카테고리중 하나로 정확히 분류 해주세요. {','.join(NEWS_CATEGORIES)}"
                "반드시 주어진 카테고리에서만 선택해야합니다. 반환 값으로는 카테고리만 반환합니다. ",
            ),
            ("human", "제목: {title}\n내용: {content}\n\n 주어진 뉴스를 분류합니다."),
        ]
    )

    chain = prompt | llm
    result = chain.invoke({"title": title, "content": content})
    # print(result)
    return result.content


def summarize_and_categorize(count):
    results = []
    for news in news_datas[: count + 1]:
        title = news.get("title")
        content = news.get("content")

        # step2 데이터 요약
        summary = summarize_news(title, content)
        print(summary)

        # step3 카테고리 분류
        category = categorize_news(title, content)
        results.append(
            {
                "title": title,
                "summary": summary,
                "category": category,
            }
        )
    return results


def main():
    # step1 데이터 수집
    # data_collect()
    news_count = len(news_datas)
    datas = summarize_and_categorize(news_count)
    # step4 보고서 작성
    print(datas)

    result = llm.invoke(
        f"{datas}\n 첨부한 데이터를 마크다운으로 변환하고 보고서 형식으로 바꿔주세요. "
        "결괏값으로는 마크다운 형식만 반환하세요."
    )

    current_time = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"report_{current_time}.md"

    # 마크다운 파일로 저장
    with open(filename, "w", encoding="utf-8") as f:
        f.write(result.content)

    print(f"파일이 '{filename}'으로 저장되었습니다.")


if __name__ == "__main__":
    main()
