import asyncio
import os
import pprint
from agents import Agent, Runner, tool
from agents.extensions.models.litellm_model import LitellmModel

# ------------------------------------------------------------------------------
# 3단계: 모니터링 및 디버깅 (Monitoring and Debugging)
#
# 에이전트가 어떤 생각을 하고(Reasoning), 어떤 도구를 호출하는지 내부 과정을
# 지켜보는 것은 디버깅과 성능 튜닝에 매우 중요합니다.
# Runner는 `monitor` 콜백을 통해 이벤트 로그를 제공합니다.
# ------------------------------------------------------------------------------

@tool
def get_stock_price(symbol: str) -> str:
    """주식 종목 코드를 입력받아 현재 주가를 반환합니다."""
    # 시뮬레이션 데이터
    prices = {"AAPL": "$150", "GOOGL": "$2800", "TSLA": "$700"}
    return prices.get(symbol.upper(), "알 수 없는 종목입니다.")

def monitor_callback(event):
    """
    Runner에서 발생하는 이벤트를 가로채서 출력하는 콜백 함수입니다.
    """
    print(f"\n[Monitor] Event Type: {type(event).__name__}")
    # 이벤트 객체의 속성을 딕셔너리로 변환하여 출력 (가독성을 위해 pprint 사용)
    # 실제로는 로그 파일에 저장하거나 대시보드로 전송할 수 있습니다.
    # pprint.pprint(event.__dict__, width=80)
    
    # 예: 모델 입력/출력 확인
    if hasattr(event, 'model_input'):
         print(f"  -> Model Input (Length): {len(str(event.model_input))}")
    if hasattr(event, 'model_output'):
         print(f"  -> Model Output: {event.model_output}")
    if hasattr(event, 'tool_name'):
         print(f"  -> Tool Call: {event.tool_name} with args {event.tool_args}")
    if hasattr(event, 'tool_output'):
         print(f"  -> Tool Output: {event.tool_output}")

async def main():
    if "GEMINI_API_KEY" not in os.environ:
        print("오류: GEMINI_API_KEY 환경 변수가 필요합니다.")
        return

    model = LitellmModel(model="gemini/gemini-1.5-flash")

    agent = Agent(
        name="StockBroker",
        model=model,
        tools=[get_stock_price],
        instructions="주식 가격을 알려주는 에이전트입니다. (한국어로 답변)"
    )

    print("--- 모니터링 기능이 활성화된 에이전트 실행 ---")
    
    # monitor 파라미터에 콜백 함수를 전달합니다.
    await Runner.run(
        agent, 
        input_text="애플(AAPL)과 구글(GOOGL)의 주가는 얼마인가요?", 
        monitor=monitor_callback
    )

if __name__ == "__main__":
    asyncio.run(main())
