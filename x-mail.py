#!/usr/bin/env python
import pika
import sys
import json
from tkinter import messagebox
import sendMail
import argparse
import xml.etree.ElementTree as ET

# sendMail = sendMail.Smpt('smtp.gmail.com', 587)
# smtpconf = sendMail.connectsmtp()
# a =Smpt('smtp.gmail.com', 587)
# z= a.connectsmtp()
with open('config.json') as conf_data:
        conf =  json.load(conf_data)
        mq_url             = conf['mq_url']
        mq_port            = conf['mq_port']
        mq_user            = conf['mq_user']
        mq_pass            = conf['mq_pass']

def callback(ch, method, properties, body):
    data = json.loads(body)
    Mail = sendMail.Smpt(data['server_host'], data['server_port'],data['hotel_id'],data['user_id'])
    smtpconf = Mail.connectsmtp(data['server_host'], data['server_port'],'', data['password'])
    qr_code = data['qr_code']
    if qr_code:
            # messagebox.showinfo("enter QR Code", data['subject'])
            Mail.qrcode(smtpconf,data['qr_code'],data['mail_from'],data['receipents'],data['subject'])
            print("QR Code ")
            
    else:
        Mail.plainmail(smtpconf,data['html_body'],data['mail_from'],data['receipents'],data['subject'])
        print("Normal Mail")

    

def main(args):
   # construct the argument parse and parse the arguments
    credits = pika.PlainCredentials(mq_user,mq_pass)
    params = pika.ConnectionParameters(mq_url,mq_port,'/',credits)
    connection = pika.BlockingConnection(parameters=params)
    channel = connection.channel()
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--set", required=False,
        help="name of the user")
    args = vars(ap.parse_args())
    command = args['set']
    # command = int(command)
#     print(command)
    if command =='1':
             print("1 for change SMTP Setting \n2 for change Rabbit MQ Setting")
             subcommand = input("Select Your Action ")
            #  Message=input("Enter Your Message")
             if int(subcommand) ==1:
                setSmtp()
             elif int(subcommand) ==2:
                setRabbitMQ()
             else:
                print("Please enter Proper code")
                print("1 for change SMTP Setting \n2 for change Rabbit MQ Setting")
           
    else:
        channel.basic_consume(callback,
                      queue='in_email_queue',
                      no_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()   

def setSmtp():
    tree = ET.parse('config.xml')  
    root = tree.getroot()

    #Changeing SMTP IP Adress
    smtp_host = input("Enter SMTP IP Adress- ")
    for rank in root.iter('smtp_host'):
        new_smtp_host = smtp_host
        rank.text = new_smtp_host
    #Changeing SMTP User Name
    smtpuser = input("Enter SMTP User Name- ")
    for rank in root.iter('smtpuser'):
        new_smtpuser = smtpuser
        rank.text = new_smtpuser
    #Changeing SMTP Password     
    smtppassword = input("Enter SMTP Password- ")
    for rank in root.iter('smtppassword'):
        new_smtppassword = smtppassword
        rank.text = new_smtppassword
    #Changeing SMTP Port    
    smtp_port = input("Enter SMTP Port- ")    
    for rank in root.iter('smtp_port'):
        new_smtp_port = smtp_port
        rank.text = new_smtp_port
         
    tree.write('config.xml') 

def setRabbitMQ():
    tree = ET.parse('config.xml')  
    root = tree.getroot()

    #Changeing Rabbit MQ host 
    mq_host = input("Enter SMTP IP Adress- ")
    for rank in root.iter('mq_host'):
        new_mq_host = mq_host
        rank.text = new_mq_host
    #Changeing Rabbit MQ User 
    mq_user = input("Enter Rabbit MQ User- ")
    for rank in root.iter('mq_user'):
        new_mq_user = mq_user
        rank.text = new_mq_user
    #Changeing Rabbit MQ User 
    mq_pass = input("Enter Rabbit MQ Password- ")
    for rank in root.iter('mq_pass'):
        new_mq_pass = mq_pass
        rank.text = new_mq_pass
   #Changeing Rabbit MQ User 
    mq_port = inputNumber("Enter Rabbit MQ Port- ")
    
    for rank in root.iter('mq_pass'):
        new_mq_port = mq_port
        rank.text = new_mq_port
    #Testing Connection
    conteststatus=rabbitconnectiontest(new_mq_host,new_mq_user,new_mq_pass,new_mq_port) 
    if conteststatus ==False:
        diacesen = input("You want to save or not(y/n) :")
        if diacesen=='y':
            tree.write('config.xml') 
           
    

def rabbitconnectiontest(new_mq_host,new_mq_user,new_mq_pass,new_mq_port):
    status = False
    print('connecting to Rabbit MQ Serve ....\n')
    credits = pika.PlainCredentials(new_mq_user,new_mq_pass)
    params = pika.ConnectionParameters(new_mq_host,new_mq_port,'/',credits)
    try:
     connection = pika.BlockingConnection(parameters=params)
     if connection.is_open:
        print('Rabbit MQ Serve connection .........................successfully')
        status = True
     else :
            status = False
     connection.close()
     exit(0)
    except Exception:
        pass  # or you could use 'continue'
        print('Rabbit MQ Serve connection .........................Failed')
        status = False
    return status
def inputNumber(message):
  while True:
    try:
       userInput = int(input(message))       
    except ValueError:
       print("Not an integer! Try again.")
       continue
    else:
       return userInput 
       break 

if __name__ == '__main__':
      main(sys.argv[1:])
    # print(rabbitconnectiontest())