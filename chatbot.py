from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter

# Load the OpenRouter API key from .env
load_dotenv()

# Initialize the model
llm = ChatOpenRouter(
    model="openrouter/free",
    temperature=0.7,
    max_tokens=500,
)

print("OpenRouter Chatbot is ready!")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ["exit", "quit"]:
        print("Bot: Goodbye!")
        break

    if not user_input:
        continue

    try:
        response = llm.invoke(user_input)
        print("Bot:", response.content)

    except Exception as e:
        print("Error:", e)