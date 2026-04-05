def insert_patient_data(name: str, age: int):

    if type(name) == str and type(age) == int:
        print(name, age)
        print("inserted into db")
    else:
        raise TypeError("Incorrect data types")
        
        
insert_patient_data("name", "fdsf")