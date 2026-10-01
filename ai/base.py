from abc import ABC, abstractmethod

class AIPlatform(ABC):
      @abstractmethod
      def chat(self, prompt: str) -> str:
            #sends a prompt to the AI and get a response
            pass
