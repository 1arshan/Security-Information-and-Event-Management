import json
import random
import datetime

# Define possible log levels and messages
levels = ["INFO", "WARNING", "ERROR"]
messages = [
    "User login successful for user admin",
    "Multiple failed login attempts detected",
    "Database connection timeout on server X",
    "Scheduled backup completed successfully",
    "Memory usage exceeded threshold on server Y",
    "Unexpected shutdown detected",
    "File system check completed",
    "Service restarted successfully",
    "Configuration file updated",
    "Network latency increased beyond threshold"
]

# Number of log entries to generate
num_entries = 1000

# Start time for logs
start_time = datetime.datetime(2025, 2, 25, 12, 0, 0)

# Open the file for writing
with open("large_sample.log", "w") as f:
    for i in range(num_entries):
        # Increment time by 30 seconds for each entry
        current_time = start_time + datetime.timedelta(seconds=i * 30)
        timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Randomly choose level and message
        level = random.choice(levels)
        message = random.choice(messages)
        
        # Create log entry as a dictionary
        log_entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message
        }
        
        # Write the JSON log entry to file (each entry on a new line)
        f.write(json.dumps(log_entry) + "\n")

print(f"Generated {num_entries} log entries in 'large_sample.log'")
