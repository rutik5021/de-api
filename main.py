# Total 932 records in the json file

from fastapi import FastAPI, Query
from typing import Optional
from datetime import datetime
import copy
import json


app = FastAPI()

# Sample data
with open("generated_records.json", "r") as f:
    original_data = json.load(f)

@app.get("/data")
def get_data(
    start_time: Optional[datetime] = Query(None, description="Records with timestamp > this"),
    end_time: Optional[datetime] = Query(None, description="Records with timestamp <= this"),
    sort_by: Optional[str] = Query("timestamp", description="Field to sort by"),
    sort_order: Optional[str] = Query("asc", description="asc or desc")
):
    # Make a deep copy to avoid mutating original data
    filtered_data = copy.deepcopy(original_data)

    # Parse timestamps
    for item in filtered_data:
        item["timestamp"] = datetime.fromisoformat(item["timestamp"])

    # Apply filters
    if start_time:
        filtered_data = [item for item in filtered_data if item["timestamp"] >= start_time]
    if end_time:
        filtered_data = [item for item in filtered_data if item["timestamp"] <= end_time]

    # Sorting logic
    reverse = sort_order.lower() == "desc"
    try:
        filtered_data.sort(key=lambda x: x[sort_by], reverse=reverse)
    except KeyError:
        return {"error": f"Cannot sort by '{sort_by}'. Field does not exist."}
    
    filtered_data = filtered_data[:100]

    # Convert timestamp back to string
    for item in filtered_data:
        item["timestamp"] = item["timestamp"].isoformat()

    return {"results": filtered_data}
