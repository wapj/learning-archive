import asyncio
import os
import sys
from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

# ------------------------------------------------------------------------------
# 5단계: 멀티 에이전트 핸드오프 (Multi-Agent Handoff)
#
# 이 예제는 복잡한 작업을 여러 전문 에이전트가 협력하여 처리하는 방법을 보여줍니다.
# 하나의 에이전트가 처리할 수 없는 작업을 다른 에이전트에게 위임(Handoff)합니다.
# ------------------------------------------------------------------------------

# 1. 모델 구성
model = LitellmModel(
    model="gemini/gemini-1.5-flash"
)

# 2. 전문 에이전트 정의

# 영어 전문 에이전트
english_agent = Agent(
    name="EnglishExpert",
    model=model,
    instructions="당신은 영어 번역 전문가입니다. 주어진 텍스트를 자연스러운 영어로 번역하세요."
)

# 스페인어 전문 에이전트
spanish_agent = Agent(
    name="SpanishExpert",
    model=model,
    instructions="당신은 스페인어 번역 전문가입니다. 주어진 텍스트를 자연스러운 스페인어로 번역하세요."
)

# 3. 메인 라우팅 에이전트 (Triage Agent) 정의
# 이 에이전트는 사용자의 요청을 분석하여 적절한 전문 에이전트에게 전달(Handoff)합니다.
def transfer_to_english_expert():
    """영어로 번역이 필요할 때 영어 전문가에게 연결합니다."""
    return english_agent

def transfer_to_spanish_expert():
    """스페인어로 번역이 필요할 때 스페인어 전문가에게 연결합니다."""
    return spanish_agent

triage_agent = Agent(
    name="TriageBot",
    model=model,
    instructions="""당신은 고객 요청을 분류하는 봇입니다. 
    사용자가 '영어로 번역해줘'라고 하면 EnglishExpert에게 넘기세요.
    사용자가 '스페인어로 번역해줘'라고 하면 SpanishExpert에게 넘기세요.
    그 외의 일반적인 질문에는 직접 대답하세요. (한국어로)
    """,
    # 다른 에이전트로 전환하기 위한 함수를 'tools' 처럼 등록이 아닌, 'handoffs' 메커니즘을 사용합니다.
    # OpenAI Agents SDK 에서는 handoffs 리스트에 함수를 전달하여 제어를 넘길 수 있습니다.
    handoffs=[transfer_to_english_expert, transfer_to_spanish_expert]
)

# 4. 실행
async def main():
    print("--- 멀티 에이전트 핸드오프 데모 ---")
    if "GEMINI_API_KEY" not in os.environ:
        print("오류: GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")
        return

    # Case 1: 영어 번역 요청
    print("\n1. 사용자: '안녕하세요'를 영어로 번역해줘")
    result1 = await Runner.run(triage_agent, messages=[{"role": "user", "content": "'안녕하세요'를 영어로 번역해줘"}])
    print(f"결과: {result1.final_output}\n")
    
    # Case 2: 스페인어 번역 요청
    print("2. 사용자: '반갑습니다'를 스페인어로 번역해줘")
    # 새로운 실행을 위해 Runner.run을 다시 호출
    result2 = await Runner.run(triage_agent, messages=[{"role": "user", "content": "'반갑습니다'를 스페인어로 번역해줘"}])
    print(f"결과: {result2.final_output}\n")
    
    # Case 3: 일반 질문
    print("3. 사용자: 오늘 기분 어때?")
    result3 = await Runner.run(triage_agent, messages=[{"role": "user", "content": "오늘 기분 어때?"}])
    print(f"결과: {result3.final_output}\n")

if __name__ == "__main__":
    asyncio.run(main())
