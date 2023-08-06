# -*- coding: utf-8 -*-
from pydoc import cli
import onmqtt
import time

product_id=  '533618'# 产品ID
device_id = '966637746' # 设备ID
auth_info = '1' # 鉴权信息
# def on_msg(client, userdata, msg):
#     print("getinfo:",msg.payload.decode('utf8'))
client = onmqtt.onenet_mqtt(product_id,device_id, auth_info)
# client.on_message = on_msg # 在连接之前设置回调函数on_message
client.connect_onenet()

temperature = 0
client.loop_start() # must exist
getinfo = 0
while 1:
    temperature += 1 
    # print('test')
    client.qpublish("temp_cpu", temperature)
    getinfo = client.getinfo()
    # print("in test_file",getinfo,type(getinfo))
    # print('test')
    if(getinfo != -1):
        print("getinfo:",getinfo)
        
    time.sleep(1)
# client.loop_stop() # 死循环不会执行到这

