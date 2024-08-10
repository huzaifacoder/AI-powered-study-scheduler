import streamlit as st
import datetime
from collections import defaultdict
import pandas as pd
import os

# IGCSE subjects with codes
igcse_subjects = {
    "Accounting - 0452": "Accounting",
    "Accounting (9-1) - 0985": "Accounting (9-1)",
    "Afrikaans - Second Language - 0548": "Afrikaans - Second Language",
    "Agriculture - 0600": "Agriculture",
    "Arabic - First Language - 0508": "Arabic - First Language",
    "Arabic - First Language (9-1) - 7184": "Arabic - First Language (9-1)",
    "Arabic - Foreign Language - 0544": "Arabic - Foreign Language",
    "Art & Design - 0400": "Art & Design",
    "Art & Design (9-1) - 0989": "Art & Design (9-1)",
    "Bahasa Indonesia - 0538": "Bahasa Indonesia",
    "Biology - 0610": "Biology",
    "Biology (9-1) - 0970": "Biology (9-1)",
    "Business Studies - 0450": "Business Studies",
    "Business Studies (9-1) - 0986": "Business Studies (9-1)",
    "Chemistry - 0620": "Chemistry",
    "Chemistry (9-1) - 0971": "Chemistry (9-1)",
    "Chinese - First Language - 0509": "Chinese - First Language",
    "Chinese - Second Language - 0523": "Chinese - Second Language",
    "Chinese (Mandarin) - Foreign Language - 0547": "Chinese (Mandarin) - Foreign Language",
    "Computer Science - 0478": "Computer Science",
    "Computer Science (9-1) - 0984": "Computer Science (9-1)",
    "Design & Technology - 0445": "Design & Technology",
    "Design & Technology (9-1) - 0979": "Design & Technology (9-1)",
    "Drama - 0411": "Drama",
    "Drama (9-1) - 0994": "Drama (9-1)",
    "Economics - 0455": "Economics",
    "Economics (9-1) - 0987": "Economics (9-1)",
    "English - First Language - 0500": "English - First Language",
    "English - First Language (9-1) - 0990": "English - First Language (9-1)",
    "English - First Language (US) - 0524": "English - First Language (US)",
    "English – Literature (US) – 0427": "English – Literature (US)",
    "English – Literature in English – 0475": "English – Literature in English",
    "English – Literature in English (9-1) – 0992": "English – Literature in English (9-1)",
    "English (as an Additional Language) - 0472": "English (as an Additional Language)",
    "English (as an Additional Language) (9-1) - 0772": "English (as an Additional Language) (9-1)",
    "English (Core) as a Second Language (Egypt) - 0465": "English (Core) as a Second Language (Egypt)",
    "English as a Second Language (Count-in speaking) - 0511": "English as a Second Language (Count-in speaking)",
    "English as a Second Language (Count-in Speaking) (9-1) - 0991": "English as a Second Language (Count-in Speaking) (9-1)",
    "English as a Second Language (Speaking endorsement) - 0510": "English as a Second Language (Speaking endorsement)",
    "English as a Second Language (Speaking Endorsement) (9-1) - 0993": "English as a Second Language (Speaking Endorsement) (9-1)",
    "Enterprise - 0454": "Enterprise",
    "Environmental Management - 0680": "Environmental Management",
    "Food & Nutrition - 0648": "Food & Nutrition",
    "French - First Language - 0501": "French - First Language",
    "French - Foreign Language - 0520": "French - Foreign Language",
    "French (9-1) - 7156": "French (9-1)",
    "Geography - 0460": "Geography",
    "Geography (9-1) - 0976": "Geography (9-1)",
    "German - First Language - 0505": "German - First Language",
    "German - Foreign Language - 0525": "German - Foreign Language",
    "German (9-1) - 7159": "German (9-1)",
    "Global Perspectives - 0457": "Global Perspectives",
    "Hindi as a Second Language - 0549": "Hindi as a Second Language",
    "History - 0470": "History",
    "History - American (US) - 0409": "History - American (US)",
    "History (9-1) - 0977": "History (9-1)",
    "Information and Communication Technology - 0417": "Information and Communication Technology",
    "Information and Communication Technology (9-1) - 0983": "Information and Communication Technology (9-1)",
    "IsiZulu as a Second Language - 0531": "IsiZulu as a Second Language",
    "Islamiyat - 0493": "Islamiyat",
    "Italian - Foreign Language - 0535": "Italian - Foreign Language",
    "Italian (9-1) - 7164": "Italian (9-1)",
    "Latin - 0480": "Latin",
    "Malay - First Language - 0696": "Malay - First Language",
    "Malay - Foreign Language - 0546": "Malay - Foreign Language",
    "Marine Science - 0697": "Marine Science",
    "Mathematics - 0580": "Mathematics",
    "Mathematics - Additional - 0606": "Mathematics - Additional",
    "Mathematics - International - 0607": "Mathematics - International",
    "Mathematics (9-1) - 0980": "Mathematics (9-1)",
    "Mathematics (US) - 0444": "Mathematics (US)",
    "Music - 0410": "Music",
    "Music (9-1) - 0978": "Music (9-1)",
    "Pakistan Studies - 0448": "Pakistan Studies",
    "Physical Education - 0413": "Physical Education",
    "Physical Education (9-1) - 0995": "Physical Education (9-1)",
    "Physical Science - 0652": "Physical Science",
    "Physics - 0625": "Physics",
    "Physics (9-1) - 0972": "Physics (9-1)",
    "Portuguese - First Language - 0504": "Portuguese - First Language",
    "Religious Studies - 0490": "Religious Studies",
    "Sanskrit - 0499": "Sanskrit",
    "Science - Combined - 0653": "Science - Combined",
    "Sciences - Co-ordinated (9-1) - 0973": "Sciences - Co-ordinated (9-1)",
    "Sciences - Co-ordinated (Double) - 0654": "Sciences - Co-ordinated (Double)",
    "Setswana - First Language - 0698": "Setswana - First Language",
    "Sociology - 0495": "Sociology",
    "Spanish - First Language - 0502": "Spanish - First Language",
    "Spanish - Foreign Language - 0530": "Spanish - Foreign Language",
    "Spanish - Literature - 0488": "Spanish - Literature",
    "Spanish - Literature in Spanish - 0474": "Spanish - Literature in Spanish",
    "Spanish (9-1) - 7160": "Spanish (9-1)",
    "Swahili - 0262": "Swahili",
    "Thai - First Language - 0518": "Thai - First Language",
    "Travel & Tourism - 0471": "Travel & Tourism",
    "Turkish - First Language - 0513": "Turkish - First Language",
    "Urdu as a Second Language - 0539": "Urdu as a Second Language",
    "Vietnamese - First Language - 0695": "Vietnamese - First Language",
    "World Literature - 0408": "World Literature"
}

# Function to prioritize tasks with only high and low priorities
def prioritize_tasks(subjects, deadlines, difficulties, priorities):
    priority = {}
    for subject in subjects:
        if subject in deadlines and subject in difficulties and subject in priorities:
            days_until_deadline = (deadlines[subject] - datetime.datetime.now().date()).days
            priority_level = 1 if priorities[subject] else 2
            priority[subject] = (priority_level, difficulties[subject] / days_until_deadline)
        else:
            st.warning(f"Missing data for {subject}. Please ensure deadlines, difficulties, and priorities are provided.")
    return sorted(priority.items(), key=lambda item: item[1])

# Function to create the initial schedule with balanced distribution and breaks
def create_schedule(prioritized_subjects, deadlines, hours_per_day):
    schedule = defaultdict(list)
    current_date = datetime.datetime.now().date()
    total_days = max((deadlines[subject] - current_date).days for subject, _ in prioritized_subjects)

    # Initialize available hours for each day
    available_hours = {current_date + datetime.timedelta(days=i): hours_per_day for i in range(total_days)}

    for subject, priority in prioritized_subjects:
        days_until_deadline = (deadlines[subject] - current_date).days
        priority_level = priority[0]
        daily_hours = min(hours_per_day / len(prioritized_subjects), hours_per_day)

        for day in range(days_until_deadline):
            study_date = current_date + datetime.timedelta(days=day)
            if priority_level == 1:  # High priority
                if available_hours[study_date] >= daily_hours:
                    schedule[study_date].insert(0, (subject, daily_hours))
                    available_hours[study_date] -= daily_hours
            else:  # Low priority
                if available_hours[study_date] >= daily_hours:
                    schedule[study_date].append((subject, daily_hours))
                    available_hours[study_date] -= daily_hours

    return schedule


# Function to create a timetable
def create_timetable(schedule, start_time, break_duration):
    timetable = defaultdict(list)
    for date, tasks in sorted(schedule.items()):
        current_time = datetime.datetime.combine(date, start_time)
        for i, (subject, hours) in enumerate(tasks):
            end_time = current_time + datetime.timedelta(minutes=hours_to_minutes(hours))
            timetable[date].append((subject, current_time.strftime('%I:%M %p') + ' - ' + end_time.strftime('%I:%M %p')))
            current_time = end_time
            if i < len(tasks) - 1:  # Add break after each subject except the last one
                break_end_time = current_time + datetime.timedelta(minutes=break_duration)
                timetable[date].append(('Break', current_time.strftime('%I:%M %p') + ' - ' + break_end_time.strftime('%I:%M %p')))
                current_time = break_end_time
    return timetable


def hours_to_minutes(hours):
    return int(hours * 60)

def display_regular_timetable(timetable, title):
    st.write(f"### {title}")
    for date, tasks in timetable.items():
        date_str = date.strftime('%A - %m/%d/%Y')
        st.markdown(f"**{date_str}**")
        data = []
        for subject, time_range in tasks:
            data.append([subject, time_range])
        df = pd.DataFrame(data, columns=["Subject", "Time Range"])
        st.table(df)

def save_timetable(timetable, filename):
    df = pd.DataFrame([(date, subject, time_range) for date, tasks in timetable.items() for subject, time_range in tasks], columns=['Date', 'Subject', 'Time Range'])
    df.to_csv(filename, index=False)

def load_timetable(filename):
    df = pd.read_csv(filename)
    timetable = defaultdict(list)
    for _, row in df.iterrows():
        date = datetime.datetime.strptime(row['Date'], '%Y-%m-%d').date()
        subject = row['Subject']
        time_range = row['Time Range']
        timetable[date].append((subject, time_range))
    return timetable

# Function to collect and store student logs
# Function to collect and store student logs as a daily checklist
def collect_student_logs(subjects):
    logs = {}
    for subject in subjects:
        st.markdown(f"#### Log for {subject}")
        completed_tasks = st.text_area(f"List the tasks you completed for {subject} today (comma separated)", "")
        incomplete_tasks = st.text_area(f"List the tasks you couldn't complete for {subject} today (comma separated)", "")
        logs[subject] = {
            "completed_tasks": completed_tasks.split(', ') if completed_tasks else [],
            "incomplete_tasks": incomplete_tasks.split(', ') if incomplete_tasks else []
        }
    return logs


# Function to analyze logs and update timetable
def analyze_logs_and_update_timetable(timetable, logs):
    updated_timetable = timetable.copy()
    for date, tasks in timetable.items():
        for i, (subject, time_range) in enumerate(tasks):
            if subject in logs and not logs[subject]['completed']:
                # If the subject was not completed, allocate more time in the next available slot
                additional_time = 30  # Add 30 minutes as an example
                end_time_str = time_range.split(' - ')[1]
                end_time = datetime.datetime.strptime(end_time_str, '%I:%M %p')
                new_end_time = end_time + datetime.timedelta(minutes=additional_time)
                updated_timetable[date][i] = (subject, time_range.split(' - ')[0] + ' - ' + new_end_time.strftime('%I:%M %p'))
    return updated_timetable

# Main Streamlit application
st.set_page_config(page_title="AI-Powered Study Schedule Maker", layout="wide", initial_sidebar_state="expanded")

st.title('📚 AI-Powered Study Schedule Maker')

# Initialize session state
if 'subjects' not in st.session_state:
    st.session_state.subjects = []
if 'hours_per_day' not in st.session_state:
    st.session_state.hours_per_day = 3
if 'deadlines' not in st.session_state:
    st.session_state.deadlines = {}
if 'difficulties' not in st.session_state:
    st.session_state.difficulties = {}
if 'priorities' not in st.session_state:
    st.session_state.priorities = {}
if 'strengths' not in st.session_state:
    st.session_state.strengths = {}
if 'prioritized_subjects' not in st.session_state:
    st.session_state.prioritized_subjects = []
if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.time(8, 0)
if 'break_duration' not in st.session_state:
    st.session_state.break_duration = 10
if 'timetable_visible' not in st.session_state:
    st.session_state.timetable_visible = False

# Collecting user input
st.header('Enter Your Study Information')

syllabus = st.selectbox('Select Syllabus', ['IGCSE'])
if syllabus == 'IGCSE':
    subjects_selected = st.multiselect('📘 Select IGCSE Subjects', list(igcse_subjects.keys()), ['Mathematics - 0580', 'English - First Language - 0500'])
    st.session_state.subjects = [igcse_subjects[subject] for subject in subjects_selected]

# Check if any subjects are selected
if not st.session_state.subjects:
    st.error("Please select at least one subject.")
else:
    st.session_state.hours_per_day = st.number_input('⏰ Available Hours Per Day', min_value=1, max_value=24, value=st.session_state.hours_per_day)

    difficulty_options = [1, 2, 3, 4, 5]
    priority_options = [1, 0]
    strength_options = [1, 2, 3]

    subject_columns = st.columns(len(st.session_state.subjects))

    for i, subject in enumerate(st.session_state.subjects):
        with subject_columns[i]:
            st.markdown(f"### {subject}")
            st.session_state.deadlines[subject] = st.date_input(f'🗓️ Deadline for {subject}', min_value=datetime.date.today(), value=st.session_state.deadlines.get(subject, None))
            st.session_state.difficulties[subject] = st.selectbox(f'📈 Difficulty for {subject}', difficulty_options, index=difficulty_options.index(st.session_state.difficulties.get(subject, 3)))
            st.session_state.priorities[subject] = st.selectbox(f'⭐ Priority for {subject}', priority_options, index=priority_options.index(st.session_state.priorities.get(subject, 1)))
            st.session_state.strengths[subject] = st.selectbox(f'💪 Strength for {subject}', strength_options, index=strength_options.index(st.session_state.strengths.get(subject, 1)))

    st.session_state.start_time = st.time_input('⏰ Preferred Start Time', value=st.session_state.start_time)
    st.session_state.break_duration = st.number_input('⏰ Break Duration (in minutes)', min_value=1, max_value=60, value=st.session_state.break_duration)

    if st.button('Submit'):
        # Process user input
        try:
            deadlines = {subject: st.session_state.deadlines[subject] for subject in st.session_state.subjects}
            difficulties = {subject: st.session_state.difficulties[subject] for subject in st.session_state.subjects}
            priorities = {subject: st.session_state.priorities[subject] for subject in st.session_state.subjects}
            strengths = {subject: st.session_state.strengths[subject] for subject in st.session_state.subjects}

            # Ensure no subject has a None deadline to avoid division by zero
            for subject in st.session_state.subjects:
                if deadlines[subject] is None:
                    st.error(f"Please provide a deadline for {subject}.")
                    st.stop()

            #st.write('### Study Information')
            #st.write('**Subjects:**', ', '.join(st.session_state.subjects))
            #st.write('**Available Hours Per Day:**', st.session_state.hours_per_day)
            #st.write('**Deadlines:**', deadlines)
            #st.write('**Difficulties:**', difficulties)
            #st.write('**Priorities:**', priorities)
            #st.write('**Strengths:**', strengths)
            #st.write('**Preferred Start Time:**', st.session_state.start_time.strftime('%I:%M %p'))
            #st.write('**Break Duration:**', f"{st.session_state.break_duration} minutes")

            # Prioritize tasks
            st.session_state.prioritized_subjects = prioritize_tasks(st.session_state.subjects, deadlines, difficulties,
                                                                     priorities)
            #st.write('### Prioritized Subjects')
            for subject, priority in st.session_state.prioritized_subjects:
                #st.write(f"**{subject}:** Priority Level {priority[0]} with difficulty ratio {priority[1]:.2f}")
                pass

            # Generate and display the schedule using Priority-Based Scheduling
            schedule_priority_based = create_schedule(st.session_state.prioritized_subjects, deadlines,
                                                      st.session_state.hours_per_day)
            timetable_priority_based = create_timetable(schedule_priority_based, st.session_state.start_time,
                                                        st.session_state.break_duration)
            st.session_state.timetable = timetable_priority_based

            # Display the generated timetable
            display_regular_timetable(timetable_priority_based, "Priority-Based Scheduling Timetable")

            # Save the timetable to a CSV file
            save_timetable(timetable_priority_based, 'timetable.csv')
            st.success("Timetable generated and saved successfully!")

            # Button to show saved timetable
            #if st.button('Show Saved Timetable'):
                #st.session_state.timetable_visible = True

            #if st.session_state.timetable_visible:
                #if os.path.exists('saved_timetable.csv'):
                    #saved_timetable = load_timetable('saved_timetable.csv')
                    #display_regular_timetable(saved_timetable, "Saved Timetable")

        except Exception as e:
            st.error(f"Error parsing input: {e}")
