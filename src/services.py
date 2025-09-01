from decimal import Decimal, ROUND_HALF_UP
from typing import List

# Helpers
def cents_from_decimal(d: Decimal) -> int:
    # garantindo arredondamento financeiro
    return int((d * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))


def compute_split_lines(total_cents: int, rules: List[dict]) -> List[dict]:
    """    
    retorna lista com amount_cents por recipient, garantindo soma == total_cents
    """
    # 1) calcular valores iniciais
    lines = []
    remaining = total_cents

    
    percent_rules = [r for r in rules if r['type'] == 'percentage']
    fixed_rules = [r for r in rules if r['type'] == 'fixed']

    
    total_pct_bp = sum(r['value'] for r in percent_rules)
    if total_pct_bp > 10000:
        raise ValueError('sum of percentage rules exceeds 100%')

    allocated = 0
    for r in percent_rules:
        amt = (total_cents * r['value']) // 10000
        lines.append({'recipient_id': r['recipient_id'], 'amount_cents': amt})
        allocated += amt

    for r in fixed_rules:
        amt = r['value']
        lines.append({'recipient_id': r['recipient_id'], 'amount_cents': amt})
        allocated += amt

    
    remainder = total_cents - allocated
    if remainder != 0:
        
        fee_idx = next((i for i, l in enumerate(lines) if l['recipient_id'] == 'cakto_fee'), 0)
        lines[fee_idx]['amount_cents'] += remainder

    
    if sum(l['amount_cents'] for l in lines) != total_cents:
        raise RuntimeError('allocation error - sums do not match')

    return lines


# Idempotent worker pseudocódigo
class SplitWorker:
    def __init__(self, db, payout_gateway, logger):
        self.db = db
        self.payout_gateway = payout_gateway
        self.logger = logger

    def on_payment_succeeded(self, event):
        payment_id = event['payment_id']
        # idempotency guard
        if self.db.split_execution_exists(payment_id):
            self.logger.info('split already executed for %s', payment_id)
            return

        payment = self.db.get_payment(payment_id)
        policy = self.db.get_active_policy(payment['product_id'])
        if not policy:
            self.logger.info('no split policy, skipping')
            # create an execution record marking no-split
            self.db.create_split_execution(payment_id, payment['amount_cents'], payment['currency'], [])
            return

        # compute allocation
        rules = []
        for r in policy['rules']:
            if r['type'] == 'percentage':
                rules.append({'type': 'percentage', 'value': int(r['value'] * 100), 'recipient_id': r['recipient_id']})
            else:
                rules.append({'type': 'fixed', 'value': r['value_cents'], 'recipient_id': r['recipient_id']})

        lines = compute_split_lines(payment['amount_cents'], rules)

        # create split_execution ledger (PENDING)
        execution_id = self.db.create_split_execution(payment_id, payment['amount_cents'], payment['currency'], lines)

        # try payouts (async, mark line statuses)
        for line in lines:
            try:
                payout_ref = self.payout_gateway.create_payout(line['recipient_id'], line['amount_cents'], payment['currency'])
                self.db.update_split_line(execution_id, line['recipient_id'], payout_status='SUCCESS', transaction_ref=payout_ref)
            except Exception as e:
                self.db.update_split_line(execution_id, line['recipient_id'], payout_status='FAILED')
                self.logger.exception('payout failed for %s', line['recipient_id'])

        # finalize execution status
        self.db.finalize_execution(execution_id)