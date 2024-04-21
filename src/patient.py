import uuid
from datetime import datetime
import requests


"""
TODO: Implement the Patient class.
Please import and use the config and db config variables.

The attributes for this class should be the same as the columns in the PATIENTS_TABLE.

The Object Arguments should only be name , gender and age.
Rest of the attributes should be set within the class.

-> for id use uuid4 to generate a unique id for each patient.
-> for checkin and checkout use the current date and time.

There should be a method to update the patient's room and ward. validation should be used.(config is given)

Validation should be done for all of the variables in config and db_config.

There should be a method to commit that patient to the database using the api_controller.
"""


class Patient:

    API_URL = 'http://127.0.0.1:5000/patients'

    def __init__(self, name, gender, age):

        self.patient_id = str(uuid.uuid4())
        self.name = name
        self.age = age
        self.gender = gender
        self.checkin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.checkout = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ward = None
        self.room = None

        self.is_new = True

    def set_room(self, room):

        if not isinstance(room, int):
            raise ValueError("Room must be an integer.")
        self.room = room

    def set_ward(self, ward):

        if not isinstance(ward, int):
            raise ValueError("Ward must be an integer.")
        self.ward = ward

    def to_dict(self):

        return {
            "patient_id": self.patient_id,
            "patient_name": self.name,
            "patient_age": self.age,
            "patient_gender": self.gender,
            "patient_checkin": self.checkin,
            "patient_checkout": self.checkout,
            "patient_ward": self.ward,
            "patient_room": self.room
        }

    def commit(self):
        url = f"{self.API_URL}/{self.patient_id}" if not self.is_new else self.API_URL
        method = requests.put if not self.is_new else requests.post
        payload = self.to_dict()
        print("Final payload being sent:", payload)

        response = method(url, json=payload)

        if response.status_code in [200, 201]:
            self.is_new = False
            return response.json()
        else:
            raise Exception(
                f"Failed to commit patient: {response.content.decode('utf-8')}")

    def __repr__(self):
        return f"<Patient {self.patient_id} | {self.name}>"
