import logging
from file_parser import FileParser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    files = ["file1.txt", "A4.pdf",]

    for filename in files:
        try:
            # Create a FileParser instance with the filename
            parser = FileParser(filepath=filename)
            # Parse the file and print the output
            content = parser.parse()
            print(f"Content of {filename}:")
            print(content[:100])  # Print the first 100 characters to avoid too much output
            print("--------------------------------------------------")
        except Exception as e:
            logging.error(f"Failed to process file '{filename}': {e}")

if __name__ == "__main__":
    main()
