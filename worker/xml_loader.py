import xml.etree.ElementTree as ET

from langchain.document_loaders.base import BaseLoader
from langchain.docstore.document import Document


class XMLLoader(BaseLoader):
    def __init__(self, file_path: str, base_path: str, encoding: str = "utf-8"):
        self.file_path = file_path
        self.base_path = base_path
        self.encoding = encoding

    def load(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        extension = '.xml'

        for elem in root.iter():
            link = elem.get('LINK')
            if link is not None:
                # Modify the link
                arr = link.rsplit('\\')
                arr.reverse()
                arr.pop()
                arr.append(arr.pop(0))
                path = '\\'.join(arr)
                new_link = self.base_path + path + extension
                elem.set('LINK', new_link)

        return self._parse_element(root)

    def _parse_element(self, root):
        content = ""

        for elem in root.iter():
            content += f"Element: {elem.tag}\n"
            for key, value in elem.attrib.items():
                content += f"Attribute - {key}: {value}\n"
            if elem.text:
                content += f"Text: {elem.text}\n"

        metadata = {"source": self.file_path}

        return Document(page_content=content, metadata=metadata)
