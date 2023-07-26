from dataclasses import asdict
from ssl import ALERT_DESCRIPTION_ACCESS_DENIED
from subprocess import STARTF_USESTDHANDLES
from serial import Serial
from keras.models import load_model
import time
import mysql.connector
import requests

ser = Serial('COM5', baudrate = 9600, timeout=5)

model_vertical = load_model("bnn_vertikal_terbaik.h5")
model_horizontal = load_model("bnn_horizontal_terbaik.h5")

sensor1_predict = 0
sensor2_predict = 0
notif = 0

# def write_read(x):
#     ser.write(bytes(x, encoding='utf-8'))
#     time.sleep(0.05)
#     data = ser.readline()
#     return data

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="mydatabase"
)

mycursor = mydb.cursor()


while 1:

    url = "https://u-elektrik.my.id/api/token/20220812-1"
    response = requests.get(url)
    token = response.json()

    prosestoken = token['token']
    # print (prosestoken)

    for i in prosestoken:
        # print(i)

        if i == "1":
            # print("ok")
            mycursor.execute("SELECT status FROM data")
            stat = mycursor.fetchall()
            status = stat[0][0]

            if status == 0:
                asdict

                arduinoData = ser.readline().decode('ascii')
                data = arduinoData.split(",")
                # time.sleep(5)

                print(data)
                data0 = data[0]
                data1 = data[1].rstrip()
                print(data0,data1)
                
                tus = 2
                sql1 = "UPDATE data SET sensor_ver = %s, sensor_hor = %s, status = %s WHERE id = 1"
                val1 = (data0, data1, tus)
                mycursor.execute(sql1, val1)
                mydb.commit()
                time.sleep(2)
                


            # print(status)

            if status == 1:
                arduinoData = ser.readline().decode('ascii')
                
                mycursor.execute("SELECT prediksi_ver, prediksi_hor FROM data")
                myresult = mycursor.fetchall()  
                prediksi_ver = myresult[0][0]
                prediksi_hor = myresult[0][1]
                # print(prediksi_ver, prediksi_hor)


                # print (data[0], data[1])

                if prediksi_ver != "y":

                    sensor1_predictint = prediksi_ver
                else:
                    sensor1_predictint = "y"


                if prediksi_ver != "y":
                    
                    sensor2_predictint = prediksi_hor
                else:
                    sensor2_predictint = "y"

                
                print(sensor1_predictint, sensor2_predictint)
                # time.sleep(4)

                kirim = str(str(sensor1_predictint) + "," + str(sensor2_predictint))
                value = ser.write(kirim.encode())
                print(value) # printing the value

                time.sleep(2)
                sql2 = "UPDATE data SET status = 0 WHERE id = 1"
                mycursor.execute(sql2)
                mydb.commit()
    # time.sleep(1)            

     
