import tempfile
import unittest
from pathlib import Path

from src.motor_finance_review import create_fictional_agreements, review_agreement, review_agreements, write_csv
from src.reporting import build_dashboard, build_governance_summary, summarise


class MotorFinanceReviewTests(unittest.TestCase):
    def setUp(self):
        self.raw = create_fictional_agreements()
        self.reviewed = review_agreements(self.raw)

    def test_population_has_100_agreements(self): self.assertEqual(len(self.raw), 100)
    def test_case_ids_are_unique(self): self.assertEqual(len({x["case_id"] for x in self.raw}), 100)
    def test_generation_is_repeatable(self): self.assertEqual(self.raw, create_fictional_agreements())
    def test_all_outputs_require_human_decision(self): self.assertTrue(all(x["human_decision_required"] for x in self.reviewed))

    def test_pch_is_excluded(self):
        case = review_agreement(dict(self.raw[0], product="PCH"))
        self.assertIn("Personal Contract Hire", case["exclusion_reasons"])

    def test_missing_evidence_needs_investigation_without_exclusion(self):
        case = dict(self.raw[0], product="PCP", key_evidence_complete=False, arrangement_type="DCA", commission_disclosed=False, existing_resolution=False, business_purpose=False, zero_interest=False, lowest_five_percent_apr=False, amount_financed=10_000, commission_paid=1_000)
        self.assertEqual(review_agreement(case)["indicative_status"], "Further investigation")

    def test_dca_can_create_eligible_indicator(self):
        case = dict(self.raw[0], product="PCP", key_evidence_complete=True, duplicate_representatives=False, arrangement_type="DCA", commission_disclosed=False, existing_resolution=False, business_purpose=False, zero_interest=False, lowest_five_percent_apr=False, amount_financed=10_000, commission_paid=1_000, agreement_start="2020-01-01")
        self.assertEqual(review_agreement(case)["indicative_status"], "Indicatively eligible")

    def test_disclosed_commission_does_not_produce_indicator(self):
        case = dict(self.raw[0], arrangement_type="DCA", commission_disclosed=True, product="PCP", key_evidence_complete=True, existing_resolution=False, business_purpose=False, zero_interest=False, lowest_five_percent_apr=False, amount_financed=10_000, commission_paid=1_000, agreement_start="2020-01-01")
        self.assertEqual(review_agreement(case)["indicative_status"], "No redress indicator")

    def test_zero_interest_is_excluded(self): self.assertIn("No interest", review_agreement(dict(self.raw[0], zero_interest=True))["exclusion_reasons"])
    def test_existing_resolution_is_excluded(self): self.assertIn("Prior court/FOS", review_agreement(dict(self.raw[0], existing_resolution=True))["exclusion_reasons"])
    def test_business_purpose_is_excluded(self): self.assertIn("Business-purpose", review_agreement(dict(self.raw[0], business_purpose=True))["exclusion_reasons"])
    def test_vulnerability_is_urgent(self): self.assertEqual(review_agreement(dict(self.raw[0], customer_vulnerability=True))["review_priority"], "Urgent")
    def test_deceased_customer_is_urgent(self): self.assertEqual(review_agreement(dict(self.raw[0], customer_deceased=True))["review_priority"], "Urgent")
    def test_no_redress_for_noneligible_case(self): self.assertEqual(review_agreement(dict(self.raw[0], product="PCH"))["illustrative_total_redress"], 0)
    def test_eligible_redress_is_nonnegative(self): self.assertTrue(all(x["illustrative_total_redress"] >= 0 for x in self.reviewed))
    def test_summary_reconciles_population(self): self.assertEqual(sum(summarise(self.reviewed)["statuses"].values()), 100)

    def test_csv_export(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "data.csv"; write_csv(self.reviewed, path)
            self.assertIn("MF-001", path.read_text(encoding="utf-8"))

    def test_dashboard_control_statement(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "index.html"; build_dashboard(self.reviewed, path)
            self.assertIn("scheme are suspended", path.read_text(encoding="utf-8"))

    def test_dashboard_has_100_rows(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "index.html"; build_dashboard(self.reviewed, path)
            self.assertEqual(path.read_text(encoding="utf-8").count("data-status="), 100)

    def test_governance_report(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "report.md"; build_governance_summary(self.reviewed, path)
            self.assertIn("Management attention", path.read_text(encoding="utf-8"))


if __name__ == "__main__": unittest.main()

