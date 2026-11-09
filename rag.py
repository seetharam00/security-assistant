from pathlib import Path

def load_chunks(folder="standards"):
    chunks = []
    for path in Path(folder).glob("*.md"):
        for para in path.read_text().split("\n\n"):
            if para.strip():
                chunks.append({"source": path.name, "text": para.strip()})
    return chunks

def search(query, chunks, k=3):
    query_words = set(query.lower().split())
    scored = []
    for c in chunks:
        overlap = len(query_words & set(c["text"].lower().split()))
        if overlap:
            scored.append((overlap, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:k]]