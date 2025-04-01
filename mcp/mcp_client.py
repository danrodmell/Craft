from mcp import ClientSession, ClientCapabilities, Implementation
from mcp.client.websocket import WebSocketClientTransport
import os
import asyncio
from typing import Dict, Any

class MCPConfig:
    def __init__(self, api_key: str, environment: str = "development"):
        self.api_key = api_key
        self.environment = environment

class MCPClient:
    def __init__(self, config: MCPConfig):
        self.config = config
        self._session = None
        self._transport = None

    async def _ensure_session(self):
        if self._session is None:
            self._transport = WebSocketClientTransport(
                f"wss://api.{self.config.environment}.modelcontextprotocol.ai/v1/ws",
                headers={"Authorization": f"Bearer {self.config.api_key}"}
            )
            self._session = ClientSession(
                self._transport,
                Implementation(name="mcp-python", version="0.1.0"),
                ClientCapabilities()
            )
            await self._session.initialize()

    async def health_check(self) -> Dict[str, str]:
        try:
            await self._ensure_session()
            await self._session.ping()
            return {"status": "healthy"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    async def process_context(self, query: str, context: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        await self._ensure_session()
        result = await self._session.create_message(
            query,
            context=context,
            options=options or {}
        )
        return {
            "processed_query": query,
            "processed_context": context,
            "response": result.content
        }

    async def close(self):
        if self._session:
            await self._session.close()
            self._session = None
            self._transport = None

def create_sync_client(config: MCPConfig) -> MCPClient:
    """Create a synchronous client wrapper."""
    client = MCPClient(config)
    
    def health_check():
        return asyncio.run(client.health_check())
    
    def process_context(query: str, context: str, options: Dict[str, Any] = None):
        return asyncio.run(client.process_context(query, context, options))
    
    client.health_check = health_check
    client.process_context = process_context
    return client 