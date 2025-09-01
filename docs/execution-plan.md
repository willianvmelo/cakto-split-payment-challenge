### Sprint 1-2: Foundation (semanas 1-2)

- **Prioridade:** modelagem do banco de dados, especificação da API, contrato de eventos, infraestrutura de filas (RabbitMQ/Kafka em container para dev), esqueleto do app Django.  
- **Entregáveis:** migrations, endpoint `POST /api/v1/splits/` CRUD, testes básicos.  
- **Componentes paralelizáveis:** infraestrutura da fila, model & migration, testes unitários do validator.

---

### Sprint 3-4: Core Implementation (semanas 3-4)

- **Build:** integração com o fluxo de pagamento — ao receber **PAYMENT_SUCCEEDED**, produzir evento; worker consome e executa o split → grava ledger → tenta payouts ou registra payout.  
- **Marcos:** teste end-to-end para um pagamento com 3 recipients; **idempotency** garantida.  
- **Testes:** unitários para rules, integração local (docker-compose com broker + DB), carga leve simulada.  
- **Garantia de qualidade:** cobertura mínima de 80% para módulos críticos.

---

### Sprint 5-6: Production Readiness (semanas 5-6)

- **Critérios de go-live:** testes E2E verdes; **reconciliation** diária mostrando 0 drift; SLA de latência definida; alertas configurados.  
- **Rollback:** feature flag para desabilitar splits (aplicar fallback para pagar o valor inteiro ao criador); banco de dados: manter versão anterior da policy como ativa.  
- **Observabilidade:** dashboards e alertas configurados.
