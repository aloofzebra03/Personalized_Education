from config import OUTPUT_CSV
from generator import generate_profiles
import pandas as pd
import json
from collections import deque

NUM_PROFILES = 2000
MEMORY_LIMIT = 1000  # Define the memory limit

# Use a deque for efficient appending and popping from the left (oldest)
memory_profiles = deque(maxlen=MEMORY_LIMIT) 

def is_duplicate(profile: dict, memory: deque) -> bool:
    return profile in memory

def main():
    all_profiles = []

    # 1. Load existing profiles from CSV and populate memory_profiles
    try:
        if OUTPUT_CSV.exists():
            existing_df = pd.read_csv(OUTPUT_CSV)
            # Convert DataFrame rows to dictionaries and add to memory_profiles
            # Ensure only the latest MEMORY_LIMIT profiles are loaded into memory
            for _, row in existing_df.tail(MEMORY_LIMIT).iterrows():
                all_profiles.append(row.to_dict())
            print(f"Loaded {len(all_profiles)} profiles from {OUTPUT_CSV.resolve()} into memory.")
    except Exception as e:
        print(f"Error loading existing profiles from CSV: {e}")

    # Initialize all_profiles with existing data to avoid re-generating them if NUM_PROFILES is larger
    # This also helps if we want to continue adding to an existing dataset.
    memory_profiles.extend(list(all_profiles)) 
    print(f"Initial profiles in all_profiles (from memory): {len(all_profiles)}")


    while len(all_profiles) < NUM_PROFILES:
        try:
            # generate_profiles should ideally take a list/deque of dicts
            new_profiles = generate_profiles(list(memory_profiles))  # Pass as list if generate_profiles expects it
            
            for profile in new_profiles:
                profile_dict = profile.model_dump()

                memory_profiles.append(profile_dict)  # deque automatically handles the maxlen

                # Check for duplicates against the current memory_profiles
                if not is_duplicate(profile_dict, memory_profiles):
                    all_profiles.append(profile_dict)
                    print(f"Accepted {profile_dict['next_section']}")
                else:
                    print(f"Skipped duplicate")
            
            print(f"Total: {len(all_profiles)}/{NUM_PROFILES}")

        except Exception as e:
            print(f"Error during profile generation: {e}")

    df = pd.DataFrame(all_profiles)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {len(all_profiles)} profiles to {OUTPUT_CSV.resolve()}")

if __name__ == "__main__":
    main()