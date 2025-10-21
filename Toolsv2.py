import Modules.Core as Core
from mcp.server.fastmcp import FastMCP
from Modules.ToolDefinition import describeTools as getToolManifest
from Modules.Database import (
    listDBs as showDBs,
    deleteCollection as delCollection
)

mcp = FastMCP("RAG")

@mcp.tool()
def describeTools() -> dict:
    return getToolManifest()

@mcp.tool()
def listDBs() -> dict:
    return showDBs()

@mcp.tool()
def deleteCollection(collection: str) -> dict:
    return delCollection(collection)

@mcp.tool()
def embedPDF(filepath: str, file_url: str, filename: str, collection: str) -> dict:
    return Core.embedPDF(filepath, file_url, filename, collection)

@mcp.tool()
def retrieveDocs(query: str, collection: str, top_k: int = 20, use_reranker: bool = True) -> dict:
    return Core.retrieveDocs(query, collection, top_k, use_reranker)

# Validation error
@mcp.tool()
def citationProvider(results: dict, answer: str) -> dict:
    return Core.citationProvider(results, answer)

if __name__ == "__main__":
    mcp.run()