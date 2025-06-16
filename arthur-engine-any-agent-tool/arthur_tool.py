import os
import requests
from typing import Optional, Dict, Any


class ArthurEngineClient:
    def __init__(
        self,
        task_id: str,
        conversation_id: str,
        user_id: str,
        host: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize the Arthur Engine client.
        
        Args:
            task_id: The ID of the task to validate against
            conversation_id: The ID of the conversation
            user_id: The ID of the user
            host: The Arthur Engine host URL. If not provided, will use ARTHUR_ENGINE_HOST env var.
            api_key: The Arthur Engine API key. If not provided, will use ARTHUR_ENGINE_API_KEY env var.
        """
        self.task_id = task_id
        self.conversation_id = conversation_id
        self.user_id = user_id
        self.host = host or os.getenv("ARTHUR_ENGINE_HOST")
        self.api_key = api_key or os.getenv("ARTHUR_ENGINE_API_KEY")
        
        if not self.host:
            raise ValueError("Arthur Engine host URL must be provided or set in ARTHUR_ENGINE_HOST env var")
        if not self.api_key:
            raise ValueError("Arthur Engine API key must be provided or set in ARTHUR_ENGINE_API_KEY env var")

    def validate_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Validate a prompt using the Arthur Engine API.
        
        Args:
            prompt: The prompt text to validate
            
        Returns:
            Dict containing the API response
        """
        url = f"{self.host}/api/v2/tasks/{self.task_id}/validate_prompt"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": prompt,
            "conversation_id": self.conversation_id,
            "user_id": self.user_id
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        return response.json()

    def validate_response(
        self,
        inference_id: str,
        response: str,
        context: str
    ) -> Dict[str, Any]:
        """
        Validate a response using the Arthur Engine API.
        
        Args:
            inference_id: The ID of the inference to validate
            response: The response text to validate
            context: The context information for validation
            
        Returns:
            Dict containing the API response
        """
        url = f"{self.host}/api/v2/tasks/{self.task_id}/validate_response/{inference_id}"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "response": response,
            "context": context
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        return response.json()
