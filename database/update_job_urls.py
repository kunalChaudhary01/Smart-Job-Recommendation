"""Assign verified careers / official job URLs for Indian company postings."""
import sys
sys.path.insert(0, r"d:\Projects\smart-job-recommendation")

from database.db_config import get_connection

OFFICIAL_COMPANY_URLS = {
    1: "https://www.tcs.com/careers",
    2: "https://www.infosys.com/careers.html",
    3: "https://careers.wipro.com/",
    4: "https://www.flipkartcareers.com/",
    5: "https://careers.techmahindra.com/",
    6: "https://www.zoho.com/careers/",
    7: "https://www.hcltech.com/careers",
    8: "https://careers.swiggy.com/",
    9: "https://www.ltimindtree.com/careers/",
    10: "https://razorpay.com/jobs/",
    11: "https://www.zomato.com/careers",
    12: "https://careers.cognizant.com/global/en",
    13: "https://www.capgemini.com/careers/",
    14: "https://www.freshworks.com/company/careers/",
    15: "https://www.persistent.com/careers/"
}

conn = get_connection()
cursor = conn.cursor()

for job_id, url in OFFICIAL_COMPANY_URLS.items():
    cursor.execute(
        "UPDATE jobs SET application_url = %s WHERE id = %s",
        (url, job_id)
    )

conn.commit()
print("Updated official career URLs for all 15 Indian tech employer postings.")

# Verify all jobs now have application_url
cursor.execute("SELECT id, title, company, application_url FROM jobs")
for r in cursor.fetchall():
    print(f"#{r[0]} {r[1][:25]} | {r[2][:15]} | {r[3][:60]}")

cursor.close()
conn.close()
