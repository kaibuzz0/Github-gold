"""Regression tests for GitHub Gold score/tier validation."""
import unittest
from catalog_audit import Audit, expected_tier, validate_entry


class TierValidationTests(unittest.TestCase):
    def test_all_155_score_tier_combinations(self):
        tiers = ("S", "A", "B", "C", "D")
        accepted = 0
        rejected = 0
        for score in range(31):
            for tier in tiers:
                with self.subTest(score=score, tier=tier):
                    audit = Audit()
                    entry = {
                        "name": "fixture",
                        "repository": "https://github.com/example/fixture",
                        "evidence": "VERIFIED",
                        "score": score,
                        "tier": tier,
                        "license": "MIT",
                    }
                    validate_entry(entry, where="fixture", score_key="score", tier_key="tier", audit=audit)
                    if tier == expected_tier(score):
                        self.assertEqual(audit.errors, [])
                        accepted += 1
                    else:
                        self.assertEqual(len(audit.errors), 1)
                        rejected += 1
        self.assertEqual((accepted, rejected), (31, 124))

    def test_boolean_score_is_invalid(self):
        audit = Audit()
        validate_entry({"name": "fixture", "repository": "https://github.com/example/fixture",
                        "evidence": "VERIFIED", "score": True, "tier": "D", "license": "MIT"},
                       where="fixture", score_key="score", tier_key="tier", audit=audit)
        self.assertEqual(len(audit.errors), 1)

    def test_provisional_queue_keys_are_checked(self):
        audit = Audit()
        validate_entry({"name": "fixture", "repository": "https://github.com/example/fixture",
                        "evidence": "PROMISING", "provisional_score": 25,
                        "provisional_tier": "S", "license": "MIT"},
                       where="fixture", score_key="provisional_score",
                       tier_key="provisional_tier", audit=audit)
        self.assertEqual(len(audit.errors), 1)


if __name__ == "__main__":
    unittest.main()
