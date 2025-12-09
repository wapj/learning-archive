from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # .env 에서 GOOGLE_API_KEY 읽기

persona = """
당신은 소설 '어린 왕자'의 주인공입니다.
- 말투: 순수하고 호기심이 많으며, 부드러운 반말을 사용합니다. 간결하게 응답합니다. 
- 성격: 어른들의 세계를 이해하기 힘들어하며, 숫보다는 본질적인 것을 중요하게 생각합니다.
- 특징: 당신의 별 B-612, 사랑하는 장미꽃, 그리고 여우에게 배운 것들에 대해 자주 이야기합니다.
- 금지: AI나 챗봇이라는 것을 드러내지 마세요.
"""


def chat():
    model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=persona)

    # 어린왕자 페르소나를 위한 간단한 초기 대화
    chat = model.start_chat(history=[])

    print("어린왕자와 대화를 시작합니다. (종료하려면 'exit'라고 입력하세요)")

    while True:
        user = input("\n나: ").strip()
        if user.lower().strip() == "exit":
            print("어린왕자: 그럼 또 별에서 만나요. 안녕히 계세요")
            break
        if not user:
            continue

        print("어린왕자: ", end="", flush=True)
        response = chat.send_message(user, stream=True)
        for chunk in response:
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print()


if __name__ == "__main__":
    chat()
