
import pandas as pd
import requests
from lxml import html
from datetime import datetime, date
import calendar
from dateutil.relativedelta import relativedelta
import logging

import os
import smtplib
from email.message import EmailMessage
from email.headerregistry import Address
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import *


def get_bookable_date(session,url):
    df = pd.DataFrame()
    pageContent=session.get(url)
    tree = html.fromstring(pageContent.content)
    months_html =tree.xpath('//div[@class="calendar-month-table span6"]')
    for m in months_html :
       
        month = m.xpath('.//th[@class="month"]')
        #print(month[0].text)
        dates_month_html = m.xpath('.//table//td[@class="buchbar"]/a')
        dates =[d.text for d in dates_month_html]
        df_month = pd.DataFrame({'month':month[0].text,'dates':dates})
        df = pd.concat([df,df_month],axis=0)
    return(df)

def get_next_two_months():
    
    today =date.today()
    last_month_day = calendar.monthrange(today.year,today.month)[1]
    next_month_date = today+relativedelta(months=+1)
    next_next_month_date = today+relativedelta(months=+2)
    timestamp_next_month  = calendar.timegm(next_month_date.replace(day=1).timetuple())
    timestamp_next_next_month  = calendar.timegm(next_next_month_date.replace(day=1).timetuple())
    return(timestamp_next_month,timestamp_next_next_month)

def get_all_termin_availables():
    
    with requests.Session() as s:
        df_current_and_next_month = get_bookable_date(s,URL)
        next_timestamps = get_next_two_months()
        df_months_plus_1_and_2 = get_bookable_date(s,f'{URL_BASE}{next_timestamps[0]}')
        df_months_plus_2_and_3 = get_bookable_date(s,f'{URL_BASE}{next_timestamps[1]}')
        df_all = pd.concat([df_current_and_next_month,df_months_plus_1_and_2,df_months_plus_2_and_3],axis=0)
        df_all.drop_duplicates(inplace=True)
        
    
    return df_all


def send_notification(df):

    # Compose message
    msg = MIMEMultipart()
    msg["Subject"] = "Burgeramt : {} new Termin".format(df.shape[0])
    msg["From"] = SENDER_EMAIL
    msg["To"] = ",".join(TARGET_EMAILS)
    
    HTMLBody1 = '''<h3>{0}</h3>
    <h3>{1}</h3>
                   '''.format(TITLE,LOCATION)
    part1 = MIMEText(HTMLBody1, 'html')   
    msg.attach(part1)

    HTMLBody2 = '''<h3>Termin availables :</h3>
                   {}'''.format(df.to_html())
    part2 = MIMEText(HTMLBody2, 'html')
    msg.attach(part2)

    HTMLBody3 = '''<a href={}>click here to book</a>'''.format(URL)
    part3 = MIMEText(HTMLBody3, 'html')
   
    msg.attach(part3)

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(SENDER_EMAIL, SENDER_PWD)
        server.sendmail(SENDER_EMAIL, TARGET_EMAILS, msg.as_string())
        server.close()
        logging.debug("Email sent!")
    except Exception as e:

        logging.error("Something went wrong...")
        logging.error(e)
        

def check_termin_and_send_email():
    try:
        df_termin = get_all_termin_availables()
        if df_termin.shape[0]>0:
            send_notification(df_termin)
    except Exception as e:
        logging.error(e)

