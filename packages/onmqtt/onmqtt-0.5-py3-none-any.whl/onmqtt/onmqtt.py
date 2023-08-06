# -*- coding: utf-8 -*-
from time import time
import paho.mqtt.client as mqtt
from datetime import datetime
import json
info = -1
times = 0
def on_msg(client, userdata, msg):
    global info,times
    info = msg.payload.decode('utf8')
    times = 1
    print("TIMES[{}] getinfo:{}".format(times,info))
class onenet_mqtt(mqtt.Client):
    host = '183.230.40.39'  # mqtt.heclouds.com
    port = 6002

    def __init__(self, pid, did, auth):
        '''
        pid: Product ID，产品ID,
        did：Device ID， 设备ID,
        auth: auth_info, 鉴权信息
        keepalive: 心跳时间
        '''
        self.product_id = pid 
        self.device_id = did
        self.auth_info = auth
        self.info = -1
        super().__init__(did)
        super().username_pw_set(pid, password=auth)
        self.on_message = on_msg
    def connect_onenet(self):
        super().connect(self.host, self.port, keepalive=60)  # 心跳
        pass

    def __packdata(self, data):
        ''' 
        onenet mqtt 数据格式：数据类型x1 数据长度x2 数据内容
        '''
        jdata = json.dumps(data)
        jlen = len(jdata)
        arr = bytearray(jlen + 3)
        arr[0] = 1  # publish数据类型为json
        arr[1] = int(jlen / 256)  # json数据长度 高位字节
        arr[2] = jlen % 256  # json数据长度 低位字节
        arr[3:] = jdata.encode('utf-8')  # json数据
        return arr

    def ppublish(self,
                topic='$dp',
                payload=None,
                qos=0,
                retain=False,
                properties=None):
        '''
        这里的payload是一个字典
        '''
        payload = self.__packdata(payload)
        return super().publish(topic, payload, qos, retain, properties)

    def qpublish(self, key, value, qos=0):
        '''
        快速发布信息。
        '''
        values = {
            'datastreams': [{
                "id": key,
                "datapoints": [{
                    "at": datetime.now().isoformat(),
                    "value": value
                }]
            }]
        }
        payload = self.__packdata(values)
        return super().publish('$dp', payload, qos)
    def getinfo(self):
        global info,times
        # print("class times",times)
        if times!=0:
            times = 0
        else:
            info = -1
        # print("class info",info)
        return int(info)