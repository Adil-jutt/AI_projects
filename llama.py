from fastapi import FastAPI, Request
from pydantic import BaseModel
import ollama
import ast

app = FastAPI()

class EmailRequest(BaseModel):
    orderNum: str

class extractEmail(BaseModel):
    email:str

@app.post("/process_email")
async def process_email(request: extractEmail):
    email = request.email
    print("Api Hit.................")
    # Step 1: Extract order number and name
    extraction_response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': f'You are supposed to extract the order number and sender name (May find it under regards) from the provided email. Your response should be in a json format with the key (orderNumber,Name) and Do not add anything in your response other than the json. here is the email: \n\n {email}'
        },
    ])

    extraction_res = extraction_response['message']['content']
    try:
        jsonobj = ast.literal_eval(extraction_res)
        order_num = jsonobj['orderNumber']
        customer_name = jsonobj['Name']
        return {"orderNum":order_num,"customerName":customer_name}
    except (ValueError, SyntaxError) as e:
        return {"error": "Failed to parse response", "details": str(e)}
    


@app.post("/write_email")
async def process_email(request: EmailRequest):

    orderNum = request.orderNum
    status = "shipped"
    date = "20 May 2024"
    order = "Hp laptop"

    response = ollama.chat(model='llama3', messages=[
    {
        'role': 'user',
        'content': f'Your are supposed to write a personalized email to our customers in which the status of the order will be presented in a professional and humanized manner. These are the details. order Number : {orderNum}\n delivery status: {status}\n delivery date: {date} \n ordered product: {order}. Donot mention anything that is not provided and do not assume anything. do not leave empty blanks'
    },
    ])
    email = response['message']['content']
    return {"email": email}