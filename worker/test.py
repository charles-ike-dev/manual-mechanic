from langchain_text_splitters import RecursiveCharacterTextSplitter
from UI_loader import UIDocumentLoader


# loader = UIDocumentLoader("../docs/v1/IU_5000011779_1.xml")

# get all the document in folder v1
loader = UIDocumentLoader("../docs/v1/IU_5000010570_2.xml")

documents = loader.load()
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1000, chunk_overlap=0)
# docs = text_splitter.split_documents(documents)

for doc in documents:
    print("doc", doc)
    print()
