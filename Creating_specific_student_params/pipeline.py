import time
import requests
import os
import csv

from Creating_specific_student_params.generator import generate_profile

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

    # 1) Fetch the student JSON with timeout
    timeout_sec = 40  # total time to wait for JSON file
    start_time = time.time()
    json_data = {}
    while True:
        try:
            resp = requests.get(json_url)
            resp.raise_for_status()
            json_data = resp.json()
            break
        except requests.HTTPError:
            elapsed = time.time() - start_time
            if elapsed >= timeout_sec:
                print(f"GitHub file not found after {timeout_sec} seconds. Proceeding without JSON data.")
                break
            print(f"Waiting for JSON file at {json_url} (status {resp.status_code})…")
        except Exception as e:
            elapsed = time.time() - start_time
            if elapsed >= timeout_sec:
                print(f"Error fetching JSON after {timeout_sec} seconds: {e}. Proceeding without JSON data.")
                break
            print(f"Error fetching JSON from {json_url}: {e}")
        time.sleep(poll_interval_sec)

    # 2) Load CSV data and merge with JSON
    csv_path = os.path.join(os.path.dirname(__file__), 'To know your Learning style better (Responses) - Form Responses 1.csv')
    csv_rows = []
    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            csv_rows = list(reader)
    except FileNotFoundError:
        print(f"CSV file not found at {csv_path}, proceeding without CSV data.")

    merged_data = {
        'json': json_data,
        'csv': csv_rows,
    }
    # 3) Generate and return the profile
    profile_model = generate_profile(merged_data, roll_no)
    if not profile_model:
        raise RuntimeError("Profile generation returned no model.")

    return profile_model
