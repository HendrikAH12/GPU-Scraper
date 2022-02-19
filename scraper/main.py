import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import json

urls = [
    "https://m.kabum.com.br/busca?string=rtx+3050",
    "https://m.kabum.com.br/busca?string=rx+6600",
    "https://m.kabum.com.br/busca?string=rtx+2060",
]

ua = UserAgent()
opts = Options()
opts.add_argument("user-agent="+ua.random)
driver = webdriver.Chrome(options=opts)
gpus = []

for url in urls:
    driver.get(url)

    html = driver.page_source
    soup = bs4.BeautifulSoup(html, "html.parser")
    items = soup.find_all("a", {"class": "ctn-produto"})

    for product in items:
        gpus.append({
            "name": product.find("div", {"class": "pnome"}).text[15:75],
            "price": product.find("span", {"class": "pvalor"}).findChildren("strong", recursive=True)[0].text
        })
        break

print(json.dumps(gpus, indent=4, sort_keys=True))
