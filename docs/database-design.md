### Tabelas principais (resumo)

- `split_policy`  
  Colunas: id, product_id, version, status, effective_date, created_by, created_at

- `split_rule`  
  Colunas: id, split_policy_id, recipient_id, type, value_amount_cents, value_percentage, order_index

- `payment` (estender tabela de pagamentos)  
  Adicionar: applied_split_policy_id, amount_cents, currency

- `split_execution` (immutable ledger)  
  Um registro por pagamento com: payment_id, executed_at, total_amount_cents, currency, status, metadata

- `split_execution_line`  
  Linhas detalhando cada recipient: recipient_id, amount_cents, fee_type, payout_status, transaction_ref

- `reconciliation_snapshot`  
  Lançamentos periódicos para auditoria

---

### Integridade financeira

- Usar `BIGINT` ou `NUMERIC` para armazenar centavos (usar `amount_cents` como inteiro para precisão)  
- Constraints no DB: NOT NULL, FK para policy/rule, CHECK(total_lines_sum = total_amount) via triggers ou procedimentos atômicos

---

### Histórico e auditoria

- `split_policy` e `split_rule` são versionadas (**append-only**). Nunca deletar; usar **soft-delete** + transições de status  
- `split_execution` é **append-only** e imutável; somente status pode mudar com registros de eventos de correção

---

### Particionamento

- Particionar `split_execution` por data (monthly) e/ou por tenant (se multi-tenant) para suportar escala de 10k+/h  
- Indexes recomendados: (payment_id), (executed_at), (recipient_id, status)
