import json
import hashlib
from pathlib import Path
from config.settings import settings
from datetime import datetime

class Indexer:
    def __init__(self):
        self.index_json_path = settings.INDEX_JSON
        self.data = self._load_index()

    def _load_index(self):
        if self.index_json_path.exists():
            with open(self.index_json_path, "r") as f:
                return json.load(f)
        return {"files": {}}

    def _save_index(self):
        with open(self.index_json_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def get_file_hash(self, file_path: Path):
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()

    def index_file(self, original_path: Path, processed_path: Path):
        file_hash = self.get_file_hash(original_path)
        rel_processed = str(processed_path.relative_to(settings.BASE_DIR))
        
        self.data["files"][str(original_path.name)] = {
            "path": rel_processed,
            "hash": file_hash,
            "indexed_at": datetime.now().isoformat(),
            "status": "indexed"
        }
        self._save_index()

    def is_already_indexed(self, file_path: Path):
        name = str(file_path.name)
        if name in self.data["files"]:
            current_hash = self.get_file_hash(file_path)
            return self.data["files"][name]["hash"] == current_hash
        return False

indexer = Indexer()
