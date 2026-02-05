# Ask Lenny Skill - Demo Prompt

Use this prompt to demonstrate building the ask-lenny Claude Code skill with a pre-built index.

## Prerequisites

Run these commands first to set up the demo environment:

```bash
cd /home/testuser/flex-product-claude-code/asklenny-demo

# Create the skill directory
mkdir -p ~/.claude/skills/asklenny

# Copy the pre-built index and transcripts
cp -r lenny-index ~/.claude/skills/asklenny/
cp -r lenny-transcripts ~/.claude/skills/asklenny/

# Verify txtai is installed
pip3 list | grep txtai || pip3 install txtai
```

---

## Prompt for Claude Code

```
I want to demonstrate building a Claude Code skill called "ask-lenny" that queries Lenny Rachitsky's podcast transcripts using semantic search.

**Current state:**
- I have 302 transcript files in ~/.claude/skills/asklenny/lenny-transcripts/
- I have a pre-built txtai index at ~/.claude/skills/asklenny/lenny-index/ (36,800 chunks, 92MB)
- txtai is already installed

**What I need you to build:**

1. **Python indexing script** (`index_transcripts.py`):
   - Same as before, but check if index exists first
   - If it exists, print "✅ Index already exists at [path]. Skipping indexing." and exit
   - If not, build the index with these specs:
     * Uses txtai with sentence-transformers/all-MiniLM-L6-v2
     * Chunks: 1000 chars with 200 char overlap
     * Creates embeddings file and separate metadata.json
     * Saves to lenny-index/ directory
   - Include proper error handling and progress indicators

2. **Query script** (`query.py`):
   - Loads the existing txtai index from ~/.claude/skills/asklenny/lenny-index/
   - Loads metadata from lenny-index/metadata.json
   - Takes a question as command-line argument
   - Returns top 10 relevant transcript segments
   - Output includes: guest name, relevance score, text preview, and full JSON

3. **Claude Code skill** (`SKILL.md`):
   - Skill invoked as `/asklenny <question>`
   - Implementation steps:
     a. Check if index exists (if not, instruct user to run indexing)
     b. Run query.py with user's question
     c. Parse results to get top segments
     d. Read relevant context from the transcript text in results
     e. Synthesize answer with specific citations and quotes
   - Answer format:
     * Brief direct answer
     * Insights from 3-4 different guests with quotes
     * Actionable takeaways
     * Source list at bottom

4. **Setup guide** (`README.md`):
   - Overview of the skill and its features
   - Installation instructions (txtai)
   - Explain the index is pre-built (how it was created)
   - Usage examples with actual questions
   - How to query the index
   - Troubleshooting section
   - Technical details (model, chunk size, index size)

**Success criteria:**
- Can immediately test `/asklenny "How do successful founders prioritize?"`
- Gets relevant results from the existing index in <2 seconds
- No 20-minute rebuild needed
- Everything works as a portable, shareable skill
- Answer includes specific guest citations with quotes

Please build these files in ~/.claude/skills/asklenny/ and verify the existing index works by running a test query.
```

---

## After Building

Test the skill:

```bash
/asklenny How do successful founders prioritize features?
/asklenny What do top PMs look for when hiring?
/asklenny How should I think about pricing for B2B SaaS?
```

## Demo Talking Points

- **The Problem**: 302 podcast transcripts = ~100 hours of content, impossible to search manually
- **The Solution**: Semantic search with txtai finds relevant answers in seconds
- **The Value**: Pre-built index means no 20-minute wait, fully portable
- **The Magic**: Not keyword matching - understands meaning and context
- **The Result**: Instant access to insights from 300+ top founders, PMs, and operators
