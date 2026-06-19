import requests


def fetch_lever_jobs(company):

    url = (
        f"https://api.lever.co/v0/postings/"
        f"{company}?mode=json"
    )

    try:

        response = requests.get(
            url,
            timeout=20
        )

        if response.status_code != 200:
            return []

        jobs = response.json()

        results = []

        for job in jobs:

            description = (
                job.get(
                    "descriptionPlain"
                )
                or
                job.get(
                    "description"
                )
                or
                ""
            )

            results.append({
                "title": job.get(
                    "text",
                    ""
                ),
                "company": company,
                "location": (
                    job.get(
                        "categories",
                        {}
                    ).get(
                        "location",
                        ""
                    )
                ),
                "description": description,
                "url": job.get(
                    "hostedUrl",
                    ""
                )
            })

        return results

    except Exception as e:
        print(
            f"Lever Error: {e}"
        )
        return []