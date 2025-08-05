
import json
from typing import List, Dict, Union

def load_faqs(filepath: str) -> List[Dict[str, Union[str, List[str]]]]:
    """
    Reads the JSON and returns a list of question/answer pairs.
    
    Args:
        filepath: The absolute path to the JSON file.
        
    Returns:
        A list of dictionaries, where each dictionary has 'questions' and 'answer' keys.
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data
