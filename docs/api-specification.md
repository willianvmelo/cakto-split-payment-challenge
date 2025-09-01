### Endpoints principais (MVP)


<summary><strong>POST /api/v1/splits/</strong></summary>
Cria ou atualiza uma **política de split** para um produto/loja.



<summary><strong>GET /api/v1/splits/{id}/</strong></summary>
Retorna os **detalhes da policy**.



<summary><strong>POST /api/v1/payments/</strong></summary>
Endpoint existente de pagamento; quando aceito, emite evento **PAYMENT_SUCCEEDED** com os seguintes dados:  
`payment_id`, `order_id`, `amount`, `currency`, `product_id`, `applied_split_id`.


---

### Exemplo de payload de criação de split
```json
{
  "product_id": "prod_abc123",
  "rules": [...],
  "effective_date": "2024-01-01T00:00:00Z"
}
```

---

### Validações de negócio


<summary><strong>Regras de validação</strong></summary>

- Soma das regras do tipo `percentage` não pode exceder 100.00%.  
- Valores de `fixed` + `percentage` combinados não podem exceder o total da venda.  
- Cada `recipient_id` deve estar ativo e com dados de conta válidos quando a regra exigir.  
- Regras devem ter `currency` compatível com o produto.  
- `cakto_fee` obrigatório/permitido com limite máximo configurável por cliente.



---

### Estados possíveis de um split


<summary><strong>Estados</strong></summary>

- `DRAFT` — criado, não aplicado  
- `ACTIVE` — em produção (aplicável a novos pagamentos)  
- `RETIRED` — desativado (não aplicável a novos pagamentos)  
- `ARCHIVED` — histórico



---

### Alterações de configuração


<summary><strong>Versionamento e alterações</strong></summary>

- Alterações geram **nova versão de policy** (versionamento sem sobrescrever histórico).  
- Aplicação retroativa: somente com workflow explícito (reconciliação manual); por padrão, **effective_date** aplica-se apenas a pagamentos futuros.



---

### Versionamento de API


<summary><strong>Controle de versões</strong></summary>

- `/api/v1/...` — versão inicial. Para alterações breaking, usar `v2` e manter **translator/adapter** para compatibilidade.  
- Use headers `Accept: application/vnd.cakto.v1+json` para controle fino.


