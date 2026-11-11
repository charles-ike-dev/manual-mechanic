# ChatIVG

AI assistant for vehicle technicians. Ask questions about workshop and service documentation (maintenance intervals, gearbox procedures, CAN networks, connector pin-outs, DTCs) and get answers grounded in the manuals, with the source passages shown alongside.

The current iteration (`v20`) targets the **Iveco S-WAY AS** documentation and uses a fine-tuned `gpt-4o-mini` model on top of retrieval-augmented generation (RAG).

## How it works

```
docs/  (manuals: XML, PDF, TXT, ...)
   │
   ▼
worker/  ── Python: parse, chunk, embed ──►  Pinecone index (one namespace per version)
                                                   │
webapp/  ── Next.js chat UI ── /api/chat/retrieval ┘
              │
              └─ condense question → retrieve chunks → answer with OpenAI model → stream + sources
```

- **Ingestion** (`worker/`): walks a docs folder, parses each file (a custom loader for the eTIM XML manuals, `PyPDFLoader` for PDFs, `unstructured` for everything else), splits it into 1000-character chunks, and embeds them with `text-embedding-3-large` into a Pinecone namespace.
- **Chat** (`webapp/`): a LangChain retrieval chain rewrites follow-up questions into standalone ones, retrieves relevant chunks from the version's namespace, and streams an answer. The retrieved documents are returned with the response so the UI can show them as sources.
- **Fine-tuning** (`worker/finetuning/`): builds a question/answer dataset from expert-written reference answers, expands it with generated paraphrases, and trains an OpenAI fine-tuned model used by the chat.

## Repository layout

```
.
├── webapp/                 Next.js 14 app (App Router, Tailwind, Vercel AI SDK)
│   └── src/
│       ├── app/(protected)/vN/   One chat page per iteration (model, namespace, system prompt)
│       ├── app/api/chat/         Chat endpoints (retrieval chain lives in retrieval/route.ts)
│       ├── app/api/auth/         Login / logout
│       ├── lib/config.ts         Active version users are redirected to
│       └── middleware.ts         Auth gate
├── worker/                 Python ingestion scripts
│   ├── v5.py               Current ingestion script (docs/v20 → namespace v20)
│   ├── v1.py … v4.py       Earlier ingestion scripts, kept for reference
│   ├── UI_loader.py        Loader for eTIM XML manuals
│   ├── remove_old_version.py  Keeps only the latest version of each IU_<id>_<n>.xml file
│   └── finetuning/         Dataset generation, validation and fine-tuning jobs
├── questions.json          Reference test questions (Italian)
└── questions_EN.json       Same questions in English
```

The `docs/` folder holds the source manuals and is git-ignored; you need to supply it locally.

## Prerequisites

- Node.js 18+
- Python 3.12+ (the ingestion scripts use 3.12 f-string syntax)
- An [OpenAI](https://platform.openai.com/) API key
- A [Pinecone](https://www.pinecone.io/) index with **dimension 3072** (matches `text-embedding-3-large`)
- For non-XML/PDF files, `unstructured` may need system packages such as Tesseract, Poppler and libmagic

## Setup

### 1. Environment variables

Create `webapp/.env.local` and `worker/.env` (both are git-ignored):

| Variable | Used by | Description |
|---|---|---|
| `OPENAI_API_KEY` | webapp, worker | OpenAI API key |
| `PINECONE_API_KEY` | webapp, worker | Pinecone API key |
| `PINECONE_INDEX` | webapp, worker | Name of the Pinecone index |
| `OPENAI_MODEL` | webapp | Fallback model when a page doesn't set one (default `gpt-3.5-turbo`) |
| `ALLOWED_EMAILS` | webapp | Comma-separated list of emails allowed to log in |
| `ALLOWED_PASSWORD` | webapp | Shared password for those emails |

### 2. Ingest the documentation

```bash
cd worker
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Place the manuals in ../docs/v20, then:
python remove_old_version.py     # optional: drop superseded XML versions
python v5.py
```

Each file that is ingested successfully is moved to `docs/v20/processed/`, so you can re-run the script after a failure and it will only pick up what's left. Errors are written to `worker/error.log`.

### 3. Run the web app

```bash
cd webapp
npm install
npm run dev
```

Open http://localhost:3000, log in with one of the allowed emails, and you'll be redirected to the active version's chat page.

## Adding a new iteration

1. Point `DIR_PATH` and `NAMESPACE` in the ingestion script at the new docs folder/namespace and run it.
2. Copy the latest `webapp/src/app/(protected)/vN/` page to `vN+1/` and update `MODEL`, `NAMESPACE` and `SYSTEMPROMPT`.
3. Set `version` in `webapp/src/lib/config.ts` to the new page and add it to the list in `home/page.tsx`.

## Fine-tuning

From `worker/finetuning/`, run in order:

1. `generate_alternatives.py`: generates paraphrased variants of the reference questions
2. `data_formatting.py`: converts the dataset into OpenAI chat-format JSONL
3. `data_validation.py`: checks format and token counts
4. `fine_tuning.py`: uploads the file and manages the fine-tuning job

Then set the resulting `ft:...` model ID as `MODEL` in the chat page. The input file names are hard-coded at the top of each script, so update them for a new dataset.

## Known limitations

- Authentication is a lightweight demo gate (shared password, plain `authenticated` cookie). Put proper auth in front of it before exposing it publicly.
- `/api/*` routes are not covered by the middleware auth check.
