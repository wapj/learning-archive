from dotenv import load_dotenv

from langchain.chat_models import BaseChatModel, init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

load_dotenv()


def hello_langchain():
    model: BaseChatModel = init_chat_model(
        "gemini-2.5-flash-lite", model_provider="google_genai"
    )

    result: AIMessage = model.invoke("안녕하세요?")

    print(result.content)


def input_human_message():
    model: BaseChatModel = init_chat_model(
        "gemini-2.5-flash-lite", model_provider="google_genai"
    )

    result: AIMessage = model.invoke([HumanMessage("하루 수면시간은 몇시간이 좋아?")])
    print(result.content)


def input_messages():
    model: BaseChatModel = init_chat_model(
        "gemini-2.5-flash-lite", model_provider="google_genai"
    )

    result: AIMessage = model.invoke(
        [
            SystemMessage("당신은 까칠한 AI 도우미 입니다. 단답형으로 대답하세요."),
            HumanMessage("하루 수면시간은 몇시간이 좋아?"),
        ]
    )
    print(result.content)


def prompt_template_test():
    from langchain_core.prompts import ChatPromptTemplate

    template = ChatPromptTemplate(
        [
            ("system", "당신은 뉴스요약 전문가입니다."),
            ("human", "제목 : {title}\n내용: {content}\n 주어진 뉴스를 요약해주세요."),
        ]
    )

    messages = template.format_messages(
        title="구글이 Gemini3.0을 출시했다.", content="블라블라"
    )

    model = init_chat_model("gemini-2.5-flash-lite", model_provider="google_genai")
    result = model.invoke(messages)

    print(result)

    chain = template | model
    result = chain.invoke(
        {"title": "구글이 Gemini3.0을 출시했다.", "content": "블라블라"}
    )

    """
    [ SystemMessage(content='당신은 뉴스요약 전문가입니다.'),
      HumanMessage(content='제목 : 구글이 Gemini3.0을 출시했다.\n내용: 블라블라\n 주어진 뉴스를 요약해주세요.')]
    """


def templte_with_lcel():
    from langchain_core.prompts import ChatPromptTemplate

    model = init_chat_model("gemini-2.5-flash-lite", model_provider="google_genai")
    prompt = ChatPromptTemplate(
        [
            (
                "system",
                "당신은 뉴스 요약 전문가 입니다. 100자 이내로 내용을 요약해주세요.",
            ),
            ("human", "다음의 뉴스를 요약하세요.\n제목 : {title}\n내용: {content}"),
        ]
    )

    chain = prompt | model
    result = chain.invoke(
        {
            "title": "ChatGPT 아틀라스 웹브라우저 출시",
            "content": "ChatGPT가 결합된 웹에서 즉각적 답변, 더 스마트한 제안, 작업 지원과 함께 완벽하게 제어할 수 있는 개인정보 보호 설정을 경험하세요.",
        }
    )

    print(result.content)


if __name__ == "__main__":
    templte_with_lcel()
