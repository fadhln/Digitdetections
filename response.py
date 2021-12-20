
from flask import jsonify
from datetime import datetime

def createResponse(status, info, code, predicted=[], score=[]):
    date = datetime.now()
    temp = []
    if(status == "Success"):
        for item in predicted:
            temp.append(
                {"predicted" : item,
                "score" : score[predicted.index(item)]
                })
        template = jsonify({
            "status" : status,
            "code" : code,
            "info"  : info,
            "date" : date,
            "data" : temp,

            # "data":{
            #     "predicted" : predicted,
            #     "score" : score
            # }  
        })
        return template, code
    else:
        template = jsonify({
            "status" : "Error",
            "code" : code,
            "info"  : info,
            "date" : date,
            "message" : status  
        })
        return template, code
