import numpy as np
import cv2
from paddleocr import PaddleOCR
import os
import urllib.request
import re
         
def digitocr(image_path):
    ocr = PaddleOCR(lang='en')
    result = ocr.ocr(image_path)
    texts = [res[1][0] for res in result]
    scores = [res[1][1] for res in result]
    return texts, scores


OUTPUT_FILE='./Utils/predicted.jpg'
LABELS_FILE='./Utils/obj.names'
CONFIG_FILE='./Utils/yolov4-obj.cfg'
WEIGHTS_FILE='./Utils/yolov4-obj_final.weights'
CONFIDENCE_THRESHOLD=0.3
LABELS = open(LABELS_FILE).read().strip().split("\n")

def detect_digit(image_path, info):
    boxes = []
    confidences = []
    classIDs = []
    
    net = cv2.dnn.readNetFromDarknet(CONFIG_FILE, WEIGHTS_FILE)
    try:
        with urllib.request.urlopen(image_path) as url:
            req = url.read()
            arr = np.asarray(bytearray(req), dtype=np.uint8)
        image = cv2.imdecode(arr, -1)
    except:
        return [], [], "cannot open image from url", 400
    
    image_clone = image.copy()
    (H, W) = image.shape[:2]

    
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]


    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > CONFIDENCE_THRESHOLD:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)
    
   
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD,CONFIDENCE_THRESHOLD)
    
    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

    try:    
        _image = image_clone[y-7:y+h+7, x-7:x+w+7]
        cv2.imwrite(f"result_layar_{info}.jpg", _image)
        result_path = f"result_layar_{info}.jpg"
        detected, scores = digitocr(result_path)
    except:
        return [], [], "error while detecting", 500
    
    digits = []
    score = []
    for item in detected:
        try:
            x = re.findall(r"\d+",item)
            y=""
            for number in x:
                y += number
            if(int(y)>0 and y!='' and len(y)>=4):
                digits.append(str(y))
                score.append(str(scores[detected.index(item)]))
        except:
            pass
    
    if os.path.exists(f"result_layar_{info}.jpg"):
        os.remove(f"result_layar_{info}.jpg")
    
    if(len(digits)==0):
        return digits, score, "nothing detected or detection failed", 400
    
    return digits, score, "Success", 200
