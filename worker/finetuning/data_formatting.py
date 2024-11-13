import json
import os

# Define the file paths
input_file = './augmented_dataset_20241108_155339.json'
output_file = os.path.splitext(input_file)[0] + '_output.jsonl'

# Load the content of the input file
with open(input_file, 'r') as f:
    data = json.load(f)

# Process each entry and write to a .jsonl file
with open(output_file, 'w') as f_out:
    for item in data:
        # First write the original question-answer pair
        formatted_entry = {
            "messages": [
                {"role": "user", "content": item["question"]},
                {"role": "assistant", "content": item["answer"]}
            ]
        }
        f_out.write(json.dumps(formatted_entry) + '\n')

        # Then write each similar question with the same answer
        for similar_question in item["similar_questions"]:
            formatted_entry = {
                "messages": [
                    {"role": "user", "content": similar_question},
                    {"role": "assistant", "content": item["answer"]}
                ]
            }
            f_out.write(json.dumps(formatted_entry) + '\n')

print("Data has been formatted and saved to", output_file)
