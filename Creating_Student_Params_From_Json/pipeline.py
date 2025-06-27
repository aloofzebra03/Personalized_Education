import time
import requests

from Creating_Student_Params_From_Json.generator import generate_profile

def run_profile_generation_pipeline(
    roll_no: str,
    poll_interval_sec: int = 5,
    base_url_template: str = (
        "https://raw.githubusercontent.com/"
        "markkevins109/student_grades/refs/heads/main/results/rollno{roll_no}.json"
    )
):
    # Build the URL for the given roll number
    json_url = base_url_template.format(roll_no=roll_no)

    # 1) Fetch the student JSON
    while True:
        try:
            resp = requests.get(json_url)
            resp.raise_for_status()
            data = resp.json()
            break
        except requests.HTTPError:
            print(f"Waiting for JSON file at {json_url1} (status {resp.status_code})…")
        except Exception as e:
            print(f"Error fetching JSON from {json_url}: {e}")
        time.sleep(poll_interval_sec)

    # 2) Generate and return the profile
    profile_model = generate_profile(data,roll_no)
    if not profile_model:
        raise RuntimeError("Profile generation returned no model.")

    return profile_model
