import pickle
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal


class LeadRequest(BaseModel):
    lead_source: Literal["events", "organic_search",
                         "paid_ads", "referral", "social_media"]
    number_of_courses_viewed: int = Field(
        ge=0, description="Number of courses viewed by the lead")
    annual_income: float = Field(
        ge=0, description="Lead's annual income in USD")


class LeadResponse(BaseModel):
    lead_probability: float = Field(
        ge=0, le=1, description="Predicted probability of lead conversion")
    lead: bool = Field(
        description="True if lead is likely to convert, False otherwise")


app = FastAPI(title="lead-prediction")

with open('pipeline_v2.bin', 'rb') as f_in:
    pipeline = pickle.load(f_in)


def predict_single(customer):
    result = pipeline.predict_proba(customer)[0, 1]
    return float(result)


@app.post("/predict", response_model=LeadResponse)
def predict(customer: LeadRequest):
    """Predict lead conversion probability."""
    prob = predict_single(customer.model_dump())

    return LeadResponse(
        lead_probability=prob,
        lead=prob >= 0.5
    )


# Entry point — run the app with Uvicorn when executed directly
if __name__ == "__main__":
    # '0.0.0.0' allows external access (e.g., from Docker)
    # Port 9696 is arbitrary but must match your configuration
    uvicorn.run(app, host="0.0.0.0", port=9696)
