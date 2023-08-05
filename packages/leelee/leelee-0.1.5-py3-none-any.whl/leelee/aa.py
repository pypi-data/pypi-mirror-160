import pymssql
import requests
from PIL import Image
import base64
from io import BytesIO

server = '106.10.107.2'
# 데이터 베이스 이름
database = 'farm'
# 접속 유저명
username = 'sa'
# 접속 유저 패스워드
password = 'sejoongDB9778@$'

# MSSQL 접속
cnxn =  pymssql.connect(server , username, password, database,port=1455)

cursor = cnxn.cursor()

def get_server():
    global server
    global database
    global username
    global password
    server = '106.10.107.2'
    # 데이터 베이스 이름
    database = 'smartfarm'
    # 접속 유저명
    username = 'sa'
    # 접속 유저 패스워드
    password = 'sejoongDB9778@$'
    
    return server

def get_database():
    global server
    global database
    global username
    global password
    server = '10.0.0.2'
    # 데이터 베이스 이름
    database = 'farm'
    # 접속 유저명
    username = 'sa'
    # 접속 유저 패스워드
    password = 'sejoongDB9778@$'
    
    return database
def get_username():
    global server
    global database
    global username
    global password
    server = '10.0.0.2'
    # 데이터 베이스 이름
    database = 'game_calendar'
    # 접속 유저명
    username = 'sa'
    # 접속 유저 패스워드
    password = 'sejoongDB9778@$'
    
    return username

def get_password():
    global server
    global database
    global username
    global password
    server = '10.0.0.2'
    # 데이터 베이스 이름
    database = 'game_calendar'
    # 접속 유저명
    username = 'sa'
    # 접속 유저 패스워드
    password = 'sejoongDB9778@$'
    
    return password

def get_door(data):
    global door
    sql = "SELECT TOP(1) * FROM status where no = "+str(data)
    cursor.execute(sql)
    row = cursor.fetchone()
    door = row[0]
    return door

def get_light(data):
    global light
    sql = "SELECT TOP(1) * FROM status where no = "+str(data)
    cursor.execute(sql)
    row = cursor.fetchone()
    light = row[1]
    return light

def get_fan(data):
    global fan
    sql = "SELECT TOP(1) * FROM status where no = "+str(data)
    cursor.execute(sql)
    row = cursor.fetchone()
    fan = row[2]
    return fan

def get_camera(data):
    global camera
    sql = "SELECT TOP(1) * FROM status where no = "+str(data)
    cursor.execute(sql)
    row = cursor.fetchone()
    camera = row[3]
    return camera

def send_photo(data):
    url = 'http://210.91.154.159/smartfarm/insert_farm_img'+data+'.php'


    with open("image.jpg", "rb") as image_file:
        binary_image = image_file.read()
    # Base64로 인코딩
    binary_image = base64.b64encode(binary_image)
    # UTF-8로 디코딩 
    binary_image = binary_image.decode('UTF-8')

    code = requests.post(url,data={'data':str(binary_image)})
    # with open("image.jpg", "rb") as image_file:
    #     binary_image = image_file.read()
    # sql = "INSERT INTO dbo.images (image_data,study_no) VALUES ('"+str(binary_image)+"','"+str(data)+"')"
    # cursor.execute(sql)
    # cnxn.commit()

def send_data(data,value,h,t,adcValue,date_time):

    sql = "INSERT INTO sensor (temp,humidity,cdc,water,date_time,study_no) VALUES('"+str(t)+"','"+str(h)+"','"+str(value)+"','"+str(adcValue)+"','"+str(date_time)+"','"+str(data)+"')"
    cursor.execute(sql)
    cnxn.commit()
