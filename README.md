# Ask Lenny - Claude Code Skill

Query Lenny Rachitsky's podcast transcripts using semantic search. Get instant answers with specific citations from 300+ top founders, PMs, and operators.

## What This Does

This Claude Code skill lets you ask natural language questions and get insights from 302 podcast episodes (100+ hours of content). It uses semantic search to find relevant segments and synthesizes comprehensive answers with specific quotes and citations.

**Example:**
```bash
/asklenny How do successful founders prioritize features?
```

**Returns:** Insights from multiple guests with direct quotes, actionable takeaways, and source citations.

## Requirements

- **Python**: 3.10 or higher (required for txtai 9.x)
- **Claude Code**: Latest version (install from [claude.ai/code](https://claude.ai/code))
- **Disk Space**: ~500MB (92MB index + 302 transcript files + dependencies)
- **Memory**: ~500MB RAM during queries (for model and index)

### Python Dependencies

Installed automatically via `requirements.txt`:
- `txtai` (>=8.4.0) - Semantic search engine
- `sentence-transformers` (>=2.2.0) - Embedding model

**Check your Python version:**
```bash
python3 --version  # Should show 3.10 or higher
```

**If you have Python 3.9 or lower**, you'll need Python 3.10+ installed. On macOS with Homebrew:
```bash
brew install python@3.12
which python3.12  # Verify it's installed
```

## Installation

### Quick Install

```bash
# Clone into your Claude Code skills directory
git clone https://github.com/yourusername/ask-lenny.git ~/.claude/skills/ask-lenny

cd ~/.claude/skills/ask-lenny

# Create virtual environment with Python 3.10+
# Use python3.12, python3.11, or python3.10 depending on what you have installed
python3.12 -m venv venv

# Activate venv and install dependencies
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Verify the index exists (it's pre-built!)
ls -lh lenny-index/
```

**Why the venv?** The index was built with txtai 9.x which requires Python 3.10+. The venv ensures compatibility regardless of your system Python version.

The index is pre-built and included in the repository, so you can start querying immediately!

### Manual Setup

If you need to rebuild the index (only necessary if you modify transcripts):

```bash
cd ~/.claude/skills/asklenny
python3 index_transcripts.py
```

This will take ~15-20 minutes to process 302 transcripts and create 36,800 searchable chunks.

## Usage

In any Claude Code session, use the `/asklenny` command:

```bash
/asklenny How do successful founders prioritize features?
/asklenny What do top PMs look for when hiring?
/asklenny How should I think about pricing for B2B SaaS?
/asklenny What's the best way to run user research?
```

The skill will:
1. Search 36,800 chunks using semantic similarity
2. Find the top 10 most relevant segments
3. Synthesize a comprehensive answer with quotes
4. Cite specific episodes and guests

## Technical Details

- **Search Engine**: txtai with sentence-transformers/all-MiniLM-L6-v2
- **Index Size**: ~92MB (36,800 chunks from 302 transcripts)
- **Query Performance**: <2 seconds per search
- **Chunking**: 1000 characters with 200 character overlap
- **Model**: 384-dimensional embeddings

## Project Structure

```
ask-lenny/
├── SKILL.md              # Skill definition for Claude Code
├── query.py              # Semantic search script
├── index_transcripts.py  # Index building script
├── requirements.txt      # Python dependencies
├── lenny-index/          # Pre-built txtai index (36,800 chunks)
├── lenny-transcripts/    # 302 podcast transcript files
├── CLAUDE.md             # Development context
├── PROMPT.md             # Original build instructions
└── README.md             # This file
```

## How It Works

### Indexing (Pre-built)

1. Reads all 302 transcript files from `lenny-transcripts/`
2. Splits each transcript into 1000-character chunks with 200-char overlap
3. Creates embeddings using sentence-transformers/all-MiniLM-L6-v2
4. Stores in a FAISS-backed txtai index for fast similarity search
5. Saves metadata mapping chunks to guests and episodes

### Querying (What You Use)

1. Takes your natural language question
2. Converts it to a 384-dimensional embedding
3. Searches the index for semantically similar chunks
4. Returns top 10 results with relevance scores
5. Claude synthesizes an answer with quotes and citations

## Example Output

**Query:** `/asklenny How should I think about pricing for B2B SaaS?`

**Response:**
```markdown
## Pricing should be value-based, not cost-based, and you should charge more than you think

Successful founders emphasize that pricing is about capturing a fraction of the value
you deliver to customers, not just covering costs plus margin. They recommend starting
with higher prices and testing down, experimenting frequently, and treating pricing as
a core product decision.

### Key Insights

**Patrick Campbell** shares that most companies underprice by 2-5x:
> "The biggest mistake I see is companies pricing based on their costs or what
> they think is 'fair' rather than what the customer is willing to pay based
> on the value they receive."

... [continues with more insights and sources]
```

## Troubleshooting

### "Index not found" error

Make sure you're in the skill directory:
```bash
cd ~/.claude/skills/asklenny
ls lenny-index/config.json
```

If the index is missing, run `python3 index_transcripts.py`.

### "txtai not found" or version errors

Make sure you've created the venv with Python 3.10+:
```bash
cd ~/.claude/skills/ask-lenny
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Slow queries

First query may be slower (~5 seconds) as models load into memory. Subsequent queries should be <2 seconds.

### Poor results

Try rephrasing your question to be more specific. The search understands semantic meaning, so use natural language rather than keywords.

## Benefits

- **Instant Access**: Search 100+ hours of content in <2 seconds
- **Semantic Understanding**: Finds relevant answers, not just keyword matches
- **Multiple Perspectives**: Get insights from different guests on the same topic
- **Portable**: Pre-built index means no 20-minute setup time
- **Comprehensive**: 302 episodes covering product, growth, leadership, and more

## Contributing

To add new transcripts:

1. Add transcript files to `lenny-transcripts/`
2. Delete the `lenny-index/` directory
3. Run `python3 index_transcripts.py`
4. Commit the updated index

## License

MIT License - see [LICENSE](LICENSE) file for details.

The code and tooling are open source. Podcast transcripts are from Lenny's Podcast and are included for educational and demonstration purposes. All rights to the original podcast content remain with Lenny Rachitsky and the respective guests.

## Credits

Transcripts from [Lenny's Podcast](https://www.lennyspodcast.com/) by Lenny Rachitsky.
Built as a demonstration of Claude Code skills with txtai semantic search.
