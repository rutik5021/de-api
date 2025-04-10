# Total 932 records in the json file

from fastapi import FastAPI, Query
from typing import Optional
from datetime import datetime
import copy
import json


app = FastAPI()

# Sample data
# with open("generated_records.json", "r") as f:
#     original_data = json.load(f)

@app.get("/")
def get_data(
    
):
    return "Hello World!"
