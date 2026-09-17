"""Generate the fictional dataset, dashboard and governance report."""

from pathlib import Path

from src.motor_finance_review import create_fictional_agreements, review_agreements, write_csv
from src.reporting import build_dashboard, build_governance_summary


ROOT = Path(__file__).resolve().parent


def main() -> None:
    agreements = review_agreements(create_fictional_agreements())
    write_csv(agreements, ROOT / "data" / "fictional_motor_finance_agreements.csv")
    build_dashboard(agreements, ROOT / "docs" / "index.html")
    build_governance_summary(agreements, ROOT / "reports" / "governance_summary.md")
    print(f"Generated {len(agreements)} fictional motor finance reviews")
    print(f"Dashboard: {ROOT / 'docs' / 'index.html'}")


if __name__ == "__main__":
    main()

