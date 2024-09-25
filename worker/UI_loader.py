from typing import AsyncIterator, Iterator

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

import xml.etree.ElementTree as ET
import json
from utils import flatten_dict


def get_all_tags(element):
    """Recursively collect all unique tags from the XML."""
    tags = set([element.tag])
    for child in element:
        tags.update(get_all_tags(child))
    return tags


def highlight_unprocessed_tags(root, processed_tags):
    """Highlight tags that are not processed."""
    all_tags = get_all_tags(root)
    unprocessed_tags = all_tags - processed_tags
    if unprocessed_tags:
        print("\033[91mUnprocessed Tags Found:\033[0m",
              ', '.join(unprocessed_tags))


def xml_to_dict(element):
    result = {}
    for child in element:
        if len(child) == 0:
            result[child.tag] = child.text
        else:
            result[child.tag] = xml_to_dict(child)
    return result


def extract_text(element):
    text_content = ''
    if element.text:
        text_content += element.text.strip() + ' '
    for child in element:
        text_content += extract_text(child)
        if child.tail:
            text_content += child.tail.strip() + ' '
    return text_content


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

        # Define processed tags
        processed_tags = set([
            'Title', 'Instructions', 'Instruction', 'Note', 'Image_Config',
            'Illustration', 'Illustration_Config', 'ListItem', 'Para', 'ParaCfg'
        ])

        # Highlight unprocessed tags
        highlight_unprocessed_tags(root, processed_tags)

        # Helper function to extract text
        def get_text(element, tag):
            try:
                text = element.find(tag).text
                return text if text is not None else ''  # Ensure a string is returned
            except AttributeError:
                return ''

        # Helper function to extract attributes
        def get_attributes(element, attributes=None):
            if attributes:
                return {attr: element.get(attr) for attr in attributes}
            else:
                return element.attrib

        # Function to parse Instructions
        def parse_instructions(instructions_element):
            instructions = []
            # check if instructions_element is not None
            if instructions_element is None:
                return instructions
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
            # Check if illustrations are not None
            if root.find('Illustration') is None:
                return illustrations
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

        service_iu_data = xml_to_dict(root)
        service_iu_data = flatten_dict(service_iu_data)

        # # Extracting the relevant data
        # service_iu_data = {
        #     "filename": self.file_path.split("/")[-1],
        #     "confmig": root.get("confmig", ""),
        #     "ifsid": root.get("ifsid", ""),
        #     "iuid": root.get("iuid", ""),
        #     "miuid": root.get("miuid", ""),
        #     "configlength": root.get("configlength", ""),
        #     "iupublished": root.get("iupublished", ""),
        #     "IceCode": root.get("IceCode", ""),
        #     "Version": root.get("Version", ""),
        #     "LastDateModif": root.get("LastDateModif", ""),
        #     "ValidationDate": root.get("ValidationDate", ""),
        #     "title": get_text(root.find("Title"), "Text"),
        #     "instructions": parse_instructions(root.find("Instructions")),
        #     "illustrations": parse_illustrations(root),
        #     "model_name": get_text(root.find("ICE_Model"), "Model_Name"),
        #     "market_config": get_text(root.find("ICE_Model"), "Market_Config"),
        # }

        #  Convert service_iu_data to a compact string
        # V1
        # page_content_v1 = json.dumps(
        #     service_iu_data, separators=(',', ':'))

        # V2: get the text of the document
        page_content_v2 = extract_text(root)

        yield Document(
            page_content=page_content_v2,
            metadata=service_iu_data,
        )
