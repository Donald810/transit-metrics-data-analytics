
import csv
from collections import defaultdict

# Load synthetic transit data
with open("synthetic_trips.csv", newline="") as file:
    rows = list(csv.DictReader(file))

# Step 1: Validate required columns
required_columns = {
    "trip_id",
    "route",
    "scheduled_minute",
    "actual_minute",
    "on_time"
}

assert rows, "Dataset is empty"
assert required_columns.issubset(rows[0]), "Missing columns"

# Step 2: Check for duplicate trip IDs
trip_ids = [row["trip_id"] for row in rows]

assert len(trip_ids) == len(set(trip_ids)), \
    "Duplicate trip IDs detected"

# Step 3: Validate transit performance data
results = defaultdict(list)

for row in rows:
    scheduled = int(row["scheduled_minute"])
    actual = int(row["actual_minute"])

    delay = actual - scheduled

    # A trip is on time if delay is 0-5 minutes
    expected_status = int(0 <= delay <= 5)

    assert int(row["on_time"]) == expected_status, \
        f"QA failure for trip {row['trip_id']}"

    results[row["route"]].append(expected_status)

# Step 4: Calculate route-level performance
all_values = []

for route, values in sorted(results.items()):
    on_time_rate = sum(values) / len(values) * 100

    print(f"Route {route}: {on_time_rate:.2f}% on time")

    all_values.extend(values)

# Step 5: Calculate overall performance
overall_rate = sum(all_values) / len(all_values) * 100

assert abs(overall_rate - 60) < 0.01, \
    "Overall performance does not match expected result"

print(f"Overall: {overall_rate:.2f}%")
print("All QA tests passed")
