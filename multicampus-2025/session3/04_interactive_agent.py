import asyncio
import os
import sys
from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

# ------------------------------------------------------------------------------
# 4단계: 대화형 에이전트 (Interactive Agent)
#
# 이 예제는 사용자와 지속적으로 대화할 수 있는 CLI 챗봇을 만드는 방법을 보여줍니다.
# 대화 기록(History)을 관리하여 문맥을 유지하는 방법을 다룹니다.
# ------------------------------------------------------------------------------

# 1. 모델 구성
model = LitellmModel(
    model="gemini/gemini-1.5-flash"
)

# 2. 에이전트 정의
chat_agent = Agent(
    name="ChatBuddy",
    model=model,
    instructions="당신은 친절한 대화 친구입니다. 답변을 간결하고 매력적으로 해주세요. (한국어로 답변)"
)

# 3. 대화형 루프 (Interactive Loop)
async def main():
    print("--- 대화형 챗 에이전트 ('exit'를 입력하여 종료) ---")
    
    if "GEMINI_API_KEY" not in os.environ:
        print("오류: GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")
        return

    # 대화 기록을 저장할 리스트입니다.
    # 문맥을 유지하기 위해 이전 메시지들을 계속 누적해서 전달해야 합니다.
    messages = []
    
    while True:
        try:
            user_input = input("\n나(User): ")
            if user_input.lower() in ["exit", "quit", "종료"]:
                print("안녕히 가세요!")
                break
            
            # 사용자 메시지를 기록에 추가
            # SDK는 보통 메시지 형식을 따릅니다 (role, content).
            messages.append({"role": "user", "content": user_input})
            
            # 에이전트 실행 (대화 기록 포함)
            # messages 인자를 통해 지금까지의 대화 맥락을 에이전트에게 전달합니다.
            result = await Runner.run(chat_agent, messages=messages)
            
            # 결과 출력
            print(f"에이전트(Agent): {result.final_output}")
            
            # 에이전트의 응답을 기록에 추가하여 다음 턴에 문맥으로 사용
            messages.append({"role": "assistant", "content": result.final_output})
            
        except KeyboardInterrupt:
            print("\n종료합니다!")
            break
        except Exception as e:
            print(f"오류 발생: {e}")
            break

if __name__ == "__main__":
    asyncio.run(main())
