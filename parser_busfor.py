import selenium
from bs4 import BeautifulSoup
import requests
import parser_atlas
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from base import User, Ticket

def parser_busfor_result(user:User):
    url = f'https://busfor.by/автобусы/{user.first_town}/{user.sec_town}?on={user.year}-{user.mounth}-{user.day}'
    driver = webdriver.Chrome()
    driver.get(url)
    submit_button = driver.find_element(By.ID, 'submit')
    submit_button.click()
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    tickets = soup.find_all('div', class_='ticket')
    result = ''
    for item in tickets:
        #ticket = Ticket()
        #eticket_info = item.find('div').find_all('div')[1].find_all('div')[0].find_all("div")
        #eticket_time_spot = eticket_info[0].find("div").find_all("div")
        #ticket.dep_time = eticket_time_spot[0].find("div").find("div").text
        #test =eticket_time_spot[0].find_all('div')[1]
        #ticket.dep_place = ''
        #result.append(ticket)
        return(tickets)
        
        
        
        
        
    
    
    
#for test
user = User()
user.date = '04.10.2023'
user.first_town = 'Гродно'
user.sec_town = 'Минск'
user.date_split()
print(parser_busfor_result(user))
