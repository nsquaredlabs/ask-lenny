#!/usr/bin/env python3
"""
Build or verify the txtai index for Lenny's Podcast transcripts.
"""

import os
import sys
import json
from pathlib import Path
from txtai import Embeddings

def check_existing_index(index_path):
    """Check if index already exists."""
    config_file = os.path.join(index_path, "config.json")
    metadata_file = os.path.join(index_path, "metadata.json")

    if os.path.exists(config_file) and os.path.exists(metadata_file):
        return True
    return False

def chunk_text(text, chunk_size=1000, overlap=200):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks

def build_index(transcripts_path, index_path):
    """Build the txtai index from transcript files."""
    print(f"Building index from {transcripts_path}...")

    # Collect all documents
    documents = []
    metadata = {}
    chunk_id = 0

    transcript_files = sorted(Path(transcripts_path).glob("*.txt"))
    total_files = len(transcript_files)

    print(f"Found {total_files} transcript files")

    for i, file_path in enumerate(transcript_files):
        guest_name = file_path.stem

        if (i + 1) % 50 == 0:
            print(f"Processing {i + 1}/{total_files} files...")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Chunk the transcript
        chunks = chunk_text(content, chunk_size=1000, overlap=200)

        for chunk_idx, chunk in enumerate(chunks):
            documents.append((chunk_id, chunk, None))
            metadata[str(chunk_id)] = {
                "guest": guest_name,
                "file": file_path.name,
                "chunk": chunk_idx,
                "text": chunk
            }
            chunk_id += 1

    print(f"\nCreated {chunk_id} chunks from {total_files} transcripts")
    print("Building embeddings (this may take a few minutes)...")

    # Create and build the index
    embeddings = Embeddings({
        "path": "sentence-transformers/all-MiniLM-L6-v2",
        "content": True
    })

    embeddings.index(documents)

    # Save index
    os.makedirs(index_path, exist_ok=True)
    embeddings.save(index_path)

    # Save metadata separately
    metadata_path = os.path.join(index_path, "metadata.json")
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f)

    print(f"\n✅ Index built successfully!")
    print(f"   Location: {index_path}")
    print(f"   Chunks: {chunk_id:,}")
    print(f"   Transcripts: {total_files}")

def main():
    script_dir = Path(__file__).parent
    index_path = script_dir / "lenny-index"
    transcripts_path = script_dir / "lenny-transcripts"

    # Check if transcripts exist
    if not transcripts_path.exists():
        print(f"Error: Transcripts directory not found at {transcripts_path}", file=sys.stderr)
        sys.exit(1)

    # Check if index already exists
    if check_existing_index(str(index_path)):
        print(f"✅ Index already exists at {index_path}")
        print("   Skipping indexing (delete the directory to rebuild)")
        sys.exit(0)

    # Build the index
    try:
        build_index(str(transcripts_path), str(index_path))
    except Exception as e:
        print(f"\nError building index: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
