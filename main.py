import os
from dotenv import load_dotenv

from langchain.document_loaders import TextLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
os.environ["OPENAI_API_KEY"] = API_KEY

# Define file paths for prospect and company information
prospect_info_path = './example_data/prospect_info.txt'
company_info_path = './example_data/company_info.txt'

# Read company information from a file
with open(company_info_path, "r") as file:
    company_info = file.read()


# Load prospect information from a file
def get_prospect_data():
    loader = TextLoader(prospect_info_path)
    return loader.load()

data = get_prospect_data()
print(f"You have {len(data)} main document(s)")


# Split documents to avoid token limits and enable prompt engineering; Will be taking chunks and map_reducing
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap  = 0
)

docs = text_splitter.split_documents(data)
print (f"You now have {len(docs)} split documents")


# Define map and combine prompts for text generation
# Define map_prompt: This prompt is used during the initial processing of documents.
# It instructs the model to generate concise summaries about the prospect from each document.
# Placeholders like {text} and {prospect} will be replaced with actual content during text generation.
map_prompt = """ 
    % MAP PROMPT

    Below is a section of a website about {prospect}

    Write a concise summary about {prospect}. If the information is not about {prospect}, exclude it from your summary.

    {text} 
    """

# Define prompt template for summarization of sections
map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text", "prospect"])


# Define combine_prompt: This prompt is used when combining the outputs of the map pass.
# It guides the model to compose personalized outbound emails, incorporating information about both companies.
# Placeholders like {company}, {company_information}, {sales_rep}, {prospect}, and {text} will be replaced during text generation.
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

# Define prompt template for combined map_prompt output summarization
combine_prompt_template = PromptTemplate(
    template=combine_prompt, 
    input_variables=["company", "company_information", "sales_rep", "prospect", "text"])


# Initialize the OpenAI language model
llm = OpenAI(temperature=.5)

# Define a text generation chain
# Even though we're not summarizing, we use the Summarize framework for efficient map-reduce processing.
# Prompts (map_prompt_template and combine_prompt_template) provide specific directions for the text generation process.
chain = load_summarize_chain(
    llm,
    chain_type="map_reduce",
    map_prompt=map_prompt_template,
    combine_prompt=combine_prompt_template,
    verbose=True
)

# Generate text based on provided documents and prompts
output = chain({
    "input_documents": docs,
    "company": "RapidRoad",
    "company_information" : company_info,
    "sales_rep" : "Michael",
    "prospect" : "GitLab"
})

# Print the generated output
print(output['output_text'])