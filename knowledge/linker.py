import re
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class Linker:
    # Pattern for [[Link]] or [[Link|Alias]]
    LINK_PATTERN = r"\[\[(.*?)\]\]"

    def detect_links(self, text):
        matches = re.findall(self.LINK_PATTERN, text)
        links = []
        for match in matches:
            if "|" in match:
                target = match.split("|")[0].strip()
            else:
                target = match.strip()
            links.append(target)
        return list(set(links))

linker = Linker()
