### **Resumo das Decisões**

**Escolha arquitetural:** **Híbrida** — manter o **core de pagamentos** no monólito Django existente, extrair o componente de **Split** como um serviço interno e um **worker assíncrono** (processo separado) que consome eventos via fila (**RabbitMQ**/**Kafka**).  
**Justificativa:** prazo curto, compatibilidade com o sistema atual e segurança na transição.

---

**Consistência e atomicidade:**  
Adotar **orchestration via events** com **transações sagas idempotentes** + **ledger contábil imutável**.  
- As operações de **charge** (gateway) permanecem no fluxo síncrono do pagamento.  
- A contabilização do **split** ocorrerá em um fluxo eventual, com **compensações** e **locks otimizados**.

---

**Event Sourcing:**  
Não será obrigatório como mecanismo primário (devido à alta complexidade).  
- Implementaremos um **append-only ledger** (tabelas imutáveis de eventos/transactions) para auditoria.  
- O **Event Sourcing completo** ficará no *roadmap* para depois do MVP.

---

**Deploy sem downtime:**  
Usar **Blue/Green** ou **Canary** com **feature flags**.  
- Para o MVP, o deploy será realizado com **containers**.

---

**Métricas críticas:**  
- **Throughput** (transações por segundo)  
- **Latência** (gateway charge, split processing)  
- **Erros por tipo** (gateway, payout, reconciliation)  
- **Fiscal balance** (sum inbound == sum outbound)  
- **Queue length**  
- **Consumer lag**  
- **Percentual de idempotent replays**  
- **Reconciliation drift** (diferenças em centavos)

---

### **Riscos e Trade-offs**
- Extrair um **microserviço completo** aumentaria a complexidade e a carga de infraestrutura. A abordagem **híbrida** reduz o risco de integração e permite entrega em 6 semanas.  
- **Event Sourcing** garante auditabilidade perfeita, mas demanda mais tempo. Substituímos por **ledger append-only** no banco para cumprir o prazo.
