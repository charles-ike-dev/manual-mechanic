import os
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings


load_dotenv(override=True)  # take environment variables from .env.

DIR_PATH = "../docs/zero"
NAMESPACE = "zero"

index_name = os.getenv("PINECONE_INDEX")


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


all_files = get_all_files(DIR_PATH)
for file_name, file_path in all_files:
    try:
        print(f"Processing file: {file_name}")
        loader = UnstructuredFileLoader(file_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

        vectorstore = PineconeVectorStore(
            index_name=index_name, embedding=embeddings, namespace=NAMESPACE)
        vectorstore.add_documents(docs)
    except Exception as e:
        print(f"Error processing file {file_name}: {e}")
        continue
