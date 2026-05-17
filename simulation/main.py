import argparse

from model import Parameters
from simulation.experiments.paper_reproduce import reproduce_paper, omega_sweep


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run 1-DOF project simulations.")
    parser.add_argument(
        "--reproduce-paper",
        action="store_true",
        help="Run the baseline paper reproduction run.",
    )
    parser.add_argument(
        "--omega-sweep",
        action="store_true",
        help="Run the Omega sweep experiment.",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=200,
        help="Number of Omega samples for the sweep.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base = Parameters()

    run_any = args.reproduce_paper or args.omega_sweep
    if not run_any:
        args.reproduce_paper = True

    if args.reproduce_paper:
        reproduce_paper(base)

    if args.omega_sweep:
        omega_sweep(base, n=args.n)


if __name__ == "__main__":
    main()
