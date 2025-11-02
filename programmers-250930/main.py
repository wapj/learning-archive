import httpx
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")


def extract_article_text(html_content):
    """
    HTML에서 data-tiara-layer="article_body" 속성을 가진 div의 텍스트를 추출
    """
    soup = BeautifulSoup(html_content, "html.parser")
    article_div = soup.find("div", attrs={"data-tiara-layer": "article_body"})
    if article_div:
        text = article_div.get_text(strip=True, separator="\n")
        lines = [line.strip() for line in text.split("\n") if line.strip() != ""]
        clean_text = "\n".join(lines)
        return clean_text
    else:
        return "article_body를 찾을 수 없습니다."


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
                f"당신은 뉴스분류 전문가 입니다. 주어진 뉴스를 다음 카테고리중 하나로 정확히 분류 해주세요. {','.join(NEWS_CATEGORIES)}"
                "반드시 주어진 카테고리에서만 선택해야합니다. 반환 값으로는 카테고리만 반환합니다. ",
            ),
            ("human", "제목: {title}\n내용: {content}\n\n 주어진 뉴스를 분류합니다."),
        ]
    )
    chain = prompt | llm
    result = chain.invoke({"title": title, "content": content})
    return result.content


def summarize_and_categorize(count, news_data):
    results = []
    for news in news_data[:count]:
        title = news.get("title")
        content = news.get("content")
        summary = summarize_news(title, content)
        print(summary)
        category = categorize_news(title, content)
        results.append(
            {
                "title": title,
                "summary": summary,
                "category": category,
            }
        )
    return results


def fetch_news_data_from_url(url):
    """
    주어진 URL에서 JSON 데이터를 가져옵니다.
    """
    try:
        response = httpx.get(url)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        print(f"URL에서 데이터를 가져오는 중 오류 발생: {e}")
        return None
    except json.JSONDecodeError:
        print("가져온 데이터를 JSON으로 파싱하는 데 실패했습니다.")
        return None


def save_data_as_json(data, filename="generated_datas.json"):
    """
    주어진 데이터를 JSON 파일로 저장합니다.
    """
    if not data:
        print("저장할 데이터가 없습니다.")
        return

    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"데이터를 '{filename}' 파일로 저장했습니다.")


def load_data_from_json(filename="generated_datas.json"):
    """
    JSON 파일에서 데이터를 불러옵니다.
    """
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, filename)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"'{filename}' 파일을 찾을 수 없습니다.")
        return None
    except json.JSONDecodeError:
        print(f"'{filename}' 파일의 데이터를 JSON으로 파싱하는 데 실패했습니다.")
        return None


def main():
    # 1. GitHub에서 원본 뉴스 데이터를 가져옵니다.
    url = "https://raw.githubusercontent.com/wapj/learning-archive/refs/heads/main/programmers-250930/news_data.json"
    news_data_from_url = fetch_news_data_from_url(url)

    # 2. 각 뉴스를 순회하며 'content' 필드를 채웁니다. (불필요한 if문 제거)
    for news in news_data_from_url:
        pc_url = news.get("pcUrl")
        article_text = None
        try:
            response = httpx.get(pc_url)
            response.raise_for_status()
            html_content = response.text
            article_text = extract_article_text(html_content)
        except httpx.RequestError as e:
            print(f"기사 콘텐츠를 가져오는 중 오류 발생 (URL: {pc_url}): {e}")

        # 3. 본문 추출 성공 여부에 따라 'content'를 설정합니다.
        if article_text and "article_body를 찾을 수 없습니다." not in article_text:
            news["content"] = article_text
        else:
            news["content"] = news.get("summary", "내용 없음")

    # 4. 업데이트된 데이터를 'news_data.json'으로 저장합니다.
    save_data_as_json(news_data_from_url, filename="news_data2.json")

    # 5. 저장된 'news_data.json'을 다시 불러와 후속 작업을 진행합니다.
    loaded_news_data = load_data_from_json(filename="news_data2.json")
    if not loaded_news_data:
        print("JSON 파일에서 데이터를 불러오는 데 실패했습니다.")
        return

    # 6. 요약, 분류 및 리포트 생성 작업을 수행합니다.
    news_count = len(loaded_news_data)
    datas = summarize_and_categorize(news_count, loaded_news_data)

    print(datas)
    result = llm.invoke(
        f"{datas}\n 첨부한 데이터를 마크다운으로 변환하고 보고서 형식으로 바꿔주세요. "
        "결괏값으로는 마크다운 형식만 반환하세요."
    )

    current_time = datetime.now().strftime("%Y%m%d_%H%M")
    report_filename = f"report_{current_time}.md"

    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, report_filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(result.content)

    print(f"파일이 '{file_path}'으로 저장되었습니다.")


if __name__ == "__main__":
    main()
