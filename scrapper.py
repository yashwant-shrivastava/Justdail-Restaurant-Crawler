from bs4 import BeautifulSoup
import urllib.request
import csv
import os

from restaurant import Restaurant
from settings import Constants
import requests

def which_digit(html):
    class_to_digit_mapping = {
        'icon-ji': 9,
        'icon-dc': '+',
        'icon-fe': '(',
        'icon-hg': ')',
        'icon-ba': '-',
        'icon-lk': 8,
        'icon-nm': 7,
        'icon-po': 6,
        'icon-rq': 5,
        'icon-ts': 4,
        'icon-vu': 3,
        'icon-wx': 2,
        'icon-yz': 1,
        'icon-acb': 0,
    }
    return class_to_digit_mapping.get(html, '')

class Scrapper(object):
    def __init__(self, file_path):
        self.base_url = None
        self.body = None
        self.file_path = file_path
        self.parsed_res = set()

    def _get_name(self):
        return self.body.find('span', {'class': 'jcn'}).a.string

    def _get_phone_number(self):
        i = 0
        phone_no = "No Number!"
        try:

            for item in self.body.find('p', {'class': 'contact-info'}):
                i += 1
                if (i == 2):
                    phone_no = ''
                    try:
                        for element in item.find_all(class_=True):
                            classes = []
                            classes.extend(element["class"])
                            phone_no += str((which_digit(classes[1])))
                    except:
                        pass
        except:
            pass
        body = self.body['data-href']
        soup = BeautifulSoup(body, 'html.parser')
        for a in soup.find_all('a', {"id": "whatsapptriggeer"}):
            phone_no = str(a['href'][-10:])

        return phone_no

    def _get_address(self):
        return self.body.find('span', {'class': 'mrehover'}).text.strip()

    def start_scrapping(self, url):
        self.base_url = url
        page_number = 1
        service_count = 1

        fields = ['Name', 'Phone', 'Address']
        if not os.path.exists(self.file_path):
            out_file = open(self.file_path, 'w')
        else:
            out_file = open(self.file_path, 'a')

        csv_writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)
        flag = True

        while flag:
            if page_number == 1:
                # baseurl = "https://www.justdial.com/Delhi/Indian-Restaurants/"
                try:
                    html = requests.get(
                        self.base_url,
                        headers={
                            'USER-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64)",
                            'Host': 'www.justdial.com',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Connection': 'keep-alive'
                        }
                    )
                    url = html.url
                except:
                    page_number += 1
                    flag = False
                    continue

            try:
                new_url = url + "/page-{}".format(page_number)
                html = requests.get(
                        new_url,
                        headers={
                            'USER-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64)",
                            'Host': 'www.justdial.com',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Connection': 'keep-alive'
                        }
                    )

                soup = BeautifulSoup(html.text, "html.parser")
                services = soup.find_all('li', {'class': 'cntanr'})

                if not services or len(services) == 0:
                    flag = False
                    continue

                for service_html in services:
                    self.body = service_html
                    dict_service = {}
                    name = self._get_name()
                    phone = self._get_phone_number()
                    address = self._get_address()
                    if name != None:
                        dict_service['Name'] = name
                    if phone != None:
                        dict_service['Phone'] = phone
                    if address != None:
                        dict_service['Address'] = address

                    print(dict_service)
                    if len(dict_service.keys()) == 0:
                        flag = False
                        continue

                    restaurant = Restaurant(name, address, phone)
                    if restaurant not in self.parsed_res:
                        self.parsed_res.add(restaurant)
                        csv_writer.writerow(dict_service)
                        print("#" + str(service_count) + " ", dict_service)
                        service_count += 1
                    else:
                        continue
                page_number += 1
            except Exception as e:
                print("Exception caught {}".format(e))
                flag = False

        out_file.close()
