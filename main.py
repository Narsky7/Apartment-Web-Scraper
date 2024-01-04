from bs4 import BeautifulSoup
import requests
import time

def checkPrice():
    r = requests.get('https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/?search%5Bfilter_enum_rooms%5D%5B0%5D=one&search%5Bfilter_enum_rooms%5D%5B1%5D=two', auth=('user', 'pass'))

    html = r.text

    soup = BeautifulSoup(html, 'lxml') 
    headers = soup.find_all(class_="css-qfzx1y")
    metraz = soup.find_all(class_="css-643j0o")
    data_miejsce = soup.find_all(class_="css-veheph")

    suma = 0

    for i, header in enumerate(headers) :
        nazwa = header.h6.text
   
        cena = header.p.text

        #We want to delete unnecessery line of text if there is 'negotiable' after the price

        if len(cena) >= 12:
            cena = cena[0:-15]  
        else: 
            cena = cena[0:-2]  

        cena = cena.replace(" ","")
        cena_liczbowa = int(cena)

        suma += cena_liczbowa

        print(f"{i}. Metraż: {metraz[i].text} Cena: {cena_liczbowa} złotych Miejsce i Data: {data_miejsce[i].text}")

    #display the arithmetic average of all the prices

    srednia_arytmetyczna = round(suma / (len(headers)),2)
    print(f"Srednio cena mieszkania wynosi {srednia_arytmetyczna} złotych")

    file = open('average.txt', 'at')
    file.write("\n" + "=>" + str(srednia_arytmetyczna))
    file.close()


if __name__ == '__main__':
    while True:
        checkPrice()
        time.sleep(600)
    