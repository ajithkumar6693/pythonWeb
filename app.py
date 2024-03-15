from flask import Flask, request, jsonify
import os
import fitz  # PyMuPDF
from openai import AzureOpenAI

app = Flask(__name__)


def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

    
# Endpoint to extract data from document
@app.route('/extractData', methods=['POST'])
def extractData():
    data = request.get_json()
    client = AzureOpenAI(
        api_key="d329beed866b40bba241a3fad10717af",
        api_version="2024-02-15-preview",
        azure_endpoint="https://samsungs23ultrapro.openai.azure.com/"
    )
    if 'pdfName' in data and 'question' in data:
        question = data['question']
        pdfName = data['pdfName']
        pdf_text = extract_text_from_pdf("./" + pdfName)
        conversation = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": pdf_text}
        ]
        conversation.append({"role": "user", "content": question})
        response = client.chat.completions.create(
            model="gpt35",  # Use your deployed model name
            messages=conversation
        )
        print(response.choices[0].message.content)
        return jsonify({'message': 'Success', 'responseMsg': response.choices[0].message.content}), 201
    else:
        return jsonify({'error': 'Invalid request, name and age are required'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8080)
