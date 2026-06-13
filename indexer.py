
import os, json, re, pathlib

DOCS_DIR = "docs"
INDEX_PATH = ".kb/index.json"

def parse_markdown(filepath):
    text = open(filepath).read()
    # 用 ## heading 切塊
    chunks = re.split(r'\n(?=## )', text)
    results = []
    for chunk in chunks:
        lines = chunk.strip().splitlines()
        heading = lines[0].lstrip('#').strip() if lines else "intro"
        content = "\n".join(lines[1:]).strip()
        if content:
            results.append({
                "source": f"{os.path.basename(filepath)}#{heading}",
                "heading": heading,
                "content": content
            })
    return results

def build_index():
    os.makedirs(".kb", exist_ok=True)
    all_chunks = []
    for f in pathlib.Path(DOCS_DIR).glob("*.md"):
        all_chunks.extend(parse_markdown(f))
    json.dump(all_chunks, open(INDEX_PATH, "w"), ensure_ascii=False, indent=2)
    print(f"Indexed {len(all_chunks)} chunks → {INDEX_PATH}")

if __name__ == "__main__":
    build_index()