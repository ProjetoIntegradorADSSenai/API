```mermaid
classDiagram
    class Peca {
        +id: INT (PK)
        +tipo: VARCHAR(255)
        +separacoes: Separacao[]
    }

    class Separacao {
        +id: INT (PK)
        +id_peca: INT (FK)
        +horario_inicial: TIMESTAMP
        +horario_fim: TIMESTAMP
    }

    class AgregacaoView {
        +peca_tipo: VARCHAR(255)
        +time_interval: DATETIME
        +total_separacoes: INT
        +avg_duration_seconds: FLOAT
        +min_duration: INT
        +max_duration: INT
    }

    Peca "1" -- "0..*" Separacao : has
    Separacao -- AgregacaoView : contributes to
```