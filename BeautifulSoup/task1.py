# import requests
# from bs4 import BeautifulSoup

# with open("validProxies.txt", "r") as f:
#     proxies = f.read().split("\n")
# counter = 8
# print(proxies[counter])
# try:
#     url = 'https://www.yelu.in/category/restaurants/city:mumbai'
#     res = requests.get(url, proxies={"http": proxies[counter], "https": proxies[counter]}, timeout=30)
#     soup = BeautifulSoup(res.text, 'html.parser')

    
#     print(soup.prettify())
# except Exception as m:
#     print("Failed", m)
# finally:
#     counter += 1
#     print(counter)
#     print(proxies[counter])


# single Linklist program