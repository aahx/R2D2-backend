from pydantic import BaseModel

class UpdateCompanyInfoModel(BaseModel):
    updated_info: str

class EmailGenerationRequest(BaseModel):
    prospect_info_url: str  # URL to the prospect information file in the cloud storage
    company_info_url: str  # URL to the company information file in the cloud storage