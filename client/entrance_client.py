import cv2
from pymata4 import pymata4
import time
import requests
import base64
# from queue import Queue


trigpin_entrance = 2
echopin_entrance = 3
motor_entrance = 4

board = pymata4.Pymata4()


def call_back(data):
    return


board.set_pin_mode_sonar(trigpin_entrance, echopin_entrance, call_back)
board.set_pin_mode_servo(motor_entrance)

# import threading

# image_queue = Queue()

apiurl = 'http://i10b301.p.ssafy.io:8081/apiv1/'


def capture():
    # connect to webcam
    cap1 = cv2.VideoCapture(0)

    # set frame
    cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # capture
    ret, frame = cap1.read()

    # disconnect webcam
    cap1.release()

    # save image
    cv2.imwrite('./image.jpg', frame)

    # open image as binary data
    image = open('image.jpg', 'rb')

    # encoding
    base64_str = base64.b64encode(image.read())
    # decoding and return
    return base64.b64decode(base64_str)


def open_barricate():
    entrance_url = f'{apiurl}ent-open/'
    while True:
        try:
            print('here?')

            time.sleep(1)
            ent_response = requests.post(entrance_url)
            ent_res = ent_response.json()
            print(ent_res)
            if ent_res['response'] == 'open':
                board.servo_write(motor_entrance, 0)
                time.sleep(5)
                return
        except:
            pass


def main():
    while 1:
        try:
            time.sleep(1)
            dist = board.sonar_read(trigpin_entrance)
            print(dist)
            if dist[0] <= 7:
                image_source = capture()
                entrance_url = f'{apiurl}entrance/'
                entrance_response = requests.post(entrance_url, data=image_source)
                entrance_result = entrance_response.json()
                print(entrance_result)
                if entrance_result['response'] == True:
                    # start to check
                    open_barricate()
                    
                # if entrance_result:
                #     board.servo_write(motor_entrance, 0)
                # time.sleep(5)
            board.servo_write(motor_entrance, 90)
        except Exception:
            board.shutdown()
            

if __name__ == "__main__":
    main()