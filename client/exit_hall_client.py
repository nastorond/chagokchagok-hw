import cv2
from pymata4 import pymata4
import time
import requests
import base64

# varialbes
# for auto report system
trigpin_section = 2
echopin_section = 3

# for hallway capture trigger
trigpin_hall = 6
echopin_hall = 5
# each parking lot's barricade servo
# need to change variable name or setting where it is
motor_hall_1 = 7
motor_hall_2 = 8

# for exit capture trigger
trigpin_exit = 9
echopin_exit = 10
# exit's barricade servo
motor_exit = 11

# set board
board = pymata4.Pymata4()


def capture1():
    # connect to webcam
    cap1 = cv2.VideoCapture(2)

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


def capture2():
    # connect to webcam
    cap2 = cv2.VideoCapture(0)

    # set frame
    cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # capture
    ret, frame = cap2.read()

    # disconnect webcam
    cap2.release()

    # save image
    cv2.imwrite('./image.jpg', frame)

    # open image as binary data
    image = open('image.jpg', 'rb')

    # encoding
    base64_str = base64.b64encode(image.read())
    # decoding and return
    return base64.b64decode(base64_str)


# will add managing system after completing others
def bar():
    bar_url = 'http://127.0.0.1:8000/api/v1/admin/bar/'
    bar_response = requests.post(bar_url)
    bar_result = bar_response.json()
    park_no = bar_result['park_no'][0]
    if park_no:
        # open = 0
        # close = 90
        board.servo_write(f'motor_hall_{park_no}', 0)


# callback func for executing
def call_back(data):
    dis = data[2]

# hallway pin settings
board.set_pin_mode_sonar(trigpin_hall, echopin_hall, call_back)
board.set_pin_mode_servo(motor_hall_1)
board.set_pin_mode_servo(motor_hall_2)

# exit pin settings
board.set_pin_mode_sonar(trigpin_exit, echopin_exit, call_back)
board.set_pin_mode_servo(motor_exit)

# auto report system pin setting
board.set_pin_mode_sonar(trigpin_section, echopin_section, call_back)

# AIserver url
url = 'http://i10b301.p.ssafy.io:8081/apiv1/'
# backend server url
spring_url = 'https://chagokchagok.store/api/'


def main():
    cnt = 0
    while 1:
        try:
            time.sleep(1)
            cnt += 1
            hall_dis = board.sonar_read(trigpin_hall)
            exit_dis = board.sonar_read(trigpin_exit)
            sect_dis = board.sonar_read(trigpin_section)
            print(hall_dis)
            print(exit_dis)
            print(sect_dis)

            # hall way logic
            if hall_dis[0] <= 7:
                # data processing
                image_source = capture1()
                # request url
                hall_url = f'{url}hall/'
                # request to django

                hall_response = requests.post(hall_url, data=image_source)
                hall_result = hall_response.json()
                # need to change conditions after checking
                try:

                    if hall_result:
                        print('here')
                        if hall_result['park_id'] == 'A1':
                            board.servo_write(motor_hall_1, 0)
                        else:
                            board.servo_write(motor_hall_2, 0)
                    time.sleep(5)
                except:
                    print(hall_result)

            # exit logic
            if exit_dis[0] <= 7:
                # data processing
                image_source = capture2()
                # reuqest url
                exit_url = f'{url}exit-way/'
                # request to django
                exit_response = requests.post(exit_url, data=image_source)
                exit_result = exit_response.json()
                print(exit_result)
                if exit_result:
                    # open barricate for exit
                    board.servo_write(motor_exit, 0)
                    
                    # check car's parking section
                    # will change condition after deciding parking section number 1 to another
                    section = exit_result['response']
                    print(section)
                    if section == 'A2':
                        # check parking section is empty
                        # if it is not empty
                        if sect_dis[0] <= 7:
                            print('here?')
                            report_url = f'{spring_url}park/auto?location={section}'
                            headers = {'Content-type': 'application/json', 'charset': 'utf8'}
                            hall_response = requests.get(report_url, headers=headers)
                            print(hall_response)
                            
                        # if it is empty
                        else:
                            board.servo_write(motor_hall_2, 90)
                    else:
                        board.servo_write(motor_hall_1, 90)
                time.sleep(5)
            

            if cnt == 3:
                cnt = 0
                print('CHECK')
                # url
                check_managing_url = f'{url}bar-open/'
                try:
                    bar_response = requests.get(check_managing_url)
                    print(bar_response)
                    area_value = bar_response.json()['response']
                except:
                    area_value = 'empty'
                if area_value == 'empty':
                    pass
                elif area_value == '2':
                    # open = 0
                    board.servo_write(motor_hall_2, 0)
                elif area_value == '1':
                    board.servo_write(motor_hall_1, 0)

            # activate barricate at exit   
            board.servo_write(motor_exit, 90)

        except Exception:
            board.shutdown()
            print('error')
            break


if __name__ == "__main__":
    main()