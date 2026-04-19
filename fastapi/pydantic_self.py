from pydantic import BaseModel

class PatientData(BaseModel):
    name: str
    age: int
    
patient_info = {"name": "mehul", "age": 21}

patient1 = PatientData(**patient_info)

print(patient1)



# def insert_patient_data(name: str, age: int):
#     if type(name) == str and type(age) == int:
#         print(name, age)
#         print("inserted into db")
#     else:
#         raise TypeError("Incorrect data types")


# insert_patient_data("name", 21)






