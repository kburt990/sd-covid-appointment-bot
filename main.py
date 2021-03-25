from bs4 import BeautifulSoup
from playsound import playsound
import requests
import re
import time
import datetime


def get_appointments() -> dict:
    """Returns a dict of open appointment dates where keys are location and entries are dates"""

    url = 'https://www.sandiegocounty.gov/content/sdc/hhsa/programs/phs/community_epidemiology/dc/2019-nCoV/vaccines/vax-schedule-appointment.html'
    page = requests.get(url)
    parsed_site = BeautifulSoup(page.content, 'html.parser')  # parse site
    header_re = re.compile(r'^Appointments for(.*)')  # regular expression for locations

    tables = parsed_site.findChildren('tbody')
    headers = []
    for header in parsed_site.findChildren('b'):
        if header_re.match(header.text.strip()):
            headers.append(header.text)
    for header in parsed_site.findChildren('a'): # get all headers, for some reason they are under 2 different html tags
        if header_re.match(header.text.strip()):
            headers.append(header.text)

    open_apps = {}  # dict for appointments

    for header, table in zip(headers, tables[1:]):

        for row in table.findChildren('tr')[1:]:
            if not row.find_all('i'):
                date = row.find_all('td')[0].text  # get date
                if header in open_apps.keys():
                    open_apps[header].append(date)
                else:
                    open_apps[header] = [date]

    return open_apps


def print_appointments(appointments:dict) -> None:
    """Prints formatted appointments"""
    if not appointments:
        print("No appointments currently available.")
    else:
        for key in appointments.keys():
            print(key)
            for appointment in appointments[key]:
                print(f"   * {appointment}")


def print_time() -> None:
    """Prints formatted date"""
    current_time = datetime.datetime.now()
    current_date = datetime.datetime.today()
    time_str = current_time.strftime("%H:%M:%S")
    day_str = current_date.strftime("%B %d, %Y")
    print(f"Appointments as of {day_str} at {time_str}")


def run() -> None:
    """Main loop"""

    appointments = None

    while True:
        current_apps = get_appointments()

        if current_apps != appointments:
            playsound('alert.mp3')
            appointments = current_apps
            print_time()
            print_appointments(appointments)

        time.sleep(30)







if __name__ == "__main__":
    run()




