import time
import requests
import pandas as pd
from config import OUTPUT_CSV
from generator import generate_profile

GITHUB_JSON_URL = "https://raw.githubusercontent.com/your-org/your-repo/main/student.json"
POLL_INTERVAL_SEC = 5

def download_student_json(url: str) -> dict:
    while True:
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                return resp.json()
            else:
                print(f"Waiting for JSON file (status {resp.status_code})…")
        except Exception as e:
            print(f"Error fetching JSON: {e}")
        time.sleep(POLL_INTERVAL_SEC)

def main():
    # 1) fetch the student JSON
    student_details = download_student_json(GITHUB_JSON_URL)

    # 2) generate one profile
    try:
        profile_model = generate_profile(student_details)
        if profile_model:
            profile_dict = profile_model.model_dump()
            df = pd.DataFrame([profile_dict])
            df.to_csv(OUTPUT_CSV, index=False)
            print(f"Saved 1 profile to {OUTPUT_CSV.resolve()}")
        else:
            print("No profile generated.")
    except Exception as e:
        print(f"Error in generation pipeline: {e}")

if __name__ == "__main__":
    main()
