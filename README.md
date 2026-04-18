# MEMORA

## SYSTEM ARCHITECTURE

```
                ┌────────────────────┐
                │   Raw Files        │
                │ (pdf/txt/md)       │
                └────────┬───────────┘
                         ↓
                ┌────────────────────┐
                │   Converter        │
                │ (→ markdown)       │
                └────────┬───────────┘
                         ↓
                ┌────────────────────┐
                │ Markdown Storage   │
                │ (source of truth)  │
                └────────┬───────────┘
                         ↓
                ┌────────────────────┐
                │ Index Builder      │
                │ (index.json)       │
                └────────┬───────────┘
                         ↓
                ┌────────────────────┐
                │ Chunk + Embed      │
                └────────┬───────────┘
                         ↓
                ┌────────────────────┐
                │ Qdrant Vector DB   │
                └────────┬───────────┘
                         ↓
User Query → Embed → Retrieve → Prompt → LLM → Answer
```

## SYSTEM ARCHITECTURE

```
memora/
│
├── data/
│   ├── raw/                     # pdf, txt inputs
│   ├── processed/               # converted markdown files
│   └── index.json               # metadata index
│
├── db/
│   └── qdrant_client.py         # DB connection & setup
│
├── core/
│   ├── loader.py                # load markdown files
│   ├── chunker.py               # semantic chunking
│   ├── embedder.py              # embeddings
│   ├── retriever.py             # query vector DB
│   ├── prompt.py                # prompt templates
│   └── utils.py
│
├── ingestion/
│   ├── converter.py             # pdf/txt → md
│   ├── indexer.py               # builds index.json
│   └── ingest.py                # full ingestion pipeline
│
├── rag/
│   ├── pipeline.py              # orchestrates RAG flow
│   └── query.py                 # query handler
│
├── knowledge/
│   ├── editor.py                # view/edit markdown
│   ├── linker.py                # detect [[links]]
│   └── graph.py                 # build note graph
│
├── interface/
│   ├── cli.py                   # CLI interface
│   └── api.py                   # FastAPI (future)
│
├── config/
│   └── settings.py              # chunk size, top_k, model configs
│
├── tests/
│
├── main.py
├── requirements.txt
└── README.md
```

## DATA FLOW

```
## Ingestion
raw → convert → markdown → index → chunk → embed → Qdrant

## Query
query → embed → retrieve → filter → prompt → LLM → answer
```