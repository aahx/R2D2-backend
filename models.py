from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from typing import List

class UpdateCompanyInfoModel(BaseModel):
    updated_info: str

# from typing import List
# from fastapi import UploadFile, File

# class EmailGenerationRequest(BaseModel):
#     prospect_info: List[UploadFile]
#     company_info: List[UploadFile]