import argparse
import os

from utils import now_iso, print_json
import db as dbmod

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="sqlite-manager",
        description="SQLite Manager Tool (init, seed, list, report) - JSON output"
    )
    p.add_argument(
        "--db",
        default=os.environ.get("DB_PATH", dbmod.DEFAULT_DB_PATH),
        help="Path to sqlite db file (default: data/app.db)"
    )

    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init", help="Create database & tables")
    sub.add_parser("seed", help="Insert sample data")
    sub.add_parser("list", help="List tables")
    sub.add_parser("report", help="Print JSON report (status, tables, counts)")
    return p

def cmd_init(db_path: str):
    dbmod.init_db(db_path)
    ok, msg = dbmod.healthcheck(db_path)
    print_json({
        "timestamp": now_iso(),
        "action": "init",
        "db": db_path,
        "status": "success" if ok else "failed",
        "message": msg
    })

def cmd_seed(db_path: str):
    created = now_iso()
    dbmod.init_db(db_path)
    dbmod.seed(db_path, created)
    print_json({
        "timestamp": now_iso(),
        "action": "seed",
        "db": db_path,
        "status": "success",
        "seeded_at": created
    })

def cmd_list(db_path: str):
    tables = dbmod.list_tables(db_path)
    print_json({
        "timestamp": now_iso(),
        "action": "list",
        "db": db_path,
        "tables": tables
    })

def cmd_report(db_path: str):
    ok, msg = dbmod.healthcheck(db_path)
    tables = dbmod.list_tables(db_path) if ok else []
    counts = dbmod.table_row_counts(db_path) if ok else {}
    print_json({
        "timestamp": now_iso(),
        "action": "report",
        "db": db_path,
        "health": {"ok": ok, "message": msg},
        "tables": tables,
        "row_counts": counts
    })

def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.cmd == "init":
        cmd_init(args.db)
    elif args.cmd == "seed":
        cmd_seed(args.db)
    elif args.cmd == "list":
        cmd_list(args.db)
    elif args.cmd == "report":
        cmd_report(args.db)

if __name__ == "__main__":
    main()
