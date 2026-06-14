import urllib.request
from bs4 import BeautifulSoup

def get_with_www_timeanddate_com(year: int):
    table = {}

    for month in range(1, 13):
        contents = urllib.request.urlopen(f"https://www.timeanddate.com/sun/russia/yekaterinburg?month={month}&year={year}").read()
        soup = BeautifulSoup(contents)

        days = {}
        
        for line in soup.select('tr[data-day]'):
            day = int(line.attrs['data-day'])
            sunrise = line.select_one('td:nth-of-type(1)').contents[0].text.rstrip()
            sunset = line.select_one('td:nth-of-type(2)').contents[0].text.rstrip()
            
            days[day] = { 'sunrise': sunrise, 'sunset': sunset }

        table[month] = days

    return table