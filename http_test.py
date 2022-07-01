import os

from flask import Flask, request, render_template
import logging
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import os
from glob import glob

app = Flask(__name__)
os.makedirs("./save_data/", exist_ok= True)
save_path = "./save_data/"
device = dict()
print('server on')

@app.route('/')
@app.route('/api/watch/receiver', methods=['GET', 'POST'])
def receiver():
    if request.method == 'GET':
        return "OK"

    else:
        device_req = request.form["device"]
        time_req = request.form["time"]

        if device_req not in device.keys():

            brand = device_req.split()[0]
            deviceId = device_req.split()[1]

            # 저장 파일 만들기
            new_path = "./save_data/" + device_req + "/"
            os.makedirs(new_path, exist_ok=True)
            new_file = new_path + brand + "_" + deviceId + "_" + time_req + ".csv"
            new_df = pd.DataFrame(columns=['index', 'time', 'value'])

            print(new_df)
            new_df.to_csv(new_file)
            device[device_req] = {'time': [], 'value': [], 'index': [], 'path': new_file}

            print(f'[{device_req}] 측정 시작')
            print(new_file)

        tag_req = request.form["tag"]
        cur_device = device[device_req]

        if tag_req == "stop":

            # 데이터 로스 구하기
            total_data = cur_device['index'][-1]+1
            total_time = int(cur_device['time'][-1]/1000 - cur_device['time'][0]/1000)
            incorrect = total_data - len(cur_device['index'])

            data_acc = round(float((total_data - incorrect)/total_data)*100, 3)
            data_loss = round(float(incorrect/total_data)*100, 3)

            print(f'[{device_req}] 측정 종료')
            print(f'{total_time}초간 Data acc/loss: {data_acc}% / {data_loss}%')

            # save_df = pd.DataFrame(cur_device['time'], cur_device['value'], columns=['time', 'value'])
            # save_df.to_csv


            device.pop(device_req)

        else:
            value_req = request.form["value"]
            index_req = request.form["index"]
            # logging.info(value_req)

            cur_device['time'].append(int(time_req))
            cur_device['value'].append(value_req)
            cur_device['index'].append(int(index_req))

            print(f'[{device_req}] {index_req} {datetime.fromtimestamp(int(time_req)/1000)} Heart-rate :  {value_req} ')

            # 50개 마다 저장
            if int(index_req) % 50 == 0:
                print('update file')
                load_df = pd.read_csv(device[device_req]['path'])
                if 'Unnamed: 0' in load_df.columns:
                    load_df.drop(['Unnamed: 0'], axis=1, inplace=True)

                temp_df = pd.DataFrame({'index': cur_device['index'], 'time': cur_device['time'], 'value' :cur_device['value']})
                pd.concat([load_df, temp_df]).to_csv(cur_device['path'], index=False)

                cur_device['time'] = []
                cur_device['value'] = []
                cur_device['index'] = []



        # received = request.form["time"], request.form["value"]
        # app.logger.info(received)
        return "OK"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port='5002')