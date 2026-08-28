import re

def clean_text(text: str) -> str:
    """it s used to clean the text which gets from the document"""

    if not text:
        return ""
    #reduce all the space and give a correct one space
    text=re.sub(r"[\t]+", " ",text)

    #it removes the empty lines
    text=re.sub(r"\n{3,}", "\n\n",text)

    #it is used to remove the unwanted space at the beginning/end
    text=text.strip()

    return text

def truncate_text(
        text: str,
        max_length: int = 5000
) -> str:
    """
    it is used to give the output in the limited length not as a big length
    """
    if not text:
        return ""

    if len(text) <= max_length:
        return text

    return text[:max_length] + "...."

def format_file_size(size_in_bytes: int) -> str:
    """
    convert the file from bytes format to a understandable language
    eg:1024 -> 1.00kb
    """
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"

    if size_in_bytes < 1024 ** 2:
        size = size_in_bytes / 1024
        return f"{size: 2f} KB"

    if size_in_bytes < 1024 ** 3:
        size = size_in_bytes / (1024 ** 2)
        return f"{size:.2f} MB"
    size = size_in_bytes/(1024 ** 3)

    return f"{size:.2f} GB"

def generate_error_message(
    operation: str,
    error: Exception    
) -> str:
    """
    it shows the error message while i cannot generate the content
    """
    return f"Failed to {operation}: {str(error)}"
