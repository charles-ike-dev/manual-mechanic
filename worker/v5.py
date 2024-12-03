import os
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from UI_loader import UIDocumentLoader
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm import tqdm
from langchain_unstructured import UnstructuredLoader
from utils import flatten_dict
import unicodedata
import logging

DIR_PATH = "../docs/v19"
PROCESSED_DIR_PATH = DIR_PATH + "/processed"
NAMESPACE = "v19"

load_dotenv(override=True)  # Take environment variables from .env.

# Set the environment variable to suppress OpenAI logs
os.environ["OPENAI_LOG_LEVEL"] = "WARNING"

# Ensure the processed directory exists
os.makedirs(PROCESSED_DIR_PATH, exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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
        # Add filename to metadata
        doc.metadata["filename"] = ascii_file_name

    # Use the ASCII filename as the document ID
    vectorstore.add_documents(documents=docs, ids=[ascii_file_name])


def process_txt(file_name, file_path, vectorstore):
    loader = TextLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    # Convert filename to ASCII
    ascii_file_name = to_ascii(file_name)
    for doc in docs:
        doc.metadata["filename"] = ascii_file_name
    # Generate ASCII IDs
    ids = [f"{ascii_file_name}_{i}" for i in range(len(docs))]
    vectorstore.add_documents(documents=docs, ids=ids)


def process_pdf(file_name, file_path, vectorstore):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    ascii_file_name = to_ascii(file_name)
    for doc in docs:
        doc.metadata["filename"] = ascii_file_name
    # Generate ASCII IDs
    ids = [f"{ascii_file_name}_{i}" for i in range(len(docs))]
    vectorstore.add_documents(documents=docs, ids=ids)


def process_file(file_name, file_path, vectorstore):
    loader = UnstructuredLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    for doc in docs:
        # Remove text_as_html from metadata
        doc.metadata.pop("text_as_html", None)
        doc.metadata = flatten_dict(doc.metadata)
    # Convert filename to ASCII
    ascii_file_name = to_ascii(file_name)
    # Generate ASCII IDs
    ids = [f"{ascii_file_name}_{i}" for i in range(len(docs))]
    vectorstore.add_documents(documents=docs, ids=ids)


all_files = get_all_files(DIR_PATH)

skipped_files_extensions = [
    ".png", ".ds_store", ".svg", ".jpeg", ".jpg", ".gif", ".zip", ".gz"
]

for file_name, file_path in tqdm(all_files):
    try:
        if file_path.startswith(PROCESSED_DIR_PATH):
            continue
        logging.info(f"Processing file: {file_name}")
        if file_name.endswith(".xml"):
            process_xml(file_name, file_path, vectorstore)
        elif file_name.endswith(".txt"):
            process_txt(file_name, file_path, vectorstore)
        elif file_name.endswith(".pdf"):
            process_pdf(file_name, file_path, vectorstore)
        elif file_name.lower().endswith(tuple(skipped_files_extensions)):
            # Use tqdm.write() to avoid interfering with the progress bar
            tqdm.write(f"Skipping file: {file_name}")
            continue
        else:
            process_file(file_name, file_path, vectorstore)

        # Move the file after successful processing
        dest_path = os.path.join(PROCESSED_DIR_PATH, file_name)
        shutil.move(file_path, dest_path)
        logging.info(f"Processed and moved file: {file_name}")

    except Exception as e:
        # Log the error to the error log file with traceback
        logging.error(f"Error processing file {
                      file_name}: {str(e)}", exc_info=True)
        continue

logging.info("Processing complete.")
