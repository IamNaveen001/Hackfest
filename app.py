from flask import Flask, render_template, request, jsonify
import itertools
import random

app = Flask(__name__)

def generate_timetable(subjects, time_slots, days, labs):
    timetable = {
        day: {slot: {lab: None for lab in labs} for slot in time_slots}
        for day in days
    }

    time_slot_pairs = [(time_slots[i], time_slots[i + 1]) for i in range(0, len(time_slots), 2)]
    allocation = itertools.cycle(itertools.product(days, time_slot_pairs))

    for subject_code in subjects:
        for section in ["A", "B"]:
            allocated = False
            while not allocated:
                day, (slot1, slot2) = next(allocation)
                available_labs = [
                    lab for lab, assigned_subject in timetable[day][slot1].items()
                    if assigned_subject is None
                ]

                if len(available_labs) >= 2:
                    selected_labs = random.sample(available_labs, 2)
                    timetable[day][slot1][selected_labs[0]] = f"{subject_code} (Slot {section}1)"
                    timetable[day][slot2][selected_labs[0]] = f"{subject_code} (Slot {section}1)"
                    timetable[day][slot1][selected_labs[1]] = f"{subject_code} (Slot {section}2)"
                    timetable[day][slot2][selected_labs[1]] = f"{subject_code} (Slot {section}2)"
                    allocated = True

    return timetable

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    subjects = data.get("subjects", [])
    labs = data.get("labs", [])
    days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]
    time_slots = [
        "09:00 - 09:50",
        "09:50 - 10:40",
        "11:00 - 11:50",
        "11:50 - 12:40",
        "01:40 - 02:30",
        "02:30 - 03:20",
    ]

    timetable = generate_timetable(subjects, time_slots, days, labs)
    return jsonify(timetable)

if __name__ == "__main__":
    app.run(debug=True)
