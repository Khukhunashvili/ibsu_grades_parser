import pyrebase
import json

class Firebase:
    def __init__(self):
        self.firebase = self.init_firebase()
        self.db = self.firebase.database()

    def init_firebase(self):
        firebase_config = json.load(open('google-services.json'))
        config = {
          "apiKey": firebase_config['client'][0]['api_key'][0]['current_key'],
          "authDomain": firebase_config['project_info']['project_id']+".firebaseapp.com",
          "databaseURL": "https://"+firebase_config['project_info']['project_id']+".firebaseio.com",
          "storageBucket": firebase_config['project_info']['project_id']+".appspot.com"
        }
        return pyrebase.initialize_app(config)

    def get_students_credentials(self):
        return self.db.child("auth").get().val()

    def get_grades(self, username):
        return self.db.child("grades").child(username).get().val()

    def insert_grades(self, username, grades):
        self.db.child("grades").child(username).set(grades)

    def notify_user(self, username, updated_grades):
        self.db.child("notify").child(username).set(True)
