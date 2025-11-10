from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


def main():
    model = genai.GenerativeModel("gemini-2.5-flash")
    result = model.generate_content("AI 에이전트가 뭔가요?", stream=True)

    for chunk in result:
        print(chunk.text, end="")


if __name__ == "__main__":
    main()
