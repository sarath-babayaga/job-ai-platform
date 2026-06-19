import requests


def fetch_greenhouse_jobs(board):

    url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true"

    try:

        response = requests.get(
            url,
            timeout=20
        )

        if response.status_code != 200:
            return []

        jobs = response.json().get(
            "jobs",
            []
        )

        results = []

        for job in jobs:

            results.append({
                "title": job.get("title", ""),
                "company": board,
                "location": (
                    job.get(
                        "location",
                        {}
                    ).get(
                        "name",
                        ""
                    )
                ),
                "description": (
                    job.get(
                        "content",
                        ""
                    )
                ),
                "url": job.get(
                    "absolute_url",
                    ""
                )
            })

        return results

    except Exception as e:
        print(
            f"Greenhouse Error: {e}"
        )
        return []