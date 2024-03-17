# chagokchagok-hw
차곡차곡 프로젝트 HW 파트

## server
### apis
| url | data | return value|
|:--|:--|:--|
|car-plate/image/|image data(decoding by base64)|car plate number|
|entrance | image data(decoding by base64)|response from spring server|
|hall | image data(decoding by base64)|response from spring server(parkinglot section)|
|exit-way| image data(decoding by base64)|response from spring server(parkinglot section)|
|open-area/{str:area_num}|area_number| ok sign|
|bar-open||area_number or empty|
|ent-open||get : ok, post:open sign or close|

- car-plate/image : 이미지에서 차 번호를 잘 찾아오는지 테스트 용 api
- entrance : 이미지에서 차 번호를 추출해 차량의 번호가 valid 하다면 true를 return 하고 spring server로 전송, invalid 하다면 false를 return 하는 api
- hall : 이미지에서 차 번호를 추출해 spring server 로 보내 해당 차량의 주차 구역을 리턴받아 하드웨어 쪽으로 리턴해주는 api
- exit-way : 이미지에서 차 번호를 추출해 spring server로 보내 해당 차량의 주차 구역을 리턴받아 하드웨어 쪽으로 리턴해주는 api
- open-area/{str:area_num}/ : 관리자 (spring server)로 부터 어떤 주차 구역의 차단을 해제해야 하는지 입력받아 저장하는 api
- bar-open : 어떤 주차구역을 해제해야 하는지 알려주는 api
- ent-open
    - GET : 입구의 주차 차단을 해제 해도 된다는 신호를 입력받는 api
    - POST : 입구의 주차 차단을 해제해도 되는지 여부를 알려주는 api

## client
### funtions
- entrance client
    - capture : 라즈베리파이에 연결되어있는 웹캠을 사용해 차량을 촬영하고 base64로 디코딩해 data를 return 합니다
    - open_barricate : 호출되면 ent-open에 post 요청을 보내 주차장 입구의 차단 해제 가능여부를 1초 간격으로 확인합니다. 차단 해제가 가능하다면 입구측 차단바를 해제하고 5초간 아두이노를 정지시킨 후 return 합니다
    - main : 차량이 진입하는 것을 감지하면 capture()를 호출하고 entrance api를 호출해 차량의 번호판의 유효성을 검사하고, 유효하다면 open_barricate()를 호출합니다. 해당 과정을 1초에 한번씩 반복합니다
- exit hall client
    - capture1 : 라즈베리파이에 연결되어있는 복도쪽 캠을 이용해 차량을 촬영하고 base64로 디코딩해 data를 return 합니다
    - capture2 : 라즈베리파이에 연결되어있는 출구쪽 캠을 이용해 차량을 촬영하고 base64로 디코딩해 data를 return 합니다
    - bar : 테스트용 코드
    - call_back : library 안에 있는 set_pin_mode_sonar를 위한 callback 함수
    - main : 크게 복도(hall)과 출구(exit), 주차자리 개방 여부 로 구분할 수 있습니다. 모든 과정은 1초에 한번 씩 반복되며, 주차자리 개방 여부는 3초에 한번씩만 확인합니다.
        - hall : 차량이 진입한 것을 확인하면, capture1()을 호출하고 hall api를 호출합니다. return 받은 주차 자리 번호를 확인하고 해당하는 자리의 주차 자리의 차단을 해제합니다.
        - exit : 차량이 진입한 것을 확인하면, capture2()를 호출하고 exit-way api를 호출합니다. 출구 측 차단바를 해제하고, return 받은 주차 자리 번호를 확인하고 해당하는 주차 자리를 차단합니다. 이때, 해당 자리에 차량이 존재한다면, spring server로 해당 차량이 있음을 자동으로 신고하고, 주차자리를 차단하지 않습니다.
        - 주차자리 개방 여부 : bar-open api를 호출하여, empty 라면 무시하고, 주차자리 번호가 return 되었을 경우, 해당하는 자리의 차단을 해제합니다.