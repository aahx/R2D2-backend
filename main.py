import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from models import ProspectUpdateModel, CompanyUpdateModel, EmailGenerationRequest
from langchain.document_loaders import TextLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
import boto3

# Creating a FastAPI instance
app = FastAPI()

# Loading environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
os.environ["OPENAI_API_KEY"] = API_KEY

# Defining file paths for prospect and company information
prospect_info_path = './example_data/prospect_info.txt'
company_info_path = './example_data/company_info.txt'

# Health Path
@app.get('/')
async def health_check():
    return { "message" : "health check status 200"}

# Updating Propsect Info
@app.post('/update_prospect_info')
async def udpate_prospect_info(data: ProspectUpdateModel):
    try:
        # Extract the updated prospect information
        updated_info = data.prospect_info

        """
            Going to write this a S3 bucket in the cloud
            Going to write this a S3 bucket in the cloud
        """

        # Write the updated information to the prospect_info.txt file
        with open(prospect_info_path, "w") as file:
            file.write(updated_info)

        return {'message': 'Prospect information updated successfully'}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Updating Company Info
@app.post('/update_company_info')
async def udpate_company_info(data: CompanyUpdateModel):
    try:
        # Extract the updated prospect information
        updated_info = data.company_info

        """
            Going to write this a S3 bucket in the cloud
            Going to write this a S3 bucket in the cloud
        """
        # Write the updated information to the prospect_info.txt file
        with open(prospect_info_path, "w") as file:
            file.write(updated_info)

        return {'message': 'Company information updated successfully'}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




"""
    # Read company information from a file
    with open(company_info_path, "r") as file:
        company_info = file.read()

        with open(prospect_info_path, "r") as file:
    file_contents = file.read()

"""



def fetch_info_from_cloud_storage(url):
    # Use your cloud storage library or SDK to fetch the content from the URL
    # For example, using AWS S3 and the boto3 library:
    # s3 = boto3.client('s3')
    # content = s3.get_object(Bucket='your-bucket-name', Key=url)['Body'].read().decode('utf-8')
    with open(url, "r") as file:
        content = file.read()

    return content

def load_and_split_document(prospect_info):
    # Loading prospect information
    loader = TextLoader(prospect_info)
    data = loader.load()
    print(f"You have {len(data)} main document(s)")

    # Split documents to avoid token limits and enable prompt engineering; Will be taking chunks and map_reducing
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap  = 0
    )
    return text_splitter.split_documents(data)

# Defining map_prompt: This prompt is used during initial processing of individual split documents.    
map_prompt = """ 
    % MAP PROMPT

    Below is a section of a website about {prospect}

    Write a concise summary about {prospect}. If the information is not about {prospect}, exclude it from your summary.

    {text} 
"""
    
# Define combine_prompt: This prompt is used when combining the outputs of the map pass.
combine_prompt = """
    % COMBINE PROMPT
    
    Your goal is to write a personalized outbound email from {sales_rep}, a sales rep at {company} to {prospect}.
    
    A good email is personalized and combines information about the two companies on how they can help each other.
    Be sure to use value selling: A sales methodology that focuses on how your product or service will provide value to the customer instead of focusing on price or solution.

    % INFORMATION ABOUT {company}:
    {company_information}

    % INFORMATION ABOUT {prospect}:
    {text}
    
    % INCLUDE THE FOLLOWING PIECES IN YOUR RESPONSE:
        - Start the email with the sentence: "We love that {prospect} helps teams..." then insert what they help teams do.
        - The sentence: "We can help you do XYZ by ABC" Replace XYZ with what {prospect} does and ABC with what {company} does 
        - A 1-2 sentence description about {company}, be brief
        - End your email with a call-to-action such as asking them to set up time to talk more 
"""

# Define endpoint for email generation
@app.post('/generate_email')
async def generate_email(data: EmailGenerationRequest):
    try:
        # Fetch prospect information from the cloud storage
        prospect_info_url = data.prospect_info_url
        prospect_info = fetch_info_from_cloud_storage(prospect_info_url)

        # Fetch company information from the cloud storage (similar to the prospect information)
        company_info_url = data.company_info_url
        company_info = fetch_info_from_cloud_storage(company_info_url)

        # Loading and spliting propsect info
        docs = load_and_split_document(prospect_info)
        print (f"You now have {len(docs)} split documents")

        # Map_prompt: This prompt is used during initial processing of individual split documents.    
        map_prompt_template = PromptTemplate(
            template=map_prompt, 
            input_variables=["text", "prospect"])

        # Combine_prompt: This prompt is used when combining the outputs of the map pass.
        # Define prompt template for combined map_prompt output summarization
        combine_prompt_template = PromptTemplate(
            template=combine_prompt, 
            input_variables=["company", "company_information", "sales_rep", "prospect", "text"])

        # Initialize the OpenAI language model
        llm = OpenAI(temperature=.5)

        # Define a text generation chain
        # Even though we're not summarizing, we use the load_summarize_chain for efficient map-reduce processing.
        chain = load_summarize_chain(
            llm,
            chain_type="map_reduce",
            map_prompt=map_prompt_template,
            combine_prompt=combine_prompt_template,
            verbose=True
        )

        ### >>> NEED TO QUERY COMPANY NAME
        ### >>> NEED TO QUERY PROSPECT NAME

        # Generate text based on provided documents and prompts
        output = chain({
            "input_documents": docs,
            "company": "RapidRoad",
            "company_information" : company_info,
            "sales_rep" : "Michael",
            "prospect" : "GitLab"
        })

        # Print the generated output
        return {"output_text": output['output_text']}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
