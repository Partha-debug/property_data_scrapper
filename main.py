import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import pandas
import os


city = input("Please enter the name of the city: ")
r = requests.get(
    f"https://www.makaan.com/balasore-residential-property/buy-property-in-{city.lower()}-city")


if r.status_code == 200:

    soup = BeautifulSoup(r.content, "html.parser")
    property_data = defaultdict(list)

    if soup.find_all('div', {"class": "pagination"}):
        num_pages = int(soup.find_all('div', {"class": "pagination"})[
                        0].find_all('a')[-2].text)

        print(f"scrapping data from {num_pages} pages... may take several mins...")
        
        for page_no in range(2, num_pages+1):
            try:
                r = requests.get(
                    f"https://www.makaan.com/balasore-residential-property/buy-property-in-{city.lower()}-city?page={page_no}")
            except KeyboardInterrupt:
                print("Quitting...")
                break
            except:
                print("Connection terminated...")
                break

            os.system("cls")
            print(f"Scrapping page no {page_no} from {num_pages} pages...")
            
            soup = BeautifulSoup(r.content, "html.parser")

            scrapped_property_data = soup.find_all(
                'div', {"class": "infoWrap"})

            for properties in scrapped_property_data:
                property_data["Property Type"].append(
                    properties.find('a', {'class': 'typelink'}).text.strip())
                if isinstance(properties.find('span', {'class': 'projName'}), type(None)):
                    property_data["Address"].append(properties.find(
                        'a', {'class': 'loclink'}).text.strip())
                else:
                    property_data["Address"].append(properties.find('span', {'class': 'projName'}).text.strip(
                    ) + ', ' + properties.find('a', {'class': 'loclink'}).text.strip())
                property_data['Price'].append(
                    "Rs "+properties.find('div', {"data-type": "price-link"}).text.strip())
                property_data["Area"].append(properties.find(
                    'td', {"class": "lbl rate"}).text.strip())

    else:

        print('scraping data from 1 page... ')
        scrapped_property_data = soup.find_all('div', {"class": "infoWrap"})

        for properties in scrapped_property_data:
            property_data["Property Type"].append(
                properties.find('a', {'class': 'typelink'}).text.strip())
            if isinstance(properties.find('span', {'class': 'projName'}), type(None)):
                property_data["Address"].append(properties.find(
                    'a', {'class': 'loclink'}).text.strip())
            else:
                property_data["Address"].append(properties.find('span', {'class': 'projName'}).text.strip(
                ) + ', ' + properties.find('a', {'class': 'loclink'}).text.strip())
            property_data['Price'].append(
                "Rs "+properties.find('div', {"data-type": "price-link"}).text.strip())
            property_data["Area"].append(properties.find(
                'td', {"class": "lbl rate"}).text.strip())

    df = pandas.DataFrame(property_data)
    print(f'Writing data to /Properties_in_{city}.csv...')
    df.to_csv(f"Properties_in_{city}.csv", index=False)
    print("Done...")

else:
    print(f"No properties can't be found in {city}")
