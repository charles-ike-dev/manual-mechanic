from typing import AsyncIterator, Iterator

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

    # <-- Does not take any arguments
    def lazy_load(self) -> Iterator[Document]:
        """A lazy loader that reads a file line by line.

        When you're implementing lazy load methods, you should use a generator
        to yield documents one by one.
        """

        # Parse the XML file
        root = ET.parse(self.file_path).getroot()

        # Helper function to extract text
        def get_text(element, tag):
            try:
                return element.find(tag).text
            except AttributeError:
                return None

        # Helper function to extract attributes
        def get_attributes(element, attributes):
            return {attr: element.get(attr) for attr in attributes}

        # Function to parse Instructions
        def parse_instructions(instructions_element):
            instructions = []
            for instruction in instructions_element.findall('Instruction'):
                instruction_data = {
                    "internalid": instruction.get("internalid"),
                    "number": instruction.get("number"),
                    "text": get_text(instruction, "Text"),
                    "notes": [get_text(note, "Text") for note in instruction.findall("Note")],
                    "images": []
                }
                for image in instruction.findall(".//Image_Config"):
                    instruction_data["images"].append(get_attributes(
                        image, ["fileref", "internalid", "internalref", "pageheight", "pagewidth", "number", "original-pagewidth", "name"]))
                instructions.append(instruction_data)
            return instructions

        # Function to parse Illustrations
        def parse_illustrations(root):
            illustrations = []
            for illustration in root.findall('Illustration'):
                for config in illustration.findall('Illustration_Config'):
                    illustration_data = {
                        "images": [],
                        "lists": []
                    }
                    for image in config.findall(".//Image_Config"):
                        illustration_data["images"].append(get_attributes(
                            image, ["fileref", "internalid", "internalref", "pageheight", "pagewidth", "number", "original-pagewidth", "name"]))
                    for list_item in config.findall(".//ListItem"):
                        illustration_data["lists"].append({
                            "label": list_item.get("label"),
                            "text": get_text(list_item.find("Para").find("ParaCfg"), "Text")
                        })
                    illustrations.append(illustration_data)
            return illustrations

        # Extracting the relevant data
        service_iu_data = {
            "confmig": root.get("conmig"),
            "ifsid": root.get("ifsid"),
            "iuid": root.get("iuid"),
            "miuid": root.get("miuid"),
            "configlength": root.get("configlength"),
            "iupublished": root.get("iupublished"),
            "IceCode": root.get("IceCode"),
            "Version": root.get("Version"),
            "LastDateModif": root.get("LastDateModif"),
            "ValidationDate": root.get("ValidationDate"),
            "title": get_text(root.find("Title"), "Text"),
            "instructions": parse_instructions(root.find("Instructions")),
            "illustrations": parse_illustrations(root),
            "model": {
                "name": get_text(root.find("ICE_Model"), "Model_Name"),
                "market_config": get_text(root.find("ICE_Model"), "Market_Config")
            }
        }

        #  Convert service_iu_data to a compact string
        str_service_iu_data = json.dumps(
            service_iu_data, separators=(',', ':'))

        yield Document(
            page_content=str_service_iu_data,
            metadata=service_iu_data,
        )
