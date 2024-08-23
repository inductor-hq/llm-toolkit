"""Set up the MongoDB Atlas DB for Documentation Question-Answering (Q&A) Bot"""
import os
import re
from typing import Any, Dict, List, Optional, TypeVar, Union
import uuid

import pydantic
import pymongo
from pymongo import operations
import sentence_transformers


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

MONGO_CLIENT_URI = os.environ.get("MONGO_CLIENT_URI")
if MONGO_CLIENT_URI is None:
    raise ValueError(
        "MONGO_CLIENT_URI environment variable is required to be set. "
        "Please see the README for instructions on how to set up the "
        "MongoDB Atlas cluster and obtain the connection URI.")
mongodb_client = pymongo.MongoClient(MONGO_CLIENT_URI)
documentation_collection = mongodb_client[
        "inductor_starter_templates"]["documentation_qa"]
embedding_model = sentence_transformers.SentenceTransformer("all-MiniLM-L6-v2")


_T_Node = TypeVar("_T_Node", bound="_Node")  # pylint: disable=invalid-name


class _Node(pydantic.BaseModel):
    """Container for a text chunk.
    
    Attributes:
        text: Text content of the node.
        text_embedding: Embedding of the text content.
        id: Unique identifier for the node. If not provided, it is generated
            automatically.
        metadata: Arbitrary metadata associated with the node.
    """
    text: str
    text_embedding: List[float]
    id: str = pydantic.Field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Optional[Dict[str, Union[str, int, float]]] = None

    @pydantic.model_validator(mode="before")
    @classmethod
    def _create_embedding(
        cls: _T_Node, data: Any) -> Any:
        """Creates an embedding for the text content if not provided."""
        if isinstance(data, dict):
            if "text" in data and "text_embedding" not in data:
                data["text_embedding"] = embedding_model.encode(
                    data["text"]).tolist()
        return data


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


def _create_search_index():
    """Creates a MongoDB Atlas Search Index for Vector Search.
    
    If the index already exists, updates the existing index with the latest
    definition.
    """
    index_name = "text_embedding_vector_search"
    search_index_model = pymongo.operations.SearchIndexModel(
        definition={
            "fields": [
                {
                    "type": "vector",
                    "numDimensions": 384,
                    "path": "text_embedding",
                    "similarity": "euclidean"
                },
            ]
        },
        name=index_name,
        type="vectorSearch",
    )
    if (index_name not in
        documentation_collection.list_search_indexes(index_name)):
        documentation_collection.create_search_index(search_index_model)
    else:
        documentation_collection.update_search_index(
            index_name, search_index_model)


def _populate_collection():
    """Populates a database collection from a Markdown file.
    
    Deletes any existing documents in the collection before adding new ones.

    Reads the markdown files, defined by the MARKDOWN_FILES list, chunking the
    text based on headers to create nodes, which are added to the collection.
    Each node contains:
    - The text content of the chunk.
    - An embedding of the text content.
    - A unique ID.
    - A URL that is associated with the node, stored in the node's metadata.
    """
    documentation_collection.delete_many({})

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

    documentation_collection.insert_many([node.model_dump() for node in nodes])

    # Uncomment the below function call to programmatically create a MongoDB
    # Atlas Search Index for Vector Search. As of 8/6/2024, programmatic
    # creation is not available on M0, M2, or M5 Atlas Clusters. If you are
    # using one of these cluster types, please see the README for instructions
    # as to how to create the index using the MongoDB Atlas UI.

    # _create_search_index()


if __name__ == "__main__":
    _populate_collection()
