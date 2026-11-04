podcastiq/
│
├── backend/
│   └── app/
│       ├── main.py
│       ├── api/
│       │   └── v1/
│       │       ├── sessions.py
│       │       ├── ingestion.py
│       │       └── chat.py
│       │
│       │
│       ├── schemas/
│       │   ├── session.py
│       │   ├── ingestion.py
│       │   └── chat.py
│       │
│       ├── services/
│       │   ├── session_service.py
│       │   ├── transcript_service.py
│       │   ├── ingestion_service.py
│       │   ├── chunking_service.py
│       │   ├── embedding_service.py
│       │   ├── retrieval_service.py
│       │   ├── generation_service.py
│       │   └── cleanup_service.py
│       │
│       ├── repositories/
│       │   ├── session_repository.py
│       │   └── vector_repository.py
│       │
│       ├── workers/
│       │   ├── celery_app.py
│       │   ├── ingestion_tasks.py
│       │   └── cleanup_tasks.py
│       │
│       └── dependencies/
│           └── providers.py
│

├── .env.example
├── .gitignore
├── compose.yaml
├── pyproject.toml
├── uv.lock
└── README.md