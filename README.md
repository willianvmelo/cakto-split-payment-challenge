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

**Importante:** O código presente no diretório `src/` é um **esqueleto funcional** que simula a lógica de split, com testes e métricas.  
Não é um projeto Django completo, mas foi feito para que seja possível rodar o MVP em Docker, consumir eventos e verificar a lógica de divisão de pagamentos.  
A integração com o Django real do core de pagamentos seria feita posteriormente, aproveitando este módulo containerizado.

### Funcionalidades incluídas
- Lógica de cálculo de splits com precisão financeira
- Registro contábil imutável (ledger)
- Testes unitários e de integração
- Simulação de eventos assíncronos (fila)
- Métricas básicas e alertas de monitoramento


