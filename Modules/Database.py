from langchain_chroma import Chroma
from Modules.Config import CHROMA_DB_PERSIST_DIR

def listDBs() -> dict:
    """
    Lists all existing collections in the Chroma vectorstore.

    Args:
        None

    Returns:
        dict: A dictionary containing:
            - status (str): "success"
            - collections (List[str]): Names of all available vectorstore collections.
            - count (int): Total number of collections.
            - persist_directory (str): Directory path where ChromaDB collections are stored.

    On Error:
        Returns a dictionary with:
            - status (str): "error"
            - message (str): Error details.
    """
    try:
        db_collections = Chroma(persist_directory = CHROMA_DB_PERSIST_DIR)._client.list_collections()
        db_list = [i.name for i in db_collections]
        
        return {
            "status": "success",
            "collections": db_list,
            "count": len(db_list),
            "persist_directory": CHROMA_DB_PERSIST_DIR
        }

    except Exception as err:
        return {
            "status": "error",
            "message": f"Error listing DBs: {str(err)}"
        }
    
def deleteCollection(collection: str) -> dict:
    try:
        _ = Chroma(
            persist_directory = CHROMA_DB_PERSIST_DIR,
            collection_name = collection
        ).delete_collection()

        return {
            "status": "success",
            "message": f"Collection {collection} has been successfully deleted.",
        }
    
    except Exception as err:
        return {
            "status": "error",
            "message": f"Error deleting collection: {str(err)}"
        }