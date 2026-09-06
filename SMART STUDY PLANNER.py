"""
SMART STUDY PLANNER

programme that helps a student log, review and analyse
study sessions across different subjects over a semester.
 
All session data is saved to 'study_log.txt' so the planner keeps working
correctly across multiple runs.

"""
import os
DATA_FILE = "study_log.txt"
DELIMITER = "|"  # used to separate fields when saving/loading sessions


# Classification helper

def classify_session(duration):

    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"

# Adding sessions
def add_session(sessions):
   
    print("\n--- Add a Study Session ---")
    subject = input("Subject name: ").strip()
    topic = input("Topic covered: ").strip()
    date = input("Date / day label (e.g. 2026-09-05 or 'Monday'): ").strip()

    # Validate duration: must be a positive number, keep asking until valid
    duration = None
    while duration is None:
        raw_duration = input("Duration studied (minutes): ").strip()
        try:
            value = float(raw_duration)
            if value <= 0:
                print("Duration must be a positive number. Please try again.")
            else:
                duration = value
        except ValueError:
            print("That doesn't look like a number. Please try again.")

    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration,
    }
    sessions.append(session)
    print(f"Session added: {subject} ({classify_session(duration)}, {duration:.0f} min)")

# Viewing sessions
def view_sessions(sessions):
    print("\n--- All Study Sessions ---")
    if not sessions:
        print("No sessions have been logged yet.")
        return

    _print_table(sessions)


def _print_table(sessions):
    header = f"{'Subject':<15}{'Topic':<20}{'Date':<15}{'Duration (min)':<16}{'Type':<8}"
    print(header)
    print("-" * len(header))
    for s in sessions:
        classification = classify_session(s["duration"])
        print(
            f"{s['subject']:<15}{s['topic']:<20}{s['date']:<15}"
            f"{s['duration']:<16.0f}{classification:<8}"
        )
# Searching by subject
def search_by_subject(sessions):
    print("\n--- Search Sessions by Subject ---")
    subject_query = input("Enter subject to search for: ").strip().lower()

    matches = [s for s in sessions if s["subject"].lower() == subject_query]

    if not matches:
        print(f"No sessions found for subject '{subject_query}'.")
        return


    _print_table(matches)
    total_minutes = sum(s["duration"] for s in matches)
    print(f"\nTotal time spent on this subject: {total_minutes:.0f} minutes "
          f"({total_minutes / 60:.2f} hours)")

# Statistics
def study_statistics(sessions):
    print("\n--- Study Statistics ---")
    if not sessions:
        print("No sessions have been logged yet.")
        return

    # Total hours studied overall
    total_minutes = sum(s["duration"] for s in sessions)
    print(f"Total time studied overall: {total_minutes:.0f} minutes "
          f"({total_minutes / 60:.2f} hours)")

    # Total hours studied per subject (build a subject -> total minutes map)
    subject_totals = {}
    for s in sessions:
        subject_totals[s["subject"]] = subject_totals.get(s["subject"], 0) + s["duration"]

    print("\nTime studied per subject:")
    for subject, minutes in subject_totals.items():
        print(f"  {subject:<15}: {minutes:.0f} min ({minutes / 60:.2f} hrs)")

    # Weakest subject = least total study time
    weakest_subject = "min(subject_totals, key=subject_totals.get)"
    print(f"\nWeakest area (least total study time): {weakest_subject} "
          f"({subject_totals[weakest_subject]:.0f} min)")

    # Longest single session
    longest = max(sessions, key=lambda s: s["duration"])
    print(f"\nLongest single session: {longest['subject']} - {longest['topic']} "
          f"on {longest['date']} ({longest['duration']:.0f} min, "
          f"{classify_session(longest['duration'])})")

# Saving and loading
def save_sessions(sessions):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for s in sessions:
            # Join fields with a delimiter unlikely to appear in normal text
            line = DELIMITER.join([
                s["subject"],
                s["topic"],
                s["date"],
                str(s["duration"]),
            ])
            f.write(line + "\n")
    print(f"Sessions saved to '{DATA_FILE}'.")


def load_sessions():
    sessions = []

    if not os.path.exists(DATA_FILE):
        # No saved data yet - that's fine, just start with an empty list
        return sessions

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue  # skip blank lines
                parts = line.split(DELIMITER)
                if len(parts) != 4:
                    continue  # skip malformed lines rather than crashing
                subject, topic, date, duration_str = parts
                try:
                    duration = float(duration_str)
                except ValueError:
                    continue  # skip lines with a corrupted duration value
                sessions.append({
                    "subject": subject,
                    "topic": topic,
                    "date": date,
                    "duration": duration,
                })
    except OSError:
        # File exists but couldn't be read for some reason - fail gracefully
        print(f"Warning: could not read '{DATA_FILE}'. Starting with no sessions.")
        return []

    return sessions

# Menu-driven interface
def display_menu():
    print("\n===== Smart Study Planner =====")
    print("1. Add a study session")
    print("2. View all sessions")
    print("3. Search sessions by subject")
    print("4. View statistics")
    print("5. Save and exit")


def main():
    sessions = load_sessions()
    print("Welcome to the Smart Study Planner!")
    if sessions:
        print(f"Loaded {len(sessions)} session(s) from a previous run.")

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_session(sessions)
        elif choice == "2":
            view_sessions(sessions)
        elif choice == "3":
            search_by_subject(sessions)
        elif choice == "4":
            study_statistics(sessions)
        elif choice == "5":
            save_sessions(sessions)
            print("Goodbye - happy studying!")
            break
        else:
            # Reject invalid choices without crashing
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()