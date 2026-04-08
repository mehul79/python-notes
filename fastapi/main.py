from fastapi import FastAPI, Path, HTTPException, Query 
import uvicorn
import json

app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data
    
    

@app.get("/home")
def home():
    return {"message": "Patient management API"}
    
@app.get("/about")
def about():
    return {"message": "patient management with FastAPI endpoints and pydantic models"}    
    
@app.get("/patients")
def view():
    data = load_data()
    return data
    
@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="id of the patient in db", example="P001")):
    #load patients
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="patient not found")
    
@app.get("/sort")
def sort_patients(sort_by:str = Query(...,description="Sort on basis of height, weight, BMI"), order:str = Query('asc', description="sort in asc or dsc")):
    valid_field = ['height', 'weight', 'bmi']
    if sort_by not in valid_field:
        raise HTTPException(status_code=401, detail=f'invalid field selected from {valid_field}')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=401, detail=f'invalid value {order}')
    
    data = load_data()
    sort_order = True if order=='desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    
    return {"sorted_data": sorted_data}
        
    
        

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
