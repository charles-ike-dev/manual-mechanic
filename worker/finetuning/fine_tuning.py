import openai
from dotenv import load_dotenv
import os
import time

load_dotenv(override=True)  # Take environment variables from .env.

openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

data_path = "./augmented_dataset_20241218_151657_output.jsonl"


# files = client.files.create(
#     file=open(data_path, "rb"),
#     purpose="fine-tune"
# )

files = client.files.list()
print(files)
for file in sorted(files, key=lambda x: x.created_at, reverse=False):
    print(file.created_at, file.id, file.filename, file.purpose, file.status)


# if data_path file is not uploaded, upload it
filename = os.path.basename(data_path)

if not files or not any(file.filename == filename for file in files):
    files = client.files.create(
        file=open(filename, "rb"),
        purpose="fine-tune"
    )
else:
    print("File already uploaded")
    file_id = next(file.id for file in files if file.filename == filename)

    # # if the
    # # Create a fine-tuning job
    # print("Creating fine-tuning job")
    # client.fine_tuning.jobs.create(
    #     training_file=file_id,
    #     model="gpt-4o-mini-2024-07-18"
    # )

    # # List 10 fine-tuning jobs
    # jobs = client.fine_tuning.jobs.list(limit=10)
    # print("List of fine-tuning jobs:")
    # for job in jobs:
    #     print(
    #         f"id: {job.id} \ttraining_file: {job.training_file}\tstatus: {job.status}")

    # # while the job with training_file = file_id is not finished, wait for it to finish and then retrieve the state of the fine-tuning job
    # job = next(job for job in jobs if job.training_file == file_id)
    # while job.status != "succeeded":
    #     print(
    #         f"id: {job.id} \ttraining_file: {job.training_file}\tstatus: {job.status}")
    #     time.sleep(10)
    #     job = client.fine_tuning.jobs.retrieve(job.id)

# print(job)


# # Retrieve the state of a fine-tune
state = client.fine_tuning.jobs.retrieve("ftjob-OtiiYJsZ15xs1iPkiQkpcpnU")
print("State of fine-tuning job:", state)
# # # Cancel a job
# client.fine_tuning.jobs.cancel("ftjob-FDrkroZurJcaJxFWucY7tyeL")

# # # List up to 10 events from a fine-tuning job
# # client.fine_tuning.jobs.list_events(
# #     fine_tuning_job_id="ftjob-abc123", limit=10)

# # # Delete a fine-tuned model (must be an owner of the org the model was created in)
# # client.models.delete("ft:gpt-3.5-turbo:acemeco:suffix:abc123")
