import asyncio
import os
from agents import Agent, Runner, tool
from agents.extensions.models.litellm_model import LitellmModel

# ------------------------------------------------------------------------------
# 2단계: 도구를 사용하는 에이전트 (Agent with Tools) - 함수 호출 (Function Calling)
#
# 이 예제는 1단계에서 발전하여 에이전트가 호출할 수 있는 사용자 정의 도구(함수)를
# 추가하는 방법을 보여줍니다.
#
# 에이전트 동작 순서:
# 1. 사용자 질문 수신 ("서울 날씨 어때?").
# 2. `get_weather` 도구를 호출하기로 결정.
# 3. 도구 실행.
# 4. 도구의 출력을 사용하여 최종 응답 생성.
# ------------------------------------------------------------------------------

# @tool 데코레이터를 사용하여 도구를 정의합니다.
# 독스트링(docstring)과 타입 힌트(type hints)는 LLM을 위한 도구 정의를 생성하는 데
# 사용되므로 매우 중요합니다.
@tool
def get_weather(city: str) -> str:
    """
    주어진 도시의 현재 날씨를 가져옵니다.
    
    Args:
        city: 도시 이름 (예: "Seoul", "New York").
    """
    print(f"\n[Tool Execution] {city}의 날씨 정보를 가져오는 중...")
    # 실제 앱에서는 여기서 외부 날씨 API를 호출하게 됩니다.
    return f"{city}의 날씨는 맑음이며, 기온은 25도이고 가벼운 바람이 붑니다."

async def main():
    # 1. API 키 설정
    if "GEMINI_API_KEY" not in os.environ:
        print("오류: GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")
        return

    # 2. 모델 구성
    model = LitellmModel(
        model="gemini/gemini-1.5-flash"
    )

    # 3. 도구를 포함한 에이전트 정의
    # 도구 목록(list of tools)을 Agent 생성자에 전달합니다.
    agent = Agent(
        name="WeatherAssistant",
        instructions="당신은 유용한 비서입니다. 제공된 도구를 사용하여 날씨 질문에 답변하세요. (한국어로 답변해주세요)",
        model=model,
        tools=[get_weather],
    )

    print(f"에이전트 실행 중: {agent.name}, 사용 가능한 도구: {[t.name for t in agent.tools]}")

    # 4. 에이전트 실행
    try:
        # 러너(Runner)가 도구 실행 루프를 자동으로 처리합니다.
        result = await Runner.run(agent, input_text="안녕하세요, 서울의 날씨를 알려줄 수 있나요?")
        
        print("\n--- 에이전트 응답 (Agent Response) ---")
        print(result.final_output)
        print("-------------------------------------")
        
    except Exception as e:
        print(f"\n오류 발생: {e}")

if __name__ == "__main__":
    asyncio.run(main())
