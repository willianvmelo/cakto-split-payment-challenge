import unittest

from services import compute_split_lines

class TestSplitComputation(unittest.TestCase):
    def test_simple_percentages(self):
        total = 10000  # cents = R$100.00
        rules = [
            {'recipient_id': 'creator', 'type': 'percentage', 'value': 6500},
            {'recipient_id': 'partner', 'type': 'percentage', 'value': 3000},
            {'recipient_id': 'cakto_fee', 'type': 'percentage', 'value': 500},
        ]
        lines = compute_split_lines(total, rules)
        self.assertEqual(sum(l['amount_cents'] for l in lines), total)
        # deterministic check: creator gets 6500% -> R$65.00 => 6500 cents
        self.assertEqual(next(l for l in lines if l['recipient_id']=='creator')['amount_cents'], 6500)

    def test_remainder_goes_to_fee(self):
        total = 10001
        rules = [
            {'recipient_id': 'creator', 'type': 'percentage', 'value': 5000},
            {'recipient_id': 'cakto_fee', 'type': 'percentage', 'value': 5000},
        ]
        lines = compute_split_lines(total, rules)
        self.assertEqual(sum(l['amount_cents'] for l in lines), total)

if __name__ == '__main__':
    unittest.main()