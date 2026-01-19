from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
torch.set_num_threads(4)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,
    low_cpu_mem_usage=True
)
model.eval()

def generate_answer(user_question, chat_history):
    """
    chat_history: list of (user, assistant) tuples
    """
    prompt = ""
    for user, assistant in chat_history[-3:]:
        prompt += f"<|user|>\n{user}\n<|assistant|>\n{assistant}\n"

    prompt += f"<|user|>\n{user_question}\n<|assistant|>"

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=300,
            do_sample=False,
            use_cache=True
        )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.split("<|assistant|>")[-1].strip()
