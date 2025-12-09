# AI 에이전트 개발 마스터 클래스: OpenAI Agents SDK (Python)

안녕하세요! 이번 강의에서는 **OpenAI**의 새로운 오픈소스 프레임워크인 **Agents SDK**를 사용하여 AI 에이전트를 개발하는 방법을 배웁니다. 이 프레임워크는 OpenAI의 실험적 프로젝트였던 **Swarm**을 계승하여 더욱 안정적이고 확장 가능한 형태로 발전했습니다.

이번 강의의 특별한 점은 **OpenAI의 SDK를 사용하면서도, 모델은 Google의 Gemini를 연동**하여(LiteLLM 활용) 실습한다는 점입니다. 이를 통해 SDK의 유연성과 Gemini의 강력한 성능을 동시에 경험할 수 있습니다.

## 1. 이론: Agents SDK란 무엇인가?

### 1.1 개요
Agents SDK는 개발자가 신뢰할 수 있고 확장 가능한 AI 에이전트를 쉽게 구축할 수 있도록 돕는 Python 라이브러리입니다. 가볍고 사용하기 쉬운 구조로 설계되었으며, 에이전트 간의 협업(Multi-Agent)을 위한 기능들을 기본적으로 제공합니다.

### 1.2 주요 특징
*   **에이전트(Agents)**: 지침(Instructions)과 도구(Tools)를 가진 LLM 래퍼입니다.
*   **핸드오프(Handoffs)**: 에이전트가 다른 에이전트에게 제어권을 넘겨주며 복잡한 작업을 분담합니다.
*   **유연한 모델 연동**: 기본적으로 OpenAI 모델에 최적화되어 있지만, LiteLLM 등을 통해 Gemini, Claude 등 다양한 모델을 연결할 수 있습니다.
*   **관측 가능성(Observability) & 가드레일(Guardrails)**: 에이전트의 실행 과정을 추적하고, 입력/출력을 검증하는 기능을 제공합니다.

### 1.3 참고 자료
*   **공식 문서 및 코드**: [https://github.com/openai/openai-agents-python](https://github.com/openai/openai-agents-python)
*   **설치 가이드**: `pip install openai-agents` (본 강의에서는 LiteLLM도 함께 사용합니다)

---

## 2. 준비: 환경 설정

실습을 시작하기 전에 필요한 패키지를 설치하고 API 키를 설정해야 합니다.

### 2.1 설치
터미널에서 다음 명령어를 실행하세요.
```bash
pip install openai-agents litellm termcolor
```

### 2.2 API 키 설정
Gemini 모델을 사용하기 위해 환경 변수를 설정합니다. (`.env` 파일 또는 터미널 export)
```bash
export GEMINI_API_KEY="여러분의_API_키"
```

---

## 3. 실습: 단계별 에이전트 구축

우리는 총 5단계로 나누어 에이전트를 발전시켜 나갈 것입니다.

### Step 1: 기본 에이전트 (Hello World)
가장 기본적인 형태의 에이전트입니다. 모델을 연결하고 간단한 지시사항을 부여합니다.
*   **파일**: `01_basic_agent.py`
*   **핵심**: `Agent` 클래스, `Runner` 실행, `model` 설정.
*   **실행**: `python 01_basic_agent.py`

### Step 2: 도구를 사용하는 에이전트 (Tools)
에이전트에게 '날씨 검색' 같은 도구를 쥐어줍니다. LLM은 실시간 정보에 약하지만, 도구를 사용하면 정확해집니다.
*   **파일**: `02_tools_agent.py`
*   **핵심**: Python 함수(`get_weather`) 정의, `tools=[func]` 파라미터 전달.
*   **실행**: `python 02_tools_agent.py`

### Step 3: 에이전트 모니터링 (Monitoring)
에이전트가 무슨 생각을 하고 어떤 도구를 왜 썼는지 '로그'를 통해 확인합니다.
*   **파일**: `03_agent_monitoring.py`
*   **핵심**: `monitor_callback` 함수 구현, `Runner.run(..., monitor=monitor_callback)`.
*   **실행**: `python 03_agent_monitoring.py`
*   **포인트**: 에이전트의 추론 과정(Reasoning)이 출력되는 것을 확인하세요.

### Step 4: 대화형 에이전트 (Interactive Chat)
단발성 실행이 아니라, 문맥(Context)을 기억하며 사용자와 대화하는 챗봇입니다.
*   **파일**: `04_interactive_agent.py`
*   **핵심**: `messages` 리스트 관리 (대화 기록 누적), 무한 루프(`while True`).
*   **실행**: `python 04_interactive_agent.py`

### Step 5: 멀티 에이전트 협업 (Handoff)
한 명의 에이전트가 모든 걸 다 할 수는 없습니다. 전문 분야가 다른 에이전트끼리 작업을 넘기는 방법입니다.
*   **파일**: `05_multi_agent_handoff.py`
*   **핵심**: `handoffs` 파라미터. `TriageBot`(분류 담당)이 `EnglishExpert`나 `SpanishExpert`로 제어권을 이양합니다.
*   **실행**: `python 05_multi_agent_handoff.py`

---

## 4. 심화: 더 알아보기

실습을 마쳤다면 다음 주제들을 탐구해 보세요.

1.  **다른 모델 사용해보기**: `LitellmModel` 설정에서 `gpt-4o`나 `claude-3-5-sonnet` 등으로 모델 문자열만 바꾸면 어떻게 동작하는지 비교해 보세요.
2.  **복잡한 도구 연동**: 단순 문자열 처리 함수가 아니라, 실제 날씨 API나 주식 정보 API를 연동하여 실시간 정보를 가져오는 에이전트를 만들어 보세요.
3.  **상태 관리 (State Management)**: 대화가 길어질 때 토큰 제한을 관리하거나, 데이터베이스에 대화 내용을 저장하는 방법을 고민해 보세요.
4.  **프롬프트 엔지니어링**: `instructions`를 어떻게 작성하느냐에 따라 에이전트의 성능이 크게 달라집니다. 더 정교한 지시사항(Persona, Constraints)을 작성해 보세요.

---
이제 직접 코드를 실행하며 AI 에이전트의 세계를 경험해 봅시다!
