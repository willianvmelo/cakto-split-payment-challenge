# cakto-split-payment-challenge

### Objetivo
Implementar um MVP de Split Payments para permitir que receitas de vendas sejam automaticamente divididas entre múltiplos recipientes (criadores, parceiros, taxa da plataforma), atendendo restrições de precisão financeira, escalabilidade e observabilidade, para entrega em 6 semanas.

### Estrutura do repositório
```
cakto-split-payment-challenge/
├── README.md
├── docs/
│   ├── architecture-decisions.md
│   ├── api-specification.md
│   ├── database-design.md
│   └── execution-plan.md
├── src/
│   ├── models.py
│   ├── services.py
│   ├── tests.py
│   └── monitoring.py
└── docker-compose.yml
```

### Como usar (local / docker)
1. Clonar o repositório
2. `docker-compose up --build` (cria DB e app ilustrativo)
3. API exposta em `http://localhost:8000` (exemplo)

Obs: O código aqui é um esqueleto funcional focado na lógica de split, testes e observabilidade. É intencionalmente simples para caber no MVP de 6 semanas.

