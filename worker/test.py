from langchain_text_splitters import RecursiveCharacterTextSplitter
from UI_loader import UIDocumentLoader
import xml.etree.ElementTree as ET


# # loader = UIDocumentLoader("../docs/v1/IU_5000011779_1.xml")

# # get all the document in folder v1
# loader = UIDocumentLoader(
#     "../docs/full/eTIM/SM/Manuale completo/69269337_1_FULL.xml")

# documents = loader.load()
# # text_splitter = RecursiveCharacterTextSplitter(
# #     chunk_size=1000, chunk_overlap=0)
# # docs = text_splitter.split_documents(documents)

# for doc in documents:
#     print("doc", doc)
#     print()

root = ET.parse(
    "../docs/full/eTIM/SM/Manuale completo/69269337_1_FULL.xml")


print(root)
