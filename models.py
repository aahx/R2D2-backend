from pydantic import BaseModel


class ProspectUpdateModel(BaseModel):
    prospect_info: str

class CompanyUpdateModel(BaseModel):
    company_info: str

class EmailGenerationRequest(BaseModel):
    prospect_info_url: str  # URL to the prospect information file in the cloud storage
    company_info_url: str  # URL to the company information file in the cloud storage