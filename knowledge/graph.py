from pathlib import Path
from knowledge.linker import linker
from config.settings import settings
import json
import logging

logger = logging.getLogger(__name__)

class KnowledgeGraph:
    def __init__(self):
        self.nodes = [] # List of filenames/titles
        self.edges = [] # List of (source, target) tuples

    def build_graph(self):
        self.nodes = []
        self.edges = []
        
        processed_dir = settings.DATA_PROCESSED_DIR
        for md_file in processed_dir.glob("*.md"):
            source_name = md_file.stem
            self.nodes.append(source_name)
            
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                links = linker.detect_links(content)
                for target in links:
                    self.edges.append({"source": source_name, "target": target})

        return {"nodes": self.nodes, "edges": self.edges}

    def save_graph(self, path=None):
        if path is None:
            path = settings.BASE_DIR / "data" / "graph.json"
        
        graph_data = self.build_graph()
        with open(path, "w") as f:
            json.dump(graph_data, f, indent=4)
        logger.info(f"Graph saved to {path}")

graph_builder = KnowledgeGraph()
