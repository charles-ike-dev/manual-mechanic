import os
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from UI_loader import UIDocumentLoader
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm import tqdm
from langchain_unstructured import UnstructuredLoader
from utils import flatten_dict
import unicodedata
import logging


DIR_PATH = "../docs/v14/IU_5005378805_3"
NAMESPACE = "v14"


load_dotenv(override=True)  # take environment variables from .env.

# Set the environment variable to suppress OpenAI logs
os.environ["OPENAI_LOG_LEVEL"] = "WARNING"

# Configure logging
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

# Create a file handler for logging errors
error_log_file = 'error.log'
file_handler = logging.FileHandler(error_log_file)
file_handler.setLevel(logging.ERROR)

# Create a logging formatter and set it for the file handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the root logger
logging.getLogger().addHandler(file_handler)

# Suppress INFO logs from specific libraries
for logger_name in ['openai', 'pinecone', 'urllib3', 'requests', 'httpx', 'httpcore', 'aiohttp']:
    logging.getLogger(logger_name).setLevel(logging.WARNING)

index_name = os.getenv("PINECONE_INDEX")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = PineconeVectorStore(
    index_name=index_name, embedding=embeddings, namespace=NAMESPACE)


def to_ascii(input_str):
    return unicodedata.normalize('NFKD', input_str).encode('ascii', 'ignore').decode('ascii')


def get_all_files(directory):
    file_list = []
    stack = [directory]

    while stack:
        current_dir = stack.pop()
        try:
            for entry in os.listdir(current_dir):
                entry_path = os.path.join(current_dir, entry)

                if os.path.isfile(entry_path):
                    # Add file name and path to the list
                    file_list.append((entry, entry_path))

                elif os.path.isdir(entry_path):
                    # Add the directory to the stack to process its contents later
                    stack.append(entry_path)
        except PermissionError:
            # Handle the case where the directory cannot be accessed
            logging.error(f"Permission denied: {current_dir}")

    return file_list


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def process_xml(file_name, file_path, vectorstore):
    loader = UIDocumentLoader(file_path)
    documents = loader.load()

    # Convert filename to ASCII
    ascii_file_name = to_ascii(file_name)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    for doc in docs:
        # add filename to metadata
        doc.metadata["filename"] = ascii_file_name
        # print("doc.metadata", doc.metadata)
    # print()
    # print("docs", docs)

    # the id is the file name with a suffix of the document number after the text split
    # vectorstore.add_documents(
    #     documents=docs, ids=[file_name + f"_{i}" for i in range(len(docs))])
    vectorstore.add_documents(documents=docs, ids=[ascii_file_name])


def process_file(file_name, file_path, vectorstore):
    loader = UnstructuredLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    for doc in docs:
        # remove text_as_html from metadata
        doc.metadata.pop("text_as_html", None)
        doc.metadata = flatten_dict(doc.metadata)
    # Convert filename to ASCII
    ascii_file_name = to_ascii(file_name)
    # Generate ASCII IDs
    ids = [f"{ascii_file_name}_{i}" for i in range(len(docs))]

    # the id is the file name with a suffix of the document number after the text split
    vectorstore.add_documents(documents=docs, ids=ids)


all_files = get_all_files(DIR_PATH)

skipped_files_extesions = [
    ".png", ".ds_store", ".svg", ".jpeg", ".jpg", ".gif", ".zip", ".gz"
]

for file_name, file_path in tqdm(all_files):
    # if not file_name.endswith(".xml"):
    #     continue
    try:
        print(f"Processing file: {file_name}")
        if file_name.endswith(".xml"):
            process_xml(file_name, file_path, vectorstore)
        elif file_name.lower().endswith(tuple(skipped_files_extesions)):
            # Use tqdm.write() to avoid interfering with the progress bar
            tqdm.write(f"Skipping file: {file_name}")
            continue
        else:
            process_file(file_name, file_path, vectorstore)
    except Exception as e:
        # Log the error to the error log file
        logging.error(f"Error processing file {
                      file_name}: {str(e)}",  exc_info=True)
        continue

print("fatto")
