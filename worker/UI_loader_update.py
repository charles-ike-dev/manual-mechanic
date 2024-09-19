from typing import AsyncIterator, Iterator, Dict

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

import xml.etree.ElementTree as ET
import json


class UIDocumentLoader(BaseLoader):
    """An example document loader that reads a file line by line."""

    def __init__(self, file_path: str) -> None:
        """Initialize the loader with a file path.

        Args:
            file_path: The path to the file to load.
        """
        self.file_path = file_path

    def lazy_load(self) -> Iterator[Document]:
        """A lazy loader that reads a file line by line.

        When you're implementing lazy load methods, you should use a generator
        to yield documents one by one.
        """

        # Parse the XML file
        root = ET.parse(self.file_path).getroot()

        # Helper function to recursively extract text from all elements
        def xml_to_dict(element) -> Dict:
            # Convert an XML element and its children into a dictionary
            node_dict = {}

            # Add attributes if present
            if element.attrib:
                node_dict['attributes'] = element.attrib

            # Add text if present
            if element.text and element.text.strip():
                node_dict['text'] = element.text.strip()

            # Recursively add child elements
            for child in element:
                child_dict = xml_to_dict(child)

                # If the tag already exists in the dictionary, we need to make it a list
                if child.tag in node_dict:
                    if isinstance(node_dict[child.tag], list):
                        node_dict[child.tag].append(child_dict)
                    else:
                        node_dict[child.tag] = [
                            node_dict[child.tag], child_dict]
                else:
                    node_dict[child.tag] = child_dict

            return node_dict

        # Extracting the relevant data
        service_iu_data = xml_to_dict(root)

        # Convert service_iu_data to a compact string
        str_service_iu_data = json.dumps(
            service_iu_data, separators=(',', ':'))

        yield Document(
            page_content=str_service_iu_data,
            metadata=service_iu_data,
        )
