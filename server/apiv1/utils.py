import numpy as np
import cv2
from PIL import ImageFont, ImageDraw, Image
import torch, easyocr
from io import BytesIO


# init part
car_model = torch.hub.load("ultralytics/yolov5", 'yolov5s', force_reload=True, skip_validation=True)
lp_model = torch.hub.load("ultralytics/yolov5", 'custom', 'lp_det.pt')
reader = easyocr.Reader(['en'], detect_network='craft', recog_network='best_acc', user_network_directory='lp_models/user_network', model_storage_directory='lp_models/models')
car_model.classes = [2,3, 5, 7]


def main(image_path):
    global car_model, lp_model, reader

    car_m = car_model
    lp_m = lp_model
    im, text = detect(car_m, lp_m, reader, image_path)
    return text


def detect(car_m, lp_m, reader, image_path):
    fontpath = "SpoqaHanSansNeo-Light.ttf"
    font = ImageFont.truetype(fontpath, 200)

    im = Image.open(image_path)
    to_draw = np.array(im)
        
    result_text = []

    result = lp_m(im)
    if len(result) == 0:
        result_text.append('Car was not detected')
    else:
        for rslt in result.xyxy[0]:
            x2,y2,x3,y3 = [item1.cpu().detach().numpy().astype(np.int32) for item1 in rslt[:4]]
            try:
                extra_boxes = 0
                im = cv2.cvtColor(cv2.resize(to_draw[y2 - extra_boxes:y3 + extra_boxes,x2 - extra_boxes:x3 + extra_boxes], (224,128)), cv2.COLOR_BGR2GRAY)
                text = reader.recognize(im)[0][1]
                result_text.append(text)
            except Exception as e:
                return cv2.resize(to_draw, (1280,1280)), ""
            img_pil = Image.fromarray(to_draw)
            draw = ImageDraw.Draw(img_pil)
            draw.text( (x2-100,y2-300),  text, font=font, fill=(255,0,255))
            to_draw = np.array(img_pil)
            cv2.rectangle(to_draw, (x2.item(),y2.item()),(x3.item(),y3.item()),(255,0,255),10)

        return cv2.resize(to_draw, (1280,1280)), result_text
    
    return cv2.resize(to_draw, (1280,1280)), result_text


def plate_recog(image_data):
    img_out = Image.open(BytesIO(image_data))
    img_out = np.array(img_out)
    img_out = cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB)
    
    cv2.imwrite('./image.png', img_out)
    text = main('./image.png')
    return text


"""
AI Source From
https://github.com/gyupro/EasyKoreanLpDetector/tree/main
"""