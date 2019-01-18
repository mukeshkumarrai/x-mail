import smtplib
import json
import sys
import base64
import logging

#for error model 
import Error_model
import pika
import socket
import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from tkinter import messagebox

from email.mime.base import MIMEBase
from email import encoders
import smtplib
import rabbitmq


logf = open("errorlog.txt", "w")
class Smpt( object):     
  
        # __init__ is known as the constructor          
        def __init__(self, host, port,hotel_id,user_id): 
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
                    self.host          = host 
                    self.port          = port 
                    self.created_on    = str(datetime.datetime.utcnow())
                    self.service_name  = 'phyton X Mail '
                    self.mq_url        = mq_url
                    self.hotel_id      = hotel_id
                    self.created_by    = user_id
        def connMQ(self, error_msg,error_type):
            logging.basicConfig(filename='audit.log',level=logging.ERROR,format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
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
                
            except Exception as e :
                logging.error(str(e))
                sys.exit(1)
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
            # return connection.close()
        def connectsmtp(self,host,port,user1,password): 
                smtp = smtplib.SMTP(host, port) 
                smtp.starttls() 
                if (user =='') or (password == ''):
                        messagebox.showinfo("Title", "a Tk MessageBox")
                        with open('config.json') as conf_data:
                            conf = json.load(conf_data)
                            user = conf['smtpuser']
                            password = conf['smtppassword']
                try:
                    # Authentication 
                    smtp.login(user, password) 
                    # rbmqobj.method_a('test','SMTP Authentication')
                except Exception as e :
                    # messagebox.showinfo("Title", "a Tk MessageBox")
                    self.connMQ(str(e),'SMTP Authentication')
                    # sys.exit(1)
                return smtp    
        def qrcode(self,smptconf,qrcode,strFrom,to,subject):
            reciverMaillist = []
            for x in to:
                    email=x['email']
                    reciverMaillist.append(email)    
                
            # Write base64 to file 
            imgdata = base64.b64decode(qrcode)
            filename = 'QRCODE.jpg'  # I assume you have a way of picking unique filenames
            with open(filename, 'wb') as f:
                    f.write(imgdata)



            # mailing system
                    
            # Create the root message and fill in the from, to, and subject headers
            msgRoot = MIMEMultipart('related')
            msgRoot['Subject'] = subject
            msgRoot['From'] = strFrom
            msgRoot['To'] = ", ".join(reciverMaillist)
            msgRoot.preamble = 'This is a multi-part message in MIME format.'
            msgAlternative = MIMEMultipart('alternative')
            msgRoot.attach(msgAlternative)


            # We reference the image in the IMG SRC attribute by the ID we give it below
            msgText = MIMEText('<b>Hi <i>Team ,</i><br> QR Code generatored For Hotel FCS</b> .<br><img src="cid:image1" height="250" width="250"><br>Regads <br>FCS Admin', 'html')
            msgAlternative.attach(msgText)

            # This example assumes the image is in the current directory
            fp = open(filename, 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()
            # print(msgImage)
            # Define the image's ID as referenced above
            msgImage.add_header('Content-ID', '<image1>')
            msgRoot.attach(msgImage)
            try:
                smptconf.sendmail(strFrom, reciverMaillist, msgRoot.as_string())
                print('email send')
                smptconf.quit()
            except Exception as e :
                self.connMQ(str(e),'mail sending Failed')
                print('mail sending Failed')
                # sys.exit(1)
        def plainmail(self,smptconf,body,strFrom,to,subject):
                # messagebox.showinfo("Plain Mail",body)
                reciverMaillist = []
                for x in to:
                        email=x['email']
                        reciverMaillist.append(email)    
                             

            # mailing system
                        
                # Create the root message and fill in the from, to, and subject headers
                msgRoot = MIMEMultipart('related')
                msgRoot['Subject'] = subject
                msgRoot['From'] = strFrom
                msgRoot['To'] = ", ".join(reciverMaillist)
                msgRoot.preamble = 'This is a multi-part message in MIME format.'
                msgAlternative = MIMEMultipart('alternative')
                msgRoot.attach(msgAlternative)


                # We reference the image in the IMG SRC attribute by the ID we give it below
                msgText = MIMEText(body, 'html')
                msgAlternative.attach(msgText)

            
                try:
                    smptconf.sendmail(strFrom, reciverMaillist, msgRoot.as_string())
                    print('email send')
                    smptconf.quit()
                except Exception as e :
                    self.connMQ(str(e),'mail sending Failed')
                    print('mail sending Failed')

        def method_a(self, error_msg,error_type):
            
            obj = Error_model.Error_log()
            obj.error_msg = error_msg
            obj.created_by =''
            obj.user_id = ''
            obj.hotel_id =''
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
                self.errortextlog(str("mmm"))  
            except Exception as e :
                print("Rabbit connection Failed")
                print(e)
                self.errortextlog(str(e))
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
        def errortextlog(self,msg):
            messagebox.showinfo("errortextlog",msg)
            fruits=["Orange\n","Banana\n","Apple\n"]
            new_file=open("errorlog.txt",mode="a+",encoding="utf-8")
            new_file.writelines(msg)
            new_file.close()
# a =Smpt('smtp.gmail.com', 587)
# z= a.connectsmtp()
# a.sendMail(z)
