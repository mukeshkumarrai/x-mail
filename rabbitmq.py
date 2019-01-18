import pika
import socket
import datetime
import Error_model
import sys
import json
from tkinter import messagebox

class rabbitmq(object):
    def __init__(self,hotel_id,user_id):
        with open('config.json') as conf_data:
                    conf               = json.load(conf_data)
                    mq_url             = conf['mq_url']
                    mq_port            = conf['mq_port']
                    mq_user            = conf['mq_user']
                    mq_pass            = conf['mq_pass']
                    self.error_url     =    socket.gethostbyname(socket.gethostname())
                    self.created_on    = str(datetime.datetime.utcnow())
                    self.service_name  = 'phyton X Mail '
                    self.mq_url        = mq_url
                    self.mq_port       = mq_port
                    self.mq_user       = mq_user
                    self.mq_pass       = mq_pass
                    self.hotel_id      = hotel_id
                    self.created_by    = user_id
    def method_a(self, error_msg,error_type):
            
            obj = Error_model.Error_log()
            obj.error_msg = error_msg
            obj.created_by =self.created_by
            obj.user_id = self.created_by
            obj.hotel_id = self.hotel_id
            obj.created_on = self.created_on
            obj.service_name='phyton X Mail '
            obj.error_url = socket.gethostbyname(socket.gethostname())
            obj.error_type = error_type
            classObj = obj
           
            classJson = json.dumps(vars(classObj))
            # print(classJson)
            credits = pika.PlainCredentials(self.mq_user,self.mq_pass)
            params = pika.ConnectionParameters(self.mq_url,self.mq_port,'/',credits)
            try:
                connection = pika.BlockingConnection(parameters=params)
                # print("Rabbit connection sucsess")
            except Exception as e :
                print("Rabbit connection Failed")
                print(e)
            channel = connection.channel()
            # channel.queue_declare(queue='in_error_queue')
            try:
                        channel.basic_publish(exchange='Log', routing_key='error', body=classJson)
                        print(classObj)
                        print("Sending data to rabbit MQ")
            except Exception as e :
                                     print('Authentication fialed')
                                     print(e)
            connection.close()