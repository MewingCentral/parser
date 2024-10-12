#import subprocess

#subprocess.check_call(["pip", "install", "torch", "torch-xla", "transformers"])

#subprocess.check_call(["pip", "show", "torch-xla"])

import os
import torch

device = None

# check if TPU is available
# if 'COLAB_TPU_ADDR' in os.environ:
#     # if TPU is available, import necessary libraries, and configure device as TPU.
#     print(f"TPU is being used.")
#     import torch_xla
#     import torch_xla.core.xla_model as xm
#     device = xm.xla_device()

# check if GPU is available
if torch.cuda.is_available():
    # if GPU is available, configure device as GPU.
    print(f"GPU is being used.")
    print(f"GPU Device Name: {torch.cuda.get_device_name(0)}")
    device = torch.device("cuda")

# if neither TPU or GPU is available, use CPU.
else:
    print(f"CPU is being used.")
    device = torch.device("cpu")

# print the device configuration: TPU, GPU, or CPU.
print(f"Device configuration: {device}")

#get_ipython().run_line_magic('pip', 'install transformers')

import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# load the model and tokenizer
model_title = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_title)
model = AutoModelForSeq2SeqLM.from_pretrained(model_title)

formatted_questions = "formatted_questions.json"

# load the questions from the formatted_questions.json file.
with open(formatted_questions, "r") as file:
    question_content = json.load(file)


#print(f"First question entry: {question_content['questions'][0]}")

# print the first question to verify file is loaded properly.
#print(f"Question 1: ", question_content["questions"][0]["question_content"])

# generate prompt and id pairs for each question
question_prompt = [f"Generate a title for the following LeetCode question: {q['question_content']}" for q in question_content["questions"]]
question_id = [q["question_id"] for q in question_content["questions"]]

# tokenize the batch of input prompts
inputs = tokenizer(question_prompt, return_tensors="pt", padding=True, truncation=True, max_length= 250)

# generate titles for the entire batch using beam search
outputs = model.generate(**inputs, num_beams=5, max_length=15, early_stopping=True)

# decode the generated titles
generated_titles = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

# combine the above generated titles with the question ids from above to generate the output
output_data = [{"id" : question_id, "generated_title" : title} for question_id, title in zip(question_id, generated_titles)]

# print the generated question title names.
for item in output_data:
  print(f"question_id: {item['id']}, generated_title: {item['generated_title']}")

# save the generated titles to question_titles.json.
output_path = "question_titles.json"
with open(output_path, "w") as outfile:
    json.dump({"titles" : output_data}, outfile, indent=4)

print(f"Generated titles saved to '{output_path}'")

# verify the generated titles were produced successfully by loading the file.
with open(output_path, "r") as file:
  generated_titles = json.load(file)

for pair in generated_titles["titles"][:5]:
  print(f"Question ID: {pair['id']}, Generated Title: {pair['generated_title']}")
