import os
import tempfile

from utils import now_iso, print_json
import db as dbmod

def run_self_test():
    fd, path = tempfile.mkstemp(prefix="sqlite_manager_", suffix=".db")
    os.close(fd)

    results = {
        "timestamp": now_iso(),
        "db": path,
        "tests": []
    }

    try:
        dbmod.init_db(path)
        ok, msg = dbmod.healthcheck(path)
        results["tests"].append({
            "name": "healthcheck_after_init",
            "passed": ok,
            "message": msg
        })

        dbmod.seed(path, now_iso())
        counts = dbmod.table_row_counts(path)
        passed_counts = (counts.get("users", 0) >= 1) and (counts.get("notes", 0) >= 1)
        results["tests"].append({
            "name": "seed_and_counts",
            "passed": passed_counts,
            "counts": counts
        })

        results["overall_passed"] = all(t["passed"] for t in results["tests"])
    except Exception as e:
        results["overall_passed"] = False
        results["error"] = str(e)
    finally:
        try:
            os.remove(path)
        except OSError:
            pass

    return results

if __name__ == "__main__":
    print_json(run_self_test())
