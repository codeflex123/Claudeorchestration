from pydantic import BaseModel
from typing import List, Dict, Optional

class MCPTool(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    required_permissions: List[str]

class MCPRegistry:
    def __init__(self):
        # A static registry for demonstration. In a real app, this might be dynamic.
        self.tools: Dict[str, MCPTool] = {
            "github": MCPTool(
                id="github",
                name="GitHub Connector",
                description="Manage repositories, issues, and PRs.",
                icon="Github",
                required_permissions=["repo", "user"]
            ),
            "terminal": MCPTool(
                id="terminal",
                name="Local Terminal",
                description="Execute shell commands and scripts safely.",
                icon="Terminal",
                required_permissions=["read", "write"]
            ),
            "google-drive": MCPTool(
                id="google-drive",
                name="Google Drive",
                description="Access and modify documents and files.",
                icon="FileText",
                required_permissions=["drive.file"]
            ),
            "browser": MCPTool(
                id="browser",
                name="Web Browser",
                description="Search and scrape web content in real-time.",
                icon="Globe",
                required_permissions=["network"]
            ),
            "slack": MCPTool(
                id="slack",
                name="Slack Bridge",
                description="Send notifications and interact with channels.",
                icon="MessageSquare",
                required_permissions=["chat:write"]
            )
        }

    def get_tool_metadata(self, tool_ids: List[str]) -> List[MCPTool]:
        """
        Enriches a list of tool IDs with full metadata from the registry.
        """
        enriched_tools = []
        for tid in tool_ids:
            tid_lower = tid.lower().replace(" ", "-") # Basic normalization
            # Try to find the closest match
            match = next((t for k, t in self.tools.items() if k in tid_lower or tid_lower in k), None)
            if match:
                enriched_tools.append(match)
        return enriched_tools

mcp_registry = MCPRegistry()
