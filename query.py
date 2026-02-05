#!/usr/bin/env python3
"""
Query the Lenny's Podcast transcript index using semantic search.
"""

import sys
import json
import os
from pathlib import Path
from txtai import Embeddings

def load_index(index_path):
    """Load the txtai index and metadata."""
    if not os.path.exists(index_path):
        print(f"Error: Index not found at {index_path}", file=sys.stderr)
        print("Run index_transcripts.py first to build the index.", file=sys.stderr)
        sys.exit(1)

    # Load embeddings
    embeddings = Embeddings()
    embeddings.load(index_path)

    # Load metadata
    metadata_path = os.path.join(index_path, "metadata.json")
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    return embeddings, metadata

def query_index(embeddings, metadata, question, limit=10):
    """Query the index and return relevant segments."""
    # Search the index
    results = embeddings.search(question, limit)

    # Format results with metadata
    formatted_results = []
    for score, idx in results:
        idx_str = str(idx)
        if idx_str in metadata:
            chunk_data = metadata[idx_str]
            formatted_results.append({
                "score": float(score),
                "guest": chunk_data.get("guest", "Unknown"),
                "file": chunk_data.get("file", "Unknown"),
                "chunk": chunk_data.get("chunk", 0),
                "text": chunk_data.get("text", "")
            })

    return formatted_results

def main():
    if len(sys.argv) < 2:
        print("Usage: python query.py <question>", file=sys.stderr)
        sys.exit(1)

    # Get question from command line
    question = " ".join(sys.argv[1:])

    # Determine index path
    script_dir = Path(__file__).parent
    index_path = script_dir / "lenny-index"

    # Load index
    try:
        embeddings, metadata = load_index(str(index_path))
    except Exception as e:
        print(f"Error loading index: {e}", file=sys.stderr)
        sys.exit(1)

    # Query
    try:
        results = query_index(embeddings, metadata, question, limit=10)

        # Output as JSON
        print(json.dumps(results, indent=2))

    except Exception as e:
        print(f"Error querying index: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
