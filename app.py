import gradio as gr
from query import ask, build_vector_store


build_vector_store()


def handle_query(question):
    result = ask(question)
    sources = "\n".join(f"• {source}" for source in result["sources"])
    return result["answer"], sources


with gr.Blocks() as demo:
    gr.Markdown("# The Unofficial Guide to City Tech Professors")
    gr.Markdown("Ask a question about professor reviews. Answers are based only on the collected documents.")

    question = gr.Textbox(label="Your question")
    ask_button = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=5)

    ask_button.click(handle_query, inputs=question, outputs=[answer, sources])
    question.submit(handle_query, inputs=question, outputs=[answer, sources])


demo.launch()