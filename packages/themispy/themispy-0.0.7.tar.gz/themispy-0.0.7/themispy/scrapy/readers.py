import os

from themispy.project.utils import build_path


def read_jsonl(dir: str = 'temp/', attr: str = 'url', encoding: str = 'utf-8') -> 'list[str]':
    """Reads all JSON Lines datasources from the specified directory."""
    dir = build_path(dir)
    attr = f'"{attr}"'
    attr_len = len(attr)
    datasources = []
    
    with os.scandir(dir) as entries:
        for entry in entries:
            if entry.is_file() and not entry.name.startswith('.') \
            and not entry.name.lower() == 'readme.md':
                with open(entry, encoding=encoding) as file:
                    for line in file:
                        idx = line.find(attr)
                        line = line[idx+attr_len+3:]
                        idx = line.find(r'"')
                        line = line[:idx]
                        datasources.append(line)
                        
    return datasources
