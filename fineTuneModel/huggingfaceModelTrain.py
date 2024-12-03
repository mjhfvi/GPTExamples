# train huggingface model with dataset from huggingface
# Use a pipeline as a high-level helper
from __future__ import annotations

from datasets import load_dataset
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer
from transformers import pipeline
# Load model directly
# Load datasets

# Use a pipeline as a high-level helper
pipe = pipeline('text-generation', model='meta-llama/Llama-3.2-1B')

# Load model directly
tokenizer = AutoTokenizer.from_pretrained('meta-llama/Llama-3.2-1B')
model = AutoModelForCausalLM.from_pretrained('meta-llama/Llama-3.2-1B')

# Load datasets
ds = load_dataset('CyberNative/Code_Vulnerability_Security_DPO')

# Pushing model to your own account
model.push_to_hub('Llama-3.2-1B-Code_Vulnerability_Security_DPO')

# Pushing your tokenizer
tokenizer.push_to_hub('Llama-3.2-1B-Code_Vulnerability_Security_DPO')

# Pushing all things after training
trainer.push_to_hub()
