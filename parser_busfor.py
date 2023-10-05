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
    print(driver.current_url)
    soup = BeautifulSoup(html, "lxml")
    tickets = soup.find_all('div', class_='ticket')
    result = []
    for item in tickets:
        ticket = Ticket()
        
        ticket.dep_time = item.find('div', class_='Style__Time-sc-1n9rkhj-0 bmnWRj').text
        ticket.dep_place = item.find('div', class_='Style__Title-yh63zd-5 cspGxb').text + ', ' + item.find('div', class_='Style__Description-yh63zd-6 eKkHly').text
        ticket.arr_time = item.find_all('div', class_='Style__Time-sc-1n9rkhj-0 bmnWRj')[1].text
        ticket.arr_place = item.find_all('div', class_='Style__Title-yh63zd-5 cspGxb')[1].text + ', ' + item.find_all('div', class_='Style__Description-yh63zd-6 eKkHly')[1].text
        ticket.cost = item.find('span', class_='price text-nowrap').text + item.find('span', class_='price__fraction').text
        ticket.free_space = item.find('span', class_='TripFreeSeats__Seats-cj6o3m-0 dEMWiJ').text
        result.append(ticket)
    return(result)

        
        
        
        
    
    
    
#for test
user = User()
user.date = '09.10.2023'
user.first_town = 'Гродно'
user.sec_town = 'Минск'
user.date_split()
print(parser_busfor_result(user))
