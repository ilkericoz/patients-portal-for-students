import uuid
from datetime import datetime
import requests
from config import *


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
    # API URL for accessing the patient data.
    API_URL = 'http://127.0.0.1:5000/patients'

    def __init__(self, name, gender, age):
        # Initialize a new patient with basic details and generate unique identifiers and timestamps.
        self.patient_id = str(uuid.uuid4())
        self.name = name
        self.age = self.validate_age(age)
        self.gender = self.validate_gender(gender)
        self.checkin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.checkout = None
        self.ward = None
        self.room = None
        # This flag helps to determine if the patient is being registered for the first time.
        self.is_new = True

    def validate_gender(self, gender):
        if gender not in GENDERS:
            raise ValueError(
                f"Invalid gender: {gender}. Valid options are: {', '.join(GENDERS)}")
        return gender

    def validate_age(self, age):
        if not isinstance(age, int) or age <= 0:
            raise ValueError(
                f"Invalid age: {age}. Age must be a positive integer.")
        else:
            return age

    def set_room(self, room):
        # Set the room number for the patient with proper validation.
        if not isinstance(room, int):  # Assuming room has been formatted like "Ward1"
            raise ValueError("Room should be int.")

        if not any(str(room) in rooms for rooms in ROOM_NUMBERS.values()):
            raise ValueError(
                f"Room {room} does not exist in ward {self.ward}.")

        self.room = room

    def set_ward(self, ward):
        # Set the ward number for the patient with proper validation.
        if not isinstance(ward, int) or ward not in WARD_NUMBERS:
            raise ValueError("Ward doesn't exist. Please select a valid ward.")
        self.ward = ward

    def get_id(self):
        return self.patient_id

    def get_name(self):
        return self.name

    def get_ward(self):
        return self.ward

    def get_room(self):
        return self.room

    def to_dict(self):
        # Convert the patient information into a dictionary aligning with the database schema.
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
        url = f"http://127.0.0.1:5000/patient/{self.patient_id}" if not self.is_new else self.API_URL
        method = requests.put if not self.is_new else requests.post
        payload = self.to_dict()
        print("Final payload being sent:", payload)  # Debugging statement

        response = method(url, json=payload)

        if response.status_code in [200, 201]:
            self.is_new = False
            return response.json()
        else:
            raise Exception(
                f"Failed to commit patient: {response.content.decode('utf-8')} {response.status_code}")

    def __repr__(self):
        return f"<Patient {self.patient_id} | {self.name}>"
