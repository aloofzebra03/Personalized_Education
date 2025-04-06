from config import NUM_PROFILES, OUTPUT_CSV
from generator import generate_profile
import pandas as pd
import random

def main():
    profiles = []
    for _ in range(NUM_PROFILES):
        profile = generate_profile(random.randint(6, 12))
        profiles.append(profile.dict())
    df = pd.DataFrame(profiles)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f" Saved {len(profiles)} profiles to {OUTPUT_CSV.resolve()}")

if __name__ == "__main__":
    main()
