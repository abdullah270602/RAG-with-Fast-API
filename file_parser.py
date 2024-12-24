from abc import ABC, abstractmethod
import logging

# Base parser interface
class BaseParser(ABC):
    @abstractmethod
    def parse(self, filepath: str) -> str:
        """Abstract method to parse file content."""
        pass

# Concrete Parser for TXT Files
class TxtParser(BaseParser):
    def parse(self, filepath: str) -> str:
        """Parses a text file and returns its content."""
        try:
            with open(filepath, 'r') as file:
                return file.read()
        except Exception as e:
            logging.error(f"Error reading text file: {e}")
            return "Error reading text file"