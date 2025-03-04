import logging
import json
import sys
from typing import Any, Dict, List, Optional

from langchain.llms.base import LLM
from pydantic import BaseModel, Field
from langchain_ollama import OllamaLLM



# Configure logging for error tracking
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")
LOGGER = logging.getLogger(__name__)




class OllamaHandler(LLM):
    """
    Acts as an agent in LangChain using the Ollama model.
    """

    model: str = Field(default="llama3.2")
    llm: Optional[OllamaLLM] = None

    def __init__(self, **data):
        """
        Initialize the object and bind the model.
        """
        super().__init__(**data)
        object.__setattr__(self, "llm", self.get_llm())

    def get_llm(self) -> Optional[OllamaLLM]:
        """
        Initialize and return the Ollama model.
        """
        try:
            return OllamaLLM(
                model=self.model,
                system_message="Analyze the text and provide a response.",
                return_direct=True,
            )
        except Exception as e:
            LOGGER.error(f"Error initializing the model: {e}")
            return None

    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        """
        Invoke the model using LangChain.
        """
        return self.explain_question_mark(prompt)

    def explain_question_mark(self, question: str) -> str:
        """
        Execute a query and return the result.
        """
        if self.llm is None:
            return "Error: Model initialization failed."

        try:
            response = self.llm.invoke(question)
            return response
        except Exception as e:
            LOGGER.error(f"Error executing the model: {e}")
            return f"Error retrieving response: {e}"

    @property
    def _llm_type(self) -> str:
        """
        Return the type of LLM used.
        """
        return "custom_ollama"

print("LLM Handler script executed successfully!")
