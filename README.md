# simple_AI_agent_LLMS
AI-powered search agent that connects to ChatGPT and Claude, understands user queries, retrieves relevant information, and returns the most accurate and helpful response based on the input.
## Overview

This project implements a lightweight AI search agent that connects to multiple LLM providers (ChatGPT / OpenAI and Claude / Anthropic), accepts user queries, searches a local knowledge source, and returns the most relevant, concise answer by combining retrieval + LLM reasoning. It is intended as a small, extensible reference implementation rather than a production system.

## Key features

- Multi-LLM orchestration: send prompts to one or more LLM providers and aggregate results.
- Retrieval-augmented responses: find relevant documents/snippets before asking the LLM.
- Simple decision layer: choose or combine LLM outputs for the most accurate reply.
- Easy to extend: swap retriever, vector store, or LLM client with minimal changes.

## Architecture (high level)

- CLI / API layer — accepts user queries and options.
- Query parser — normalizes and sanitizes incoming text.
- Retriever — searches the local knowledge base (files or vector index) and returns top candidates.
- LLM clients — small adapters for OpenAI/Claude that format prompts and handle rate/response differences.
- Response selector — ranks/filters LLM outputs, optionally merges answers.
- Utilities — caching, logging, configuration (API keys, timeouts).

## Getting started

1. Clone the repo and open the devcontainer (already provided in this workspace).
2. Install dependencies:
    - Typically: pip install -r requirements.txt
3. Provide API keys in environment variables or a .env file:
    - OPENAI_API_KEY=your_key
    - CLAUDE_API_KEY=your_key
4. Prepare or index your knowledge data (see data/ or scripts/ for indexing helpers).
5. Run the agent (example CLI):
    - python -m src.agent --query "What is the recommended retry pattern for network requests?"

Adjust command names to match the repository layout (look in src/ or top-level scripts).

## Code layout (example)

- src/
  - agent.py — main orchestration and CLI entrypoint
  - retriever.py — search/index helpers
  - llm_clients.py — OpenAI & Claude adapters
  - selector.py — logic to pick/merge LLM responses
  - utils.py — config, logging, and helpers
- data/ — documents, indices, and example content
- requirements.txt — Python dependencies
- tests/ — unit / integration tests

(If file names differ slightly, map the concepts above to the actual files in the repository.)

## How the code works (brief)

1. Input arrives at src.agent: parsed and validated.
2. The retriever identifies a small set of relevant passages.
3. A prompt template is filled with the user query + retrieved context.
4. Prompt(s) are sent to one or more LLM clients in parallel or sequence.
5. The selector compares outputs (confidence heuristics, length, overlap) and returns the final response.
6. Optional: store the conversation or feedback for future tuning.

## Interaction tips

- Be explicit: include what you want (format, length, tone). Eg: "Summarize in 3 bullet points."
- Provide context: if asking about a repo or document, include the document name or paste the relevant snippet.
- Ask follow-ups: if the answer is unclear, ask the agent to "explain step 2" or "show sources".
- Control verbosity: specify "short answer" vs "detailed explanation".
- Use feedback: mark outputs as correct/incorrect to improve future selection logic (if implemented).

## Troubleshooting

- If LLM calls fail: verify API keys and network access.
- If retrieval returns poor results: re-index data or expand the retriever window/top-k.
- If responses are inconsistent across LLMs: try prompting templates or prefer a single trusted provider.

## Extending the agent

- Add a new LLM client by implementing the adapter interface in src/llm_clients.py.
- Swap the retriever for a vector DB (FAISS, Milvus) by replacing retriever.py internals.
- Improve selection by adding rescoring or a lightweight verification LLM pass.

## Contributing & License

- Follow existing coding patterns and add tests for new features.
- Include a short description and examples for any new prompt templates.
- Check the LICENSE file for project licensing information.

For quick reference, open the main entrypoint file (src/agent.py) to see runtime options and example invocations.