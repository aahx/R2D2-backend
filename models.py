from pydantic import BaseModel

class UpdateCompanyInfoModel(BaseModel):
    updated_info: str


# from typing import List
# from fastapi import UploadFile, File

# class EmailGenerationRequest(BaseModel):
#     prospect_info: List[UploadFile]
#     company_info: List[UploadFile]