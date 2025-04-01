from mcp.server.fastmcp import FastMCP
from typing import Dict, Any

# Create server
mcp = FastMCP("MCP Python Service")

@mcp.tool()
def process_context(query: str, context: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
    """Process the query with given context"""
    return {
        "processed_query": query,
        "processed_context": context,
        "response": "Processed by MCP server"
    }

@mcp.tool()
def health_check() -> Dict[str, str]:
    """Check the health of the MCP service"""
    return {"status": "healthy"} 