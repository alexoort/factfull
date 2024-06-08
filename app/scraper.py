import requests
from bs4 import BeautifulSoup

def scrape_ochaopt():
    url = 'https://www.ochaopt.org/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the values inside of span elements with class h2
    data = {
        'Palestinians': {},
        'Israelis': {},
        'Damages' : {}
    }

    # Function to extract reported killed number
    def extract_reported_killed(section):
        try:
            killed_section = section.find('h4', text='Reported killed')
            if killed_section:
                number_element = killed_section.find_previous_sibling('div').find('span', class_='h2')
                if number_element:
                    return number_element.get_text(strip=True)
        except AttributeError:
            return None
        return None

    # Function to extract reported injured number
    def extract_reported_injured(section):
        try:
            injured_section = section.find('h4', text='Reported injured')
            print(injured_section)
            if injured_section:
                parent_div = injured_section.find_parent('div', class_='mt-4')
                if parent_div:
                    number_element = parent_div.find('span', class_='h2')
                    if number_element:
                        return number_element.get_text(strip=True)
        except AttributeError:

            return None
        return None

    # Find and process Palestinian section
    palestinians_section = soup.find('h2', text='PALESTINIANS').find_parent('div').find_parent('div')
    if palestinians_section:
        data['Palestinians']['Reported killed'] = extract_reported_killed(palestinians_section)
        data['Palestinians']['Reported injured'] = extract_reported_injured(palestinians_section)

    # Find and process Israeli section
    israelis_section = soup.find('h2', text='ISRAELIS').find_parent('div').find_parent('div')
    print(israelis_section)
    if israelis_section:
        data['Israelis']['Reported killed'] = extract_reported_killed(israelis_section)
        data['Israelis']['Reported injured'] = extract_reported_injured(israelis_section)

    # Function to extract damage stats
    def extract_damage_stats(section):
        try:
            damage_section = section.find('h2', text='DAMAGE AND IDPS').find_parent('div').find_parent('div')
            if damage_section:
                housing_units_destroyed = damage_section.find('h4', text='Housing units destroyed in Gaza')
                displaced_in_gaza = damage_section.find('h4', text='Displaced in Gaza')
                if housing_units_destroyed:
                    housing_units_number = housing_units_destroyed.find_previous_sibling('div').find('span', class_='h2')
                    data['Damages']['Housing units destroyed in Gaza'] = housing_units_number.get_text(strip=True) if housing_units_number else None
                if displaced_in_gaza:
                    displaced_number = displaced_in_gaza.find_previous_sibling('div').find('span', class_='h2')
                    data['Damages']['Displaced in Gaza'] = displaced_number.get_text(strip=True) if displaced_number else None
        except AttributeError:
            return None
    
    extract_damage_stats(soup)

    def data_cleanup(data):
        for key, value in data.items():
            for k, v in value.items():
                if v:
                    # Allow digits, periods, and commas
                    data[key][k] = ''.join(char for char in v if char.isdigit() or char in '.,')
        return data

    data = data_cleanup(data)
    print(data)
        

    return data



