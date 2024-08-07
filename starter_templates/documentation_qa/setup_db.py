"""Set up the Vector DB for Documentation Question-Answering (Q&A) Bot"""
import re
from typing import Dict, List, Optional, Union
import uuid

import chromadb
from chromadb import config
import pydantic


# List of Markdown files with optional base URLs for citations
MARKDOWN_FILES = [
    # Each entry is a tuple containing:
    # 1. The path to the Markdown file
    # 2. An optional base URL for generating citation links (if applicable)

    ("sample.md", "https://docs.pydantic.dev/latest/concepts/models/"),

    # You can add more Markdown files below. For files without a citation URL,
    # just provide the file path as a string (without a tuple).
    # Example:
    # "path/to/another_file.md",

    # Example with a citation URL:
    # ("path/to/file_with_url.md","https://example.com/docs/file.html"),
]


COLLECTION_NAME = "markdown_collection"


chroma_client = chromadb.PersistentClient(
    settings=config.Settings(allow_reset=True))


class _Node(pydantic.BaseModel):
    """Container for a text chunk.
    
    Attributes:
        text: Text content of the node.
        id: Unique identifier for the node. If not provided, it is generated
            automatically.
        metadata: Arbitrary metadata associated with the node.
    """
    text: str
    id: str = pydantic.Field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Optional[Dict[str, Union[str, int, float]]] = None


def _split_markdown_by_header(text: str) -> List[str]:
    """Splits a Markdown text into sections based on headers.

    Divides a Markdown string into sections defined by headers, including the
    header and its following content up to the next header or text end.
    Headers within code blocks are ignored.
    
    Args:
        text: Markdown text to split.
    
    Returns:
        A list of strings, each containing a section of the input text.
    """
    chunks = []
    lines = text.split("\n")
    code_block = False
    current_section = ""

    for line in lines:
        if line.startswith("```"):
            code_block = not code_block
        header_match = re.match(r"^(#+) +(.*)", line)
        if header_match and not code_block:
            if current_section != "":
                chunks.append(current_section.strip())
            current_section = f"# {header_match.group(2)}\n"
        else:
            current_section += line + "\n"
    return chunks


def _get_nodes_from_file(
    file_path: str,
    base_url: Optional[str] = None) -> List[_Node]:
    """Extracts nodes from a Markdown file.

    Reads a Markdown file and splits it into nodes based on headers. Each node
    is assigned a unique ID.
    If a base URL is provided, it is combined with the header text to create a
    URL for the node. This URL is added to the node's metadata.
    
    Args:
        file_path: Path to the Markdown file.
        base_url: Base URL to use for generating node URLs.
    
    Returns:
        A list of Node objects, each containing a section of the input text.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = _split_markdown_by_header(text)

    nodes = []
    for chunk in chunks:
        if base_url is not None:
            first_line = chunk.split("\n", 1)[0]
            if first_line.startswith("# "):
                url = f"{base_url}#{'-'.join(first_line[2:].lower().split())}"
            else:
                url = base_url
            nodes.append(_Node(text=chunk, metadata={"url": url}))
        else:
            nodes.append(_Node(text=chunk))
    return nodes


def _create_collection() -> chromadb.Collection:
    """Creates a collection from a Markdown file.
    
    Resets the Chroma client and creates a new collection with a name defined
    by the COLLECTION_NAME constant.

    Reads the markdown files, defined by the MARKDOWN_FILES list, chunking the
    text based on headers to create nodes, which are added to the collection.
    Each node contains:
    - The text content of the chunk.
    - A unique ID.
    - A URL that is associated with the node, stored in the node's metadata.

    Returns:
        The created collection.
    """
    chroma_client.reset()
    collection = chroma_client.create_collection(name=COLLECTION_NAME)

    nodes = []
    node_text = set()
    for entry in MARKDOWN_FILES:
        if isinstance(entry, tuple):
            file_path, base_url = entry
        else:
            file_path, base_url = entry, None
        nodes_from_file = _get_nodes_from_file(file_path, base_url)
        for node in nodes_from_file:
            if node.text in node_text:
                print(f"Duplicate node found:\n{node.text}")
                print("Skipping duplicate node.")
                continue
            node_text.add(node.text)
            nodes.append(node)

    documents, ids, metadatas = (
        map(list,
            zip(*[(node.text, node.id, node.metadata) for node in nodes])))
    collection.add(documents=documents, ids=ids, metadatas=metadatas)

    return collection


if __name__ == "__main__":
    _create_collection()
