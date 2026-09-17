# Bridge Dosya Durumları

```mermaid
stateDiagram-v2
    [*] --> Inbox
    Inbox --> Processing: atomik sahiplenme
    Processing --> Archive: processed=true
    Processing --> Inbox: geçici hata ve retry
    Processing --> Rejected: şema hatası veya limit
    Archive --> [*]
    Rejected --> [*]
```

