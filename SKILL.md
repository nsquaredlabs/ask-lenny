# Ask Lenny Skill

Query Lenny Rachitsky's podcast transcripts using semantic search to get insights from 300+ top founders, PMs, and operators.

## Invocation

```
/asklenny <question>
```

## Examples

```
/asklenny How do successful founders prioritize features?
/asklenny What do top PMs look for when hiring?
/asklenny How should I think about pricing for B2B SaaS?
/asklenny What's the best way to run user research?
```

## Implementation

When this skill is invoked:

1. **Verify Setup**
   - Check that the lenny-index directory exists with config.json and metadata.json
   - If missing, inform the user to run: `python3 index_transcripts.py`
   - Check that txtai is installed: `pip3 list | grep txtai`
   - If missing, inform the user to run: `pip3 install -r requirements.txt`

2. **Run Query**
   - Execute: `python3 query.py "<user's question>"`
   - Parse the JSON output to get the top 10 most relevant segments
   - Each result includes: score, guest name, file, chunk number, and text

3. **Synthesize Answer**
   - Read the top 5-7 results to gather context
   - Identify the most relevant insights from different guests
   - Create a comprehensive answer that:
     - Starts with a brief direct answer (2-3 sentences)
     - Provides 3-4 key insights from different guests with specific quotes
     - Includes actionable takeaways
     - Lists sources at the bottom

4. **Format Response**

Use this structure:

```markdown
## [Brief, clear answer to the question]

[2-3 sentence summary]

### Key Insights

**[Guest Name]** shares that [insight]:
> "[Direct quote from transcript]"

**[Guest Name]** emphasizes [insight]:
> "[Direct quote from transcript]"

**[Guest Name]** recommends [insight]:
> "[Direct quote from transcript]"

### Takeaways

- [Actionable point 1]
- [Actionable point 2]
- [Actionable point 3]

### Sources

- [Guest Name] - Episode with [brief context]
- [Guest Name] - Episode with [brief context]
- [Guest Name] - Episode with [brief context]
```

## Error Handling

- If query.py returns no results, inform the user and suggest rephrasing
- If query.py errors, display the error and suggest checking the installation
- If the question is too vague, ask for clarification before querying

## Performance

- Queries should complete in <2 seconds
- Use only the top 5-7 results for synthesis (don't read all 10 unless needed)
- Focus on quality over quantity in the answer

## Notes

- The index contains 36,800 chunks from 302 podcast transcripts
- Semantic search understands meaning, not just keywords
- Different guests may have conflicting views - present both when relevant
- Always cite sources with guest names
