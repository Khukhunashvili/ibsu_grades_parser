from models.course import Course
import requests
import re

BASE_URL = "https://sis.ibsu.edu.ge"
LOGIN_ERROR = "Username/password was incorrect."

class IBSU_Parser:
    def __init__(self, username, password):
        self.get_data(username, password)


    def get_data(self, username, password):
        payload = {
            "username": username,
            "password": password,
            "action": "login"
        }

        with requests.Session() as session:
            dashboard = session.post(BASE_URL + "/", data=payload)

            if LOGIN_ERROR in dashboard.text:
                self.authenticated = False
                return

            self.authenticated = True
            self.courses = self.get_courses(dashboard.text)
            self.grades = {}

            for index, course in enumerate(self.courses):
                self.grades[course] = self.get_grades(session, course)

    def get_courses(self, html):
        tbody = re.findall(r"<tbody[^>]*>[\s\S]*?</tbody>\s*", html)[0]
        courses = re.findall(r"<tr[^>]*>[\s\S]*?</tr>\s*", tbody)

        for i, course_data in enumerate(courses):
            course = Course(course_data)
            courses[i] = course

        return courses

    def get_grades(self, session, course):
        if len(course.form_data) == 0:
            return None

        payload = {
            "courseId": course.form_data[0],
            "formId": course.form_data[1]
        }
        grades = session.post(BASE_URL + "/student/", data=payload)
        return grades.json()
