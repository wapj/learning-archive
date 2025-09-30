## 가상환경 설정

### 터미널 
```
pip -m venv .venv
uv init && uv venv
```

### VSCode 

VSCode의 `Python: Select Interpreter` 메뉴 사용

### 가상환경 활성화 

```
# 윈도우즈
. \.venv\Scripts\activate 

# 맥OS 또는 리눅스 
source .venv/bin/activate
```

## 의존성 설치 

```
# pip
pip install beautifulsoup4 dotenv httpx "langchain[google-genai]"

pip install -r requirements.txt

# uv
uv sync 
```
