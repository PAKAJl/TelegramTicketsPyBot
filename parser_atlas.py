from bs4 import BeautifulSoup
import requests
import base 


def get_html(url):
    r = requests.get(url)
    return r.text

def get_parser_atlas_result (user):
    try:
        url = f'https://atlasbus.by/Маршруты/{user.first_town}/{user.sec_town}?date={user.year}-{user.mounth}-{user.day}'
        html = get_html(url)
        print(url)
        soup = BeautifulSoup(html, "lxml")
        grid = soup.find('div', class_="MuiGrid-root MuiGrid-item MuiGrid-grid-md-8 MuiGrid-grid-lg-9")
        ticket_list = []
        all_routes = grid.find_all('div', class_='jss19')
        for item in all_routes:
            if item.find('h6') is None:
                continue
            else:
                ticket = Ticket()
                containers = item.find_all('div', class_='MuiGrid-root MuiGrid-item MuiGrid-grid-md-3')
                first_block = containers[0].find('div').find_all('div')
                ticket.dep_time = first_block[1].text + ' ' + first_block[2].text
                ticket.dep_place = first_block[3].text + ' ' + first_block[4].text
                sec_block = containers[1].find('div').find_all('div')
                ticket.arr_time = sec_block[1].text
                ticket.arr_place = sec_block[2].text + ' ' + sec_block[3].text
                ticket.cost = item.find('h6').text
                ticket.free_space = item.find('div', class_='MuiGrid-root MuiGrid-item MuiGrid-grid-md-auto').find('div').find_all('p')[1].text
                ticket_list.append(ticket) 
    
        return ticket_list
    except:
        return "Error"
