from typing import List
from pydantic import BaseModel

class ToolArg(BaseModel):
    name: str
    description: str
    type: str = "string"
    required: bool = True

class ToolReturn(BaseModel):
    description: str
    type: str = "dict"

class ToolInfo(BaseModel):
    name: str
    description: str
    args: List[ToolArg]
    returns: List[ToolReturn]

class ToolManifest(BaseModel):
    server_name: str
    tool_count: int
    tools: List[ToolInfo]

def describeTools() -> dict:
    """
    Lists and describes all tools available on the MCP server.

    Args:
        None

    Returns:
        dict: A dictionary containing:
            - server_name (str): Name of the MCP server.
            - tool_count (int): Total number of registered tools.
            - tools (List[dict]): Detailed metadata for each tool, including:
                - name (str): Tool name.
                - description (str): Description of the tool’s purpose.
                - args (List[dict]): Arguments accepted by the tool with type and description.
                - returns (List[dict]): Return structure with description and type.
    """
    tools = [
        ToolInfo(
            name = "describeTools",
            description = "Lists and describes all tools available on the MCP server.",
            args = [],
            returns = [
                ToolReturn(
                    type = "dict",
                    description = "Returns a dictionary consisting all the information available on MCP tools including arguments, returns, types, etc."
                )
            ]
        ),

        ToolInfo(
            name = "embedPDF",
            description = "Embeds the given PDF and stores in Chroma vectorstore.",
            args = [
                ToolArg(
                    name = "filepath",
                    description = "Specifies the filepath for the PDF",
                    type = "string",
                    required = True
                ),
                
                ToolArg(
                    name = "collection",
                    description = "Collection name for the ChromaDB vectorstore. (optional)",
                    type = "string",
                    required = False
                )
            ],
            returns = [
                ToolReturn(
                    type = "dict",
                    description = "Return a dictionary of filepath, collection name, status and confirmation message."
                )
            ]
        ),

        ToolInfo(
            name = "listDBs",
            description = "Lists all the collections in the ChromaDB vectorstore.",
            args = [],
            returns = [
                ToolReturn(
                    type = "dict",
                    description = "Returns a dictionary of collection list, number of collections and local directory of the ChromaDB vectorstore.",
                )
            ]
        ),

        ToolInfo(
            name = "deleteCollection",
            description = "Deletes the specified collection from the ChromaDB vectorstore, if available",
            args = [
                ToolArg(
                    name = "collection",
                    description = "Collection name that is to be deleted.",
                    type = "string",
                    required = True
                )
            ],
            returns = [
                ToolReturn(
                    type = "dict",
                    description = "Returns a dictionary consisting of status and corresponding message"
                )
            ]
        ),

        ToolInfo(
            name = "retrieveDocs",
            description = "Provides relevant documents retrieved from the ChromaDB vectorstore based on the query provided.",
            args = [
                ToolArg(
                    name = "query",
                    description = "Query or prompt provided by the user that is to be used to retrieve relevant documents from the ChromaDB vectorstore",
                    type = "string",
                    required = True
                ),
                ToolArg(
                    name = "collection",
                    description = "Collection name for the ChromaDB vectorstore. (optional)",
                    type = "string",
                    required = False
                ),

                ToolArg(
                    name = "top_k",
                    description =  "Specifies the number of documents to be retrieved. (Optional)",
                    type = "int",
                    required = False
                ),

                ToolArg(
                    name = "use_reranker",
                    description =  "Specifies whether to rerank the retrieved documents or not. (Optional)",
                    type = "bool",
                    required = False
                )
            ],
            returns = [
                ToolReturn(
                    type = "dict",
                    description = "Returns a dictionary consisting of status, collection name, query provided by the user, results and the number of documents retrieved."
                )
            ]
        )
    ]

    return ToolManifest(
        server_name = "RAG",
        tools = tools,
        tool_count = len(tools)
    ).dict()