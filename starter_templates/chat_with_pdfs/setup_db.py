"""Set up the Vector DB for Chat with PDF Bot"""
import pathlib
import tempfile
from typing import Dict, List, Optional, Union
from urllib import request as url_request
import uuid

import chromadb
from chromadb import config
import pydantic

from unstructured.partition import pdf as unstructured_partition
from unstructured.chunking import title as unstructured_chunking


# A list of PDFs that will be used to create the collection.
# The elements of this list can be either a file path or a url.
PDF_FILES = [
    "https://arxiv.org/pdf/1706.03762",  # "Attention Is All You Need"
    "https://arxiv.org/pdf/2005.14165",  # "Language Models are Few-Shot Learners"
    "https://arxiv.org/pdf/2303.08774",  # "GPT-4 Technical Report"
]

# Name of the collection
PDF_COLLECTION_NAME = "llm_papers"


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


def _add_pdfs_to_collection(
    collection: chromadb.Collection,
    pdf_files: List[str]
):
    """Adds pdf files to a Chroma (vector DB) collection.

    Takes in a list of either local paths to a pdf file, or urls to download
    a pdf file. It will then extract the pdf to text and chunk the data by
    Unstructured title elements to identify sections. These chunks will then be added
    into the Chroma collection. This function also adds a key value pair
    of (pdf_file -> first parsed chunk) to the Chroma collection's metadata
    for each pdf file.

    Args:
        collection: The Chroma (vector DB) collection. 
        pdf_files: A list of either local paths or urls to pdf files.
    """
    new_collection_metadata = {}
    for pdf_file in pdf_files:
        file_path = pathlib.Path(pdf_file)
        file = tempfile.NamedTemporaryFile()
        # Download pdf file if it is not local.
        if not file_path.is_file():
            file_path = file.name
            url_request.urlretrieve(pdf_file, file_path)

        elements = unstructured_partition.partition_pdf(filename=file_path)
        chunks = unstructured_chunking.chunk_by_title(
            elements, max_characters=2000)

        nodes = []
        for chunk in chunks:
            nodes.append(_Node(text=str(chunk),
                               metadata={"file_location": pdf_file}))

        documents, ids, metadatas = (
            map(list,
                zip(*[(node.text, node.id, node.metadata) for node in nodes])))
        collection.add(documents=documents,
                       ids=ids, metadatas=metadatas)

        new_collection_metadata[pdf_file] = str(chunks[0])
        file.close()
    collection.modify(metadata=new_collection_metadata)


def _create_default_pdf_collection() -> chromadb.Collection:
    """Creates and populates the default Chroma collection.

    Resets the Chroma client, creates a Chroma Collection 
    object, and populates it based on the PDF files given by PDF_FILES.
    The collection also contains the names of the processed files as
    metadata.

    Returns:
        The created PDF collection.
    """
    chroma_client.reset()
    collection = chroma_client.create_collection(
        name=PDF_COLLECTION_NAME)
    _add_pdfs_to_collection(collection, PDF_FILES)
    return collection


if __name__ == "__main__":
    _create_default_pdf_collection()
