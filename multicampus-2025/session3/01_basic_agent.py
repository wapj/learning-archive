import asyncio
import os
from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

# ------------------------------------------------------------------------------
# 1단계: Gemini를 이용한 기본 에이전트 (Basic Agent using Gemini)
#
# 이 예제는 LiteLLM 확장을 통해 Google의 Gemini 모델을 사용하는 간단한 에이전트를
# 생성하는 방법을 보여줍니다.
#
# 사전 준비사항 (Prerequisites):
# - 패키지 설치: pip install google-agents litellm termcolor
# - Google Gemini API Key 발급
# ------------------------------------------------------------------------------

async def main():
    # 1. API 키 설정 (Setup API Key)
    # 환경 변수에 설정하는 것이 가장 좋습니다: export GEMINI_API_KEY="AIza..."
    if "GEMINI_API_KEY" not in os.environ:
        print("오류: GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("다음 명령어로 설정해주세요: export GEMINI_API_KEY='your_api_key'")
        return

    # 2. 모델 구성 (Configure the Model)
    # LiteLLMModel 래퍼를 사용하여 Gemini에 액세스합니다.
    # 모델 문자열은 보통 'provider/model-name' 형식을 따릅니다.
    # Gemini의 경우 LiteLLM은 'gemini/gemini-pro' 또는 'gemini/gemini-1.5-flash'를 사용합니다.
    model = LitellmModel(
        model="gemini/gemini-1.5-flash" 
    )

    # 3. 에이전트 정의 (Define the Agent)
    # 에이전트는 이름, 지침(시스템 프롬프트), 그리고 모델을 가집니다.
    agent = Agent(
        name="GeminiAssistant",
        instructions="당신은 Gemini로 구동되는 친절하고 예의 바른 AI 비서입니다. (한국어로 답변해주세요)",
        model=model,
    )

    # 4. 에이전트 실행 (Run the Agent)
    # Runner는 실행 루프(입력 -> 모델 -> 도구 호출 -> 모델 -> 출력)를 관리합니다.
    # Runner는 인스턴스화하지 않고 클래스 메서드로 사용됩니다.
    
    print(f"에이전트 실행 중: {agent.name}...")
    
    try:
        # 에이전트에게 간단한 사용자 메시지를 보냅니다.
        # runner는 최종 출력을 포함하는 RunResult 객체를 반환합니다.
        result = await Runner.run(agent, input_text="안녕하세요! 자기소개를 부탁하고 우주에 관한 재미있는 사실 하나만 알려주세요.")
        
        print("\n--- 에이전트 응답 (Agent Response) ---")
        print(result.final_output)
        print("-------------------------------------")
        
    except Exception as e:
        print(f"\n실행 중 오류 발생: {e}")
        # 힌트: API 키가 잘못되었거나 모델 이름이 틀린 경우 발생할 수 있습니다.

if __name__ == "__main__":
    asyncio.run(main())
