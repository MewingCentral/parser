import json

input_file = "data-artifacts/document.json"
output_file = "colab-notebook/formatted questions.json"

with open(input_file, "r") as f:
    data = json.load(f)

question_titles = []
question_id = 1

for section in data["sections"]:
    for question in section["questions"]:
        
        question_content = question["text"]
        formatted_prompt = {
            "question_id" : question_id,
            "question_content" : question_content
        }

        question_titles.append(formatted_prompt)
        question_id += 1

formatted_output = {
    "questions" : question_titles
}

with open(output_file, "w") as outfile:
    json.dump(formatted_output, outfile, indent=4)

print(f"Successfully wrote question titles to {output_file}")