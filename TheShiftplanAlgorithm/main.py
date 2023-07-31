import sys
import logging
from logFormatter import LogFormatter

import fetch_json_data as db
from solution import Solution



try:
    from colorama import init
    init()
except ImportError:
    pass

LEVEL = logging.DEBUG
if "info" in sys.argv:
    LEVEL = logging.INFO
elif "debug" in sys.argv:
    LEVEL = logging.DEBUG
elif "warn" in sys.argv:
    LEVEL = logging.WARN
elif "critical" in sys.argv:
    LEVEL = logging.CRITICAL
elif "error" in sys.argv:
    LEVEL = logging.ERROR

logger = logging.getLogger("")
logger.setLevel(LEVEL)
ch = logging.StreamHandler()
ch.setLevel(LEVEL)
ch.setFormatter(LogFormatter())

logger.addHandler(ch)

if __name__ == '__main__':
    shiftplan = db.fetch_shiftplan()
    # print(shiftplan["mode_name"])
    jts = db.fetch_jobtypes()
    jobs = db.fetch_jobs(*list(jts["pk"]))
    users = db.fetch_users()
    subcrews = db.fetch_subcrews()
    preferences = db.fetch_preferences(users, jobs)
    # print("Users\n", users)
    # print()
    # print("preferences\n", preferences)
    # print(len(users.index), len(preferences.index))
    mn = shiftplan["mode_name"]
    if mn == "assign_every_job":
        from assign_every_job_model import AssignEveryJobModel as Model_class
    elif mn == "non_prioritized":
        from non_prioritized_model import NonPrioritizedModel as Model_class
    elif mn == "prioritized":
        from prioritized_model import PrioritizedModel as Model_class
    else:
        logging.error(f"Invalid mode: {mn}.")
        exit()
    logging.info(f"Creating {mn} model.")
    model = Model_class(jobs=jobs, persons=users, preferences=preferences, jobtypes=jts, shiftplan=shiftplan, subcrews=subcrews)
    
    s = Solution(model)