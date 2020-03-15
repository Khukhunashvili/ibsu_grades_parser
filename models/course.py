import re

class Course:
    def __init__(self, html_data):
        self.parse_data(html_data)

    def parse_data(self, data):
        self.title = re.findall(r"<mark[^>]*>([\s\S]*?)</mark>\s*", data)[0]
        self.group = re.findall(r"</strong[^>]*>([\s\S]*?)<br>\s*", data)[0].strip()
        self.lecturer = re.findall(r"</strong[^>]*>([\s\S]*?)<br>\s*", data)[1].strip()
        self.form_data = self.get_form_data(data)

    def get_form_data(self, data):
        courses = re.findall(r"getComponents\(\s*[^)]+?\s*\)", data)
        if len(courses) == 0:
            return []
        return re.findall(r"\'(\s*[^)]+?)\s*'", courses[0])
        # return courses
