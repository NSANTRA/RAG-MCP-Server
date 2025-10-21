import os
import requests
from langchain_chroma import Chroma
from Modules.Utils import saveFiles, rerankDocs
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from Modules.Config import CHROMA_DB_PERSIST_DIR, DOCUMENT_DIR, EMBEDDING_FUNCTION

def embedPDF(filepath: str, file_url: str, filename: str, collection: str) -> dict:
    """
    Embeds the content of a PDF file (from local path or URL) into a Chroma vectorstore.

    Args:
        filepath (str, optional): Local path to the PDF file.
        file_url (str, optional): Remote URL to the PDF file.
        filename (str, optional): Name to assign to the saved file (used for MCP client).
        collection (str): Target ChromaDB collection name.

    Returns:
        dict: A dictionary containing:
            - status (str): "success" or "error"
            - source (str): Original source (URL or local path)
            - destination_filepath (str): Final saved file path used for embedding
            - filename (str): File name used
            - collection (str): Target ChromaDB collection name
            - message (str): Summary of the operation
    """
    try:
        if not filepath and not file_url:
            raise ValueError("You must provide either 'filepath' or 'file_url'.")

        if filename:
            safe_filename = filename if filename.endswith(".pdf") else f"{filename}.pdf"
        
        elif file_url:
            safe_filename = file_url.split("/")[-1] or "downloaded.pdf"
        
        else:
            safe_filename = os.path.basename(filepath)

        destination = os.path.join(DOCUMENT_DIR, safe_filename)

        if file_url:
            response = requests.get(file_url, stream=True)
            if response.status_code != 200:
                raise ValueError(f"Failed to download file from URL: {file_url}")

            with open(destination, "wb") as f:
                for chunk in response.iter_content(chunk_size = 8192):
                    f.write(chunk)

            filepath = destination

        elif filepath:
            destination = saveFiles(filepath, target_filename = safe_filename)

        loader = PyPDFLoader(destination)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200
        )
        texts = text_splitter.split_documents(documents)

        _ = Chroma.from_documents(
            documents = texts,
            embedding = EMBEDDING_FUNCTION,
            collection_name = collection,
            persist_directory = CHROMA_DB_PERSIST_DIR
        )

        return {
            "status": "success",
            "source": file_url if file_url else filepath,
            "destination_filepath": destination,
            "filename": safe_filename,
            "collection": collection,
            "message": f"PDF {safe_filename} has been successfully embedded and stored in collection '{collection}'.",
        }

    except Exception as err:
        return {
            "status": "error",
            "message": f"Error embedding PDF: {str(err)}"
        }
    
def retrieveDocs(query: str, collection: str, top_k: int = 20, use_reranker: bool = True) -> dict:
    """
    Retrieves relevant documents from a ChromaDB collection based on a user query.

    Args:
        query (str): The search query or prompt used to find relevant documents.
        collection (str): Name of the ChromaDB collection to query.
        top_k (int, optional): Number of top documents to retrieve. Defaults to 20.
        use_reranker (bool, optional): Whether to rerank retrieved documents. Defaults to True.

    Returns:
        dict: A dictionary containing:
            - status (str): "success" if documents are retrieved, otherwise "error".
            - collection (str): Name of the queried collection.
            - query (str): The input query used for retrieval.
            - results (List[dict]): List of retrieved documents with:
                - content (str): Text content of the document.
                - metadata (dict): Metadata associated with the document.
            - count (int): Number of documents returned.

    On Error:
        Returns a dictionary with:
            - status (str): "error"
            - message (str): Error details.
    """
    try:
        db = Chroma(
            embedding_function = EMBEDDING_FUNCTION,
            collection_name = collection,
            persist_directory = CHROMA_DB_PERSIST_DIR
        ).as_retriever(kwargs = {"k": top_k})

        results = db.invoke(query)

        docs = [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
            }
            for doc in results
        ]

        if use_reranker:
            docs = rerankDocs(query, docs, top_k)

        return {
            "status": "success",
            "collection": collection,
            "query": query,
            "results": docs,
            "count": len(docs),
        }

    except Exception as err:
        return {
            "status": "error",
            "message": f"Error retrieving documents: {str(err)}"
        }

def citationProvider(results: dict, answer: str) -> dict:
    """
    Provides citations for the generated answer based on retrieved documents.

    Args:
        results (dict): Dictionary with "results" key containing retrieved documents.
        answer (str): The LLM-generated answer to annotate with citations.

    Returns:
        dict: {
            "answer_with_citations": str,
            "citations": List[dict]  # each with "id", "source", "snippet", "score"
        }
    """
    try:
        if "results" not in results or not results["results"]:
            return {
                "status": "neutral",
                "answer_with_citations": answer,
                "citations": []
            }

        citations = []
        for idx, doc in enumerate(results["results"], 1):
            citations.append({
                "id": idx,
                "source": doc.get("metadata", {}).get("source", f"Document {idx}"),
                "snippet": doc["content"][:200],
                "score": doc.get("score", None)
            })
            
        cited_answer = answer.strip() + "\n\nCitations:\n"
        for c in citations:
            cited_answer += f"[{c['id']}] {c['source']}\n"

        return {
            "status": "success",
            "answer_with_citations": cited_answer,
            "citations": citations
        }

    except Exception as err:
        return {
            "status": "error",
            "message": f"Error generating citations: {str(err)}"
        }
    
def listDocuments() -> dict:
    """
    Lists all documents stored in the DOCUMENT_DIR.

    Args:
        None

    Returns:
        dict: A dictionary containing:
            - status (str): "success" or "error"
            - documents (List[str]): List of document filenames
    """
    try:
        documents = os.listdir(DOCUMENT_DIR)
        return {
            "status": "success",
            "documents": documents
        }
    except Exception as err:
        return {
            "status": "error",
            "message": f"Error listing documents: {str(err)}"
        }