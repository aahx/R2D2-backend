from pydantic import BaseModel

class GenerateEmailModel(BaseModel):
    prospect_info: str
    prospect_name: str
    company_info: str
    company_name: str
    sales_rep: str