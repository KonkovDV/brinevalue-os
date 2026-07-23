import argparse, sys, json
from .io import synthetic_streams, load_table
from .pipeline import analyze
from .report import html_report


def cmd_demo(a):
    b = synthetic_streams(a.n, seed=a.seed)[a.index]
    res = analyze(b)
    print(json.dumps({k: res[k] for k in ("stream", "qc", "mg_li", "scaling_index", "decision")},
                     ensure_ascii=False, indent=2))
    bb = res["best"]
    print(f"BEST: {bb['scheme']} | NPV {bb['npv_rub']} руб | {bb.get('prod_cost_usd_t')} $/т Li2CO3 | ROROI {bb.get('roroi')}")
    print("TOP SENSITIVITY:", list(res["sensitivity"]["elasticity"].items())[:3])
    print("EXPERIMENT PLAN:", [e["experiment"] for e in res["experiment_plan"]["plan"]])
    if a.report:
        open(a.report, "w", encoding="utf-8").write(html_report(res, b, res["sensitivity"], res["experiment_plan"]))
        print("report ->", a.report)


def cmd_screen(a):
    for b in load_table(a.table):
        r = analyze(b, with_doe=False, with_scenarios=False)
        print(f"{b.name}: {r['decision']:8s} best={r['best']['scheme']:14s} NPV={r['best']['npv_rub']}")


def cmd_surrogate(a):
    from .surrogate import train_surrogate
    s = train_surrogate(n=a.n, seed=a.seed)
    print(f"surrogate R2 (5-fold CV): {s['cv_r2_mean']} +/- {s['cv_r2_std']} on n={s['n']}")
    print("feature importances:", json.dumps(s["importances"], ensure_ascii=False))


def main(argv=None):
    p = argparse.ArgumentParser(prog="brinevalue"); sub = p.add_subparsers(required=True)
    d = sub.add_parser("demo"); d.add_argument("--n", type=int, default=8); d.add_argument("--index", type=int, default=0)
    d.add_argument("--seed", type=int, default=0); d.add_argument("--report", default=None); d.set_defaults(func=cmd_demo)
    s = sub.add_parser("screen"); s.add_argument("table"); s.set_defaults(func=cmd_screen)
    g = sub.add_parser("surrogate"); g.add_argument("--n", type=int, default=300); g.add_argument("--seed", type=int, default=0); g.set_defaults(func=cmd_surrogate)
    a = p.parse_args(argv); a.func(a)


if __name__ == "__main__":
    main()
