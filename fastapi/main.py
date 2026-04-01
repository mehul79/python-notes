from fastapi import FastAPI, Path, HTTPException 
import uvicorn
import json

app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data
    

@app.get("/")
def home():
    return {"message": "Patient management API"}
    
    
@app.get("/patients")
def view():
    data = load_data()
    return data
    
@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="id of the patient in db", example="P007")):
    #load patients
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="patient not found")
    

@app.delete('/patient/{patient_id}')
async def delete_patient(patient_id: str):
    data = load_data()
    if patient_id in data:
        del data[patient_id]
        return {"deleted patient": f'{data[patient_id]}'}
    raise HTTPException(status_code=404, detail="patient not found")
        

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
