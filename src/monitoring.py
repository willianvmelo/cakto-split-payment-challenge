METRICS = {
    'payments.total': 'counter',
    'payments.succeeded': 'counter',
    'splits.executed': 'counter',
    'splits.failed': 'counter',
    'splits.drift_cents': 'gauge',
    'queue.consumer_lag': 'gauge',
    'payouts.success_rate': 'ratio',
    'payout.latency_millis': 'histogram',
}

ALERTS = [
    {'expr': 'rate(splits.failed[5m]) > 0.01', 'severity': 'P2', 'desc': 'Taxa de falhas de split alta'},
    {'expr': 'splits.drift_cents > 50', 'severity': 'P1', 'desc': 'Divergência financeira detectada (>R$0.50)'},
    {'expr': 'queue.consumer_lag > 5000', 'severity': 'P1', 'desc': 'Fila com grande atraso'},
    {'expr': 'increase(payments.succeeded[1h]) == 0 and increase(payments.total[1h]) > 100', 'severity': 'P0', 'desc': 'Pagamentos sendo recebidos mas splits não executados'},
]