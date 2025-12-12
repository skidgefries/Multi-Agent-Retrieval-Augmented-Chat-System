# agents/generator.py
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class Generator:
    def __init__(self, model_name='distilgpt2', device=None):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)


    def generate(self, question: str, contexts: list, max_new_tokens=128):
        # contexts: list of dicts with 'content' and 'score'
        prompt = "You are a helpful assistant. Use the sources to answer the question.\n\n"
        for i, c in enumerate(contexts):
            prompt += f"Source {i+1} (score={c['score']:.3f}): {c['content']}\n\n"
        prompt += f"Question: {question}\nAnswer:"
        inputs = self.tokenizer(prompt, return_tensors='pt', truncation=True, max_length=1024).to(self.device)
        with torch.no_grad():
            out = self.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
        text = self.tokenizer.decode(out[0], skip_special_tokens=True)
        # return portion after 'Answer:'
        return text.split('Answer:')[-1].strip()