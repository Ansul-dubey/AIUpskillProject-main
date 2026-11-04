# Can easily switch storage implementation
from src.storage.json_storage import JSONStorage  # If you made it

# Just change one line:
storage = JSONStorage("data/articles_json")

# Everything else stays the same!
