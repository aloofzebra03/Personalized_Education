from config import NUM_PROFILES, OUTPUT_CSV
from generator import generate_profiles
import pandas as pd
import json

memory_profiles = []

def is_duplicate(profile: dict, memory: list) -> bool:
    return profile in memory

def main():
    all_profiles = []

    while len(all_profiles) < NUM_PROFILES:
        try:
            new_profiles = generate_profiles(memory_profiles)  # returns list of StudentProfile
            for profile in new_profiles:
                profile_dict = profile.dict()
                if not is_duplicate(profile_dict, memory_profiles):
                    memory_profiles.append(profile_dict)
                    all_profiles.append(profile_dict)
                    print(f"Accepted: {profile_dict['name']}")
                else:
                    print(f"Skipped duplicate: {profile_dict['name']}")
            print(f"Total: {len(all_profiles)}/{NUM_PROFILES}")
        except Exception as e:
            print(f"Error: {e}")

    df = pd.DataFrame(all_profiles)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {len(all_profiles)} profiles to {OUTPUT_CSV.resolve()}")

if __name__ == "__main__":
    main()
