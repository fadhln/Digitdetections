from flask import Flask, request
from detect import detect_digit
from response import createResponse
from validate import InputSchema
from marshmallow import ValidationError


# schema = InputSchema()

app = Flask(__name__)

@app.route('/hello', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"


@app.route('/xcamp_smartmeter', methods=['POST'])
def detect_api():
    try:
        result = InputSchema().load(request.json)
        image_url = result['url']
        info = result['details']
    except ValidationError as err:
        return createResponse(err.messages,"None", 400)
    
    try :
        predicted, score, status, code = detect_digit(image_url, info)

        return createResponse(status, info, code, predicted, score)
    except :
        status = 'an error occured'
        return createResponse(status, info, code=500)    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)