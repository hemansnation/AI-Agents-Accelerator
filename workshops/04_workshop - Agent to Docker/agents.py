import os
import google.generativeai as genai
from ddgs import DDGS
from pathlib import Path

api_key = "your api key here"
genai.configure(api_key=api_key)

def calculator(expression: str) -> str:
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"


def web_search(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
            summary = "\n".join([f"{r['title']}: {r['body']}" for r in results])
            return summary if summary else "No results found."
    except Exception as e:
        return f"Error during web search: {e}"
    
def understand_image(image_path: str, prompt: str = "Explain and solve this homework question step by step. show all work clearly.") -> str:
    try:
        img = Path(image_path)
        if not img.exists():
            return "Error : Image not found. place your homeowork image in this folder and name it question.jpg, hoemwork.png, math.jpg, etc."
        image_part = {
            "mime_type": f"image/{img.suffix.lstrip('.') or 'jpeg'}",
            "data": img.read_bytes()
        }
        response = model.generate_content([prompt, image_part])
        return response.text
    except Exception as e:
        return f"Error understanding image: {e}"

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    tools=[calculator, web_search]
)

chat = model.start_chat(history=[])

def agent_response(user_input: str) -> str:
    possible_images = ["question.jpg", "homework.png", "math.jpg", "problem.jpeg", "img.png", "screenshot.png","photo.jpg"]
    attached_image = None
    for img_name in possible_images:
        if Path(img_name).exists():
            attached_image = img_name
            break
    
    if attached_image:
        print(f"Agent: Found image ({attached_image}) - analyzing now...")
        return understand_image(attached_image)

    response = chat.send_message(user_input)

    if response.candidates[0].content.parts and response.candidates[0].content.parts[0].function_call:
        func_call = response.candidates[0].content.parts[0].function_call
        func_name = func_call.name
        args = dict(func_call.args)
        tool_result = None

        if func_name == "calculator":
            tool_result = calculator(args['expression'])
        elif func_name == "web_search":
            tool_result = web_search(args['query'])
        
        if tool_result:
            final_response = chat.send_message(
                genai.protos.Part(
                    function_response=genai.protos.FunctionResponse(
                        name=func_name,
                        response={'result': tool_result}
                    )
                )
            )
            return final_response.text
    else:
        return response.text
    

if __name__ == "__main__":
    print("Student Super Agent! Text + Math + Web Search + Image Solver")

    print("Just drop your homeowkr photo in the folder!")

    print("Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        reply = agent_response(user_input)
        print(f"Agent: {reply}")