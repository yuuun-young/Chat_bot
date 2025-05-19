import gradio as gr
import openai
import os

# 직접 API 키 삽입 (보안 필요 시 환경변수 방식으로 교체 가능)
openai.api_key = "sk-proj-여기에_너의_프로젝트_키_입력"

def get_system_prompt(mode):
    if mode == "회계":
        return "너는 K-IFRS 기반 회계 전문가야. 단어나 문장을 정확하고 쉽게 설명해줘."
    else:
        return "너는 대한민국 세법에 정통한 세무사야. 법인세법, 소득세법, 부가가치세법 기준으로 설명해줘."

def chat(message, history, mode):
    messages = [{"role": "system", "content": get_system_prompt(mode)}]
    for user, bot in history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": bot})
    messages.append({"role": "user", "content": message})

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages
    )
    reply = response.choices[0].message.content
    history.append((message, reply))
    return history, history

with gr.Blocks() as demo:
    gr.Markdown("## 💬 GPT 회계·세무 메신저")
    mode = gr.Radio(["회계", "세무"], label="전문가 모드", value="회계")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="질문을 입력하고 Enter", placeholder="예: 감가상각이 뭐야?")
    clear = gr.Button("대화 초기화")
    state = gr.State([])

    msg.submit(chat, [msg, state, mode], [chatbot, state])
    clear.click(lambda: ([], []), None, [chatbot, state])

demo.launch()
