from app.services.greenhouse import (
    fetch_greenhouse_jobs
)

from app.services.lever import (
    fetch_lever_jobs
)


def fetch_all_jobs():

    jobs = []

    greenhouse_companies = [
        "airbnb",
        "stripe",
        "datadog"
    ]

    lever_companies = [
        "netflix",
        "shopify"
    ]

    for company in greenhouse_companies:

        jobs.extend(
            fetch_greenhouse_jobs(
                company
            )
        )

    for company in lever_companies:

        jobs.extend(
            fetch_lever_jobs(
                company
            )
        )

    return jobs