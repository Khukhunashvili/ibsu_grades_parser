import time
import atexit
from firebase import Firebase
from ibsu_grade_parser import IBSU_Parser
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
   return "Hello World"

def update_grades():
    print("-------------------------------")
    firebase = Firebase()
    credentials = firebase.get_students_credentials()

    for credential in credentials.values():
        for username, password in credential.items():
            ibsu = IBSU_Parser(username, password)
            grades = ibsu.grades
            updated_grades = get_updated_grades(firebase.get_grades(username), grades)
            if len(updated_grades) > 0:
                firebase.notify_user(username, updated_grades)
                firebase.insert_grades(username, grades)

def get_updated_grades(old_grades, new_grades):
    updated_grades = []
    grades = {}
    for course_title, course_grades in old_grades.items():
        total_score = 0
        for component in course_grades:
            total_score += float(component["mtCompGrade"])
        grades[course_title] = total_score

    for course_title, course_grades in new_grades.items():
        if course_grades is None:
            continue

        total_score = 0
        for component in course_grades:
            total_score += float(component["mtCompGrade"])

        if course_title not in grades or grades[course_title] != total_score:
            updated_grades.append(course_title)

    return updated_grades

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_grades, trigger="interval", seconds=5)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
   app.run()
