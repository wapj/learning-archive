import asyncio
from datetime import datetime
import math
from dotenv import load_dotenv
from langchain.tools import tool

from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain.chat_models import init_chat_model
from langchain_tavily.tavily_search import TavilySearch

from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.types import Command


load_dotenv()


@tool
def calculate(expression: str) -> str:
    """
    수학 표현식을 계산합니다 ex) calculate("2 + 2"), calculate("10 * 3")
    """
    try:
        result = eval(expression, {"__builtins__": {}, "math": math})
        return f"계산 결과: {result}"
    except Exception as e:
        return f"에러 : {str(e)}"


web_search = TavilySearch(max_result=5)
TOOLS = [calculate, web_search]

model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")


def call_agent(message):
    response = agent.invoke({"messages": [HumanMessage(content=message)]})
    print(response["messages"][-1].content)


checkpointer = MemorySaver()

agent = create_agent(
    model,
    tools=TOOLS,
    system_prompt=f"오늘 시각은 {datetime.now().strftime('%Y%m%d_%H%M%S')} 입니다."
    "당신은 친절한 AI에이전트입니다. "
    "유저의 요청을 면밀히 파악하고 필요할 때 도구를 사용하세요."
    "답변은 항상 한국어로 하고, 단계별로 설명하세요.",
    checkpointer=checkpointer,
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "calculate": {"allowed_decisions": ["approve", "reject"]},
                "tavily_search": True,  # TavilySearch 는 이름을  tavily_search로 해야함
            },
            description_prefix="도구 실행은 승인이 필요합니다.",
        )
    ],
)

# 메모리를 유지하기 위한 채팅 스레드 ID 설정
config = {"configurable": {"thread_id": "andy-session-1"}}


async def chat_loop():
    print("AI 비서가 준비 되었습니다. (종료: q)")
    while True:
        user_input = input("\n질문 : ")
        if user_input.lower() == "q":
            break

        response = await agent.ainvoke({"messages": user_input}, config=config)
        if "__interrupt__" in response:
            print("인터럽트 발생!\n ")
            yes_or_no = input("승인 y | 거절 n : ")
            if yes_or_no == "y":
                response = await agent.ainvoke(
                    Command(resume={"decisions": [{"type": "approve"}]}), config=config
                )
                result = response["messages"][-1].content
                print("\nAI:", result)
            else:
                print("도구 실행이 취소되었습니다.")
                continue
        else:
            result = response["messages"][-1].content
            print(result)


if __name__ == "__main__":
    asyncio.run(chat_loop())
