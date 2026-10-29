"""Filter and clean all existing jobs in the database to ensure they are strictly Remote or India-based."""
import sys
sys.path.insert(0, r"d:\Projects\smart-job-recommendation")

from database.db_config import get_connection
from utils.job_fetcher import is_remote_or_india

conn = get_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute("SELECT id, title, company, location, job_type FROM jobs")
all_jobs = cursor.fetchall()

removed = 0
retained = 0

for j in all_jobs:
    is_valid, j_type, norm_loc = is_remote_or_india(j["location"], is_remote_flag=(j["job_type"] == "Remote"))
    if not is_valid:
        print(f"Removing non-India/non-remote job: #{j['id']} {j['title']} at {j['company']} ({j['location']})")
        cursor.execute("DELETE FROM jobs WHERE id = %s", (j["id"],))
        removed += 1
    else:
        # Normalize job_type to Remote if location signifies remote
        if j_type == "Remote" and j["job_type"] != "Remote":
            cursor.execute("UPDATE jobs SET job_type = 'Remote', location = %s WHERE id = %s", (norm_loc, j["id"]))
        retained += 1

conn.commit()
print(f"\nCleanup summary: Retained {retained} jobs, Removed {removed} non-compliant jobs.")

# Verify remaining jobs
cursor.execute("SELECT id, title, company, location, job_type FROM jobs")
remaining = cursor.fetchall()
print(f"Total verified jobs in database: {len(remaining)}")
for r in remaining:
    print(f"  #{r['id']} {r['title']} | {r['company']} | Location: {r['location']} | Type: {r['job_type']}")

cursor.close()
conn.close()
