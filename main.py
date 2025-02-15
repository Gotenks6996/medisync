from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import  create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv
from rag import rag
import os

# Load environment variables
load_dotenv()

#api key import from .env file
api_key = os.getenv('API_KEY')

#initialising llm model
llm = ChatGroq(groq_api_key=api_key, model_name="gemma2-9b-it")

# performing RAG
vectorstore = rag()

# Create FastAPI app
app = FastAPI()

# Define input models
class Symptoms(BaseModel):
    symptom: str

class General(BaseModel):
    question: str
    context: str

class Food(BaseModel):
    bmi: str
    cal : str

class Sleep(BaseModel):
    sleep: str




@app.get("/")
async def root():
    return {"message": "Welcome to MediSync API"}



#getting diseases request
@app.post("/get_diseases")
async def get_diseases(input_text: Symptoms):
    """
    Given the symptoms provided by the user, this function uses an LLM to suggest possible diseases.
    """
    try:
        # Construct the system prompt
        system_prompt = (
            "I am a Healthcare Chatbot specialized in disease detection based on symptoms. I will only respond if you provide symptoms for analysis."
            "If the input does not contain symptoms or is unrelated to disease detection, do not respond."
            "Given the symptoms provided, classify possible diseases into three categories based on likelihood: Highly Likely, Likely, and Unlikely. Consider factors such as commonality, symptom severity, and medical patterns. Provide a brief explanation for each classification."
            "After classification, provide a section titled 'What to Do' that includes:"
            "Home Remedies: Simple treatments using common household items or lifestyle changes."
            "Medicines:  Over-the-counter medications that may help, if applicable."
            "When to See a Doctor: Signs that indicate medical attention is necessary."
            f"{input_text.symptom}"
            
        )

        # Initialize the retriever
        retriever = vectorstore.as_retriever()

        # Define the prompt template
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{context}\n{input}"),
        ])

        # Create the document chain and retrieval chain
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)

        # Invoke the retrieval-augmented generation (RAG) chain
        response = rag_chain.invoke({
            "input": (
                "I am a Healthcare Chatbot specialized in disease detection based on symptoms. I will only respond if you provide symptoms for analysis."
                "If the input does not contain symptoms or is unrelated to disease detection, do not respond."
                "Given the symptoms provided, classify possible diseases into three categories based on likelihood: Highly Likely, Likely, and Unlikely. Consider factors such as commonality, symptom severity, and medical patterns. Provide a brief explanation for each classification."
                "After classification, provide a section titled 'What to Do' that includes:"
                "Home Remedies: Simple treatments using common household items or lifestyle changes."
                "Medicines:  Over-the-counter medications that may help, if applicable."
                "When to See a Doctor: Signs that indicate medical attention is necessary."
                f"{input_text.symptom}"
            )
        })

        # Extract the paraphrased text from the response
        paraphrased_text = response.get("answer", "No response generated.")
        
        return paraphrased_text

    except Exception as e:
        # Log the error and return a 500 status code with an error message
        print(f"Error in /get_diseases: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while processing your request: {e}")


#trained chatbot
@app.post("/general")
async def dis(input_text:General):
    """
    Resolves user's question
    """
    #prompt for the llm model
    system_prompt = (
        "Assume that you are a doctor and provide a clear, informative, and responsible answer to the user's question. Do not avoid the question by stating that you are not a medical professional. However, always emphasize the importance of consulting a healthcare provider for personalized medical advice.\n\n"
"Review the previous conversation (if available) to understand the context before answering:\n\n"
f"{input_text.context if input_text.context else 'No previous conversation available.'}\n\n"
"Now, answer the following question only if it is related to healthcare:\n\n"
f"{input_text.question}\n\n"
"Provide a concise and accurate response, If the question is unrelated to healthcare, politely inform the user that you can only assist with healthcare-related queries.\n\n"
"Do not exceed a text length of 5000 characters."
        
    )

    #vector embedding
    retriever = vectorstore.as_retriever()

    #prompt
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{context}\n{input}"),
    ])

    try:
        # Assume LLM object is preloaded
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        response = rag_chain.invoke({"input": "Assume that you are a doctor and provide a clear, informative, and responsible answer to the user's question. Do not avoid the question by stating that you are not a medical professional. However, always emphasize the importance of consulting a healthcare provider for personalized medical advice.\n\n"
"Review the previous conversation (if available) to understand the context before answering:\n\n"
f"{input_text.context if input_text.context else 'No previous conversation available.'}\n\n"
"Now, answer the following question only if it is related to healthcare:\n\n"
f"{input_text.question}\n\n"
"Provide a concise and accurate response, If the question is unrelated to healthcare, politely inform the user that you can only assist with healthcare-related queries.\n\n"
"Do not exceed a text length of 5000 characters."
        })
        paraphrased_text = response["answer"]
        return paraphrased_text
    except Exception as e:
        raise RuntimeError(f"Error: {e}")



#general healthcare chatbot
@app.post("/genera")
async def general(input_text: Symptoms):
    """
    This is a genral chatbot without RAG
    """

    # Define the prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", ""),
        ("human", f"{input_text.symptom}")
    ])

    try:
        # Generate response from LLM
        response = llm.invoke(prompt.format_messages())

        return response.content
    
    except Exception as e:
        return {"error": f"Error occurred: {e}"}


@app.post("/food")
async def general(input_text: Food):
    """
    This is a food chatbot without RAG
    """


    #prompt for the llm model
    system_prompt = (
        "You are a nutrition expert. Based on the user's BMI and previous 5 days calorie intake, provide a list of recommended amount of proteins, calories and carbohydrate need to take and it should be vegetarian. for all breakfast,lunch,snacks,dinner. Each recommendation should be less than 10 words and should always give 2 3 options (e.g., yogurt or curd, 2 or 3 rotis). Adjust the suggestions based on the user's BMI: For BMI above 25 (overweight/obese): Focus on calorie reduction, healthier choices, and weight management. For BMI between 18.5 and 24.9 (healthy weight): Focus on maintaining a balanced diet and sustaining current weight. For BMI below 18.5 (underweight): Suggest higher calorie foods for weight gain and nourishment. don't include talk to a doctor . Don't include this header. At last some motivational short lines."
        "My BMI is"
        f"{input_text.bmi}"
        "and my calorie intake is"
        f"{input_text.cal}"
    )
    #prompt
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
    ])

    try:
        # Generate response from LLM
        response = llm.invoke(qa_prompt.format_messages())

        return response.content
    
    except Exception as e:
        return {"error": f"Error occurred: {e}"}

    
@app.post("/sleep")
async def general(input_text: Sleep):
    """
    This is a sleep chatbot without RAG
    """


    #prompt for the llm model
    system_prompt = (
        "I will provide my bedtime for the previous days. Based on this data, analyze my sleep consistency and generate a 25-word feedback message. Highlight patterns, potential improvements, and a friendly suggestion for a healthier sleep routine. Also, identify the best and worst sleep time based on ideal sleep schedules (10:00 PM - 11:30 PM as best, past 2:00 AM as worst). my sleep time is "
        f"{input_text.sleep}"
        "give some emojis"
    )

    #prompt
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
    ])

    try:
        # Generate response from LLM
        response = llm.invoke(qa_prompt.format_messages())

        return response.content
    
    except Exception as e:
        return {"error": f"Error occurred: {e}"}