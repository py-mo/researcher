from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ChatInput(BaseModel):
    """
    Standard input schema for the Chat agent.
    """
    query_text: str = Field(..., description="The main user query")
    context: Optional[List[str]] = Field(
        default_factory=list, 
        description="Previous conversation history, as a list of messages"
    )
    intent: Optional[str] = Field(
        default="chat", 
        description="The intent of the query: chat, search, summarize, evaluate, etc."
    )
    filters: Optional[Dict[str, Any]] = Field(
        default_factory=dict, 
        description="Optional filters for search or retrieval (e.g., date, topic)"
    )
    documents: Optional[List[str]] = Field(
        default_factory=list, 
        description="External documents provided by the user (PDF paths or URLs)"
    )
    user_preferences: Optional[Dict[str, Any]] = Field(
        default_factory=dict, 
        description="User preferences like verbosity, summary length, or style"
    )
    task_id: Optional[str] = Field(
        default=None, 
        description="Unique identifier for async or long-running tasks"
    )
    tools: Optional[List[str]] = Field(
        default_factory=list, 
        description="Explicit tools to invoke: search, RAG, CAG, etc."
    )


if __name__ == "__main__":
    example_input = ChatInput(
        query_text="Find recent papers on reinforcement learning in robotics",
        context=["User: previous question about RL algorithms"],
        intent="search",
        filters={"year": "2025"},
        user_preferences={"summary_length": "short"}
    )
    print(example_input.model_dump_json(indent=2))
