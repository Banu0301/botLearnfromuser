import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def find_closest_match(word: str, knowledge_base: dict) -> str:
    matches = get_close_matches(word, list(knowledge_base), n=1, cutoff=0.6)
    if matches:
        return matches[0]
    return None

def chat_bot():
    knowledge_base = load_knowledge_base('knowledge_base.json')
    print("Welcome to the Chatbot! Type 'exit' to quit.")

    while True:
        user_question = input("You: ")
        if user_question.lower() == 'exit':
            break

        questions_dict = {q["question"]: q["answer"] for q in knowledge_base["questions"]}
        best_match = find_closest_match(user_question, questions_dict)

        if best_match:
            answer = questions_dict[best_match]
            print(f"Chatbot: {answer}")
        else:
            print("Chatbot: I don't know the answer. Can you teach me?")
            new_answer = input("Type the answer or 'skip' to skip: ")
            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_question, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print("Chatbot: Thank you for teaching me!")

if __name__ == "__main__":
    chat_bot()
