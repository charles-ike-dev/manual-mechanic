import os
import re
import shutil

# Configuration
source_dir = "../docs/v20/unprocessed"
old_versions_dir = os.path.join(source_dir, "old_version")

# Ensure the old_versions directory exists
if not os.path.exists(old_versions_dir):
    os.makedirs(old_versions_dir)

# Regex pattern to match filenames of the form: NAME_VERSION.xml
# Example: IU_5000010586_5.xml
# Group 1: Base name
# Group 2: Version number
pattern = re.compile(r"^(.*)_(\d+)\.xml$")

# Dictionary to store files by base name
# Structure: { base_name: [(version_num, full_file_path), ...] }
files_by_base = {}

for entry in os.scandir(source_dir):
    if entry.is_file():
        match = pattern.match(entry.name)
        if match:
            base_name = match.group(1)
            version_str = match.group(2)
            # Convert version to integer for proper comparison
            version_num = int(version_str)
            files_by_base.setdefault(base_name, []).append(
                (version_num, entry.path))

# For each base name, if there are multiple versions, move the older versions
for base_name, versions in files_by_base.items():
    if len(versions) > 1:
        # Sort by version number
        versions.sort(key=lambda x: x[0])

        # The last element in the sorted list is the highest version
        highest_version = versions[-1][0]

        # Move all older versions (everything except the highest one)
        for version_num, file_path in versions:
            if version_num < highest_version:
                # Move to old_versions_dir
                dest_path = os.path.join(
                    old_versions_dir, os.path.basename(file_path))
                shutil.move(file_path, dest_path)
                print(f"Moved older version {os.path.basename(
                    file_path)} to {old_versions_dir}")
