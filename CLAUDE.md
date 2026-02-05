# Ask Lenny Skill - Development Context

This is a Claude Code skill that provides semantic search over Lenny Rachitsky's podcast transcripts using txtai.

## Purpose

Enable Claude Code users to query 302 podcast transcripts (100+ hours) using natural language and get comprehensive answers with specific citations and quotes. The skill is designed to be shared with product teams and requires minimal setup.

## Architecture

### Core Components

1. **SKILL.md** - Claude Code skill definition
   - Defines the `/asklenny` command behavior
   - Specifies answer format and synthesis approach
   - Handles error cases and edge conditions

2. **query.py** - Semantic search engine
   - Loads the pre-built txtai index
   - Converts questions to embeddings
   - Returns top 10 relevant segments with metadata
   - Outputs JSON for programmatic consumption

3. **index_transcripts.py** - Index builder
   - Checks for existing index (skips if present)
   - Chunks transcripts (1000 chars, 200 overlap)
   - Creates txtai embeddings
   - Saves index and metadata separately

4. **lenny-index/** - Pre-built search index
   - 36,800 chunks from 302 transcripts
   - FAISS-backed for fast similarity search
   - sentence-transformers/all-MiniLM-L6-v2 model
   - Separate metadata.json for chunk details

5. **lenny-transcripts/** - Source data
   - 302 transcript files (one per episode)
   - Named by guest (e.g., "Ada Chen Rekhi.txt")
   - Plain text format with speaker labels

## Technical Decisions

### Why txtai?

- Fast semantic search with minimal code
- FAISS backend for efficient vector similarity
- Small footprint (~92MB index for 302 transcripts)
- Good balance of accuracy and performance

### Why Pre-build the Index?

- Indexing takes ~15-20 minutes
- Index is deterministic (same transcripts = same index)
- Makes the skill instantly usable
- Reduces dependency on local compute resources

### Chunking Strategy

- **Size**: 1000 characters
- **Overlap**: 200 characters
- **Rationale**: Balances context preservation with search granularity

### Model Choice

- **Model**: sentence-transformers/all-MiniLM-L6-v2
- **Dimensions**: 384
- **Rationale**: Fast, accurate, well-suited for semantic search tasks

## Development Guidelines

### When Modifying the Skill

1. **Keep answers concise**: 3-4 insights, not 10
2. **Always cite sources**: Guest name + episode context
3. **Use direct quotes**: Specific, attributable quotes from transcripts
4. **Provide takeaways**: Actionable bullet points
5. **Maintain <2 second queries**: Don't read all 10 results unless necessary

### Answer Quality Standards

Good answers should:
- Start with a direct 2-3 sentence summary
- Include 3-4 insights from different guests
- Feature specific, relevant quotes (not generic statements)
- Provide 3-4 actionable takeaways
- List sources at the bottom

Avoid:
- Generic advice without citations
- Summarizing the question back to the user
- Including every search result (use top 5-7)
- Overly long responses (aim for readable length)

### Code Style

- Scripts should be standalone and CLI-friendly
- Use argparse or sys.argv for simple arguments
- Output JSON for programmatic consumption
- Print errors to stderr
- Exit with appropriate codes (0 = success)

### Testing Queries

Use these to verify the skill works well:

```bash
/asklenny How do successful founders prioritize features?
/asklenny What do top PMs look for when hiring?
/asklenny How should I think about pricing for B2B SaaS?
/asklenny What's the best way to run user research?
/asklenny How do you know when to pivot?
```

Expected behavior:
- Returns in <2 seconds
- Cites 3-4 different guests
- Includes specific quotes
- Provides actionable takeaways

## File Organization

```
ask-lenny/                        # Skill root (install to ~/.claude/skills/asklenny)
├── SKILL.md                      # Skill definition (required)
├── query.py                      # Query script (executable)
├── index_transcripts.py          # Indexing script (rarely used)
├── requirements.txt              # Python dependencies
├── README.md                     # User-facing documentation
├── CLAUDE.md                     # This file (dev context)
├── PROMPT.md                     # Original build instructions (reference)
├── lenny-index/                  # Pre-built index (92MB)
│   ├── config.json               # txtai configuration
│   ├── metadata.json             # Chunk metadata
│   └── [binary index files]      # FAISS vectors
└── lenny-transcripts/            # Source transcripts (302 files)
    ├── Ada Chen Rekhi.txt
    ├── Andrew Chen.txt
    └── ...
```

## Performance Characteristics

- **First query**: ~3-5 seconds (model loading)
- **Subsequent queries**: <2 seconds
- **Index size**: 92MB
- **Memory usage**: ~500MB (model + index in RAM)
- **Search space**: 36,800 chunks

## Common Issues

### Poor Search Results

- User question too vague → Ask for clarification
- No relevant content → Suggest rephrasing
- Keyword-focused question → Explain semantic search benefits

### Slow Performance

- First query always slower (model loading)
- Large context reads slow things down → Limit to top 5-7
- Network issues don't affect this (all local)

### Index Issues

- Missing index → Run `python3 index_transcripts.py`
- Corrupted index → Delete and rebuild
- Outdated index → Rebuild when transcripts change

## Extension Ideas

- Add filtering by guest or date range
- Support follow-up questions with context
- Create topic-based collections
- Add confidence scores to answers
- Generate episode recommendations

## Maintenance

### Adding New Transcripts

1. Add `.txt` files to `lenny-transcripts/`
2. Name files by guest name
3. Delete `lenny-index/` directory
4. Run `python3 index_transcripts.py`
5. Test with queries relevant to new content
6. Commit updated index to repository

### Updating Dependencies

```bash
pip3 install --upgrade txtai sentence-transformers
python3 index_transcripts.py  # Rebuild with new models
```

## Design Philosophy

1. **Pre-built beats custom**: Ship the index, don't make users build it
2. **Fast beats perfect**: 2-second queries with good answers > slow perfection
3. **Citations beat summaries**: Specific quotes > generic advice
4. **Actionable beats comprehensive**: 3-4 takeaways > exhaustive lists
5. **Simple beats complex**: Standalone scripts > frameworks

## Sharing This Skill

To share with product peers:

1. Push to GitHub (or share directory)
2. Include clear installation instructions
3. Provide example queries in README
4. Ensure index is committed (use Git LFS if needed)
5. Test installation on fresh machine

The skill should work immediately after `git clone` + `pip3 install -r requirements.txt`.
