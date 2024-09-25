import os
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from UI_loader import UIDocumentLoader
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm import tqdm
import time
from langchain_unstructured import UnstructuredLoader
from utils import flatten_dict

load_dotenv(override=True)  # take environment variables from .env.

DIR_PATH = "../docs/full"
NAMESPACE = "v5"

index_name = os.getenv("PINECONE_INDEX")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = PineconeVectorStore(
    index_name=index_name, embedding=embeddings, namespace=NAMESPACE)


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
            print(f"Permission denied: {current_dir}")

    return file_list


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def process_xml(file_name, file_path, vectorstore):
    loader = UIDocumentLoader(file_path)
    documents = loader.load()
    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=1000, chunk_overlap=0)
    # docs = text_splitter.split_documents(documents)
    # print()
    # print("docs", docs)

    # the id is the file name with a suffix of the document number after the text split
    # vectorstore.add_documents(
    #     documents=docs, ids=[file_name + f"_{i}" for i in range(len(docs))])
    vectorstore.add_documents(documents=documents, ids=[file_name])


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

    # the id is the file name with a suffix of the document number after the text split
    vectorstore.add_documents(
        documents=docs, ids=[file_name + f"_{i}" for i in range(len(docs))])


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
            # process_xml(file_name, file_path, vectorstore)
            continue
        elif file_name.lower().endswith(tuple(skipped_files_extesions)):
            print("Skipping file")
            continue
        else:
            process_file(file_name, file_path, vectorstore)
    except Exception as e:
        print(f"Error processing file {file_name}: {e}")
        continue

print("fatto")
