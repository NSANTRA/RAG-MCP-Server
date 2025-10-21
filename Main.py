from mcp.server.fastmcp import FastMCP
from Modules import Core, Database, ToolDefinition

mcp = FastMCP("RAG")

@mcp.tool()
def describeTools() -> dict:
    return ToolDefinition.describeTools()

@mcp.tool()
def listDocuments() -> dict:
    return Core.listDocuments()

@mcp.tool()
def listDBs() -> dict:
    return Database.listDBs()

@mcp.tool()
def deleteCollection(collection: str) -> dict:
    return Database.deleteCollection(collection)

@mcp.tool()
def embedPDF(filepath: str, file_url: str, filename: str, collection: str) -> dict:
    return Core.embedPDF(filepath, file_url, filename, collection)

@mcp.tool()
def retrieveDocs(query: str, collection: str, top_k: int = 20, use_reranker: bool = True) -> dict:
    return Core.retrieveDocs(query, collection, top_k, use_reranker)

# There may be some validation error
@mcp.tool()
def citationProvider(results: dict, answer: str) -> dict:
    return Core.citationProvider(results, answer)

if __name__ == "__main__":
    mcp.run()