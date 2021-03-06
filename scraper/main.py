import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import bs4, time, json

def create_driver():
    ua = UserAgent()
    opts = Options()
    opts.add_argument("user-agent="+ua.random)
    opts.add_argument("--headless")
    return webdriver.Chrome(options=opts)

def get_gpu(url, webdriver=None):
    gpus = []

    def append_gpu(driver):
        driver.get(url)
        time.sleep(5)
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, "html.parser")
        items = soup.find_all("a", {"class": "ctn-produto"})

        for product in items:
            gpus.append({
                "name": product.find("div", {"class": "pnome"}).text[15:70],
                "price": int(product.find("span", {"class": "pvalor"}).findChildren("strong", recursive=True)[0].text[4:9].replace(".", "")),
                "change": 0
            })

    if webdriver:
        append_gpu(webdriver)
    else:
        webdriver = create_driver()
        append_gpu(webdriver)
        webdriver.quit()

    return gpus

links = [
    "https://m.kabum.com.br/busca?string=rx+6600",
    "https://m.kabum.com.br/busca?string=rtx+3050",
    "https://m.kabum.com.br/busca?string=rtx+2060"
]

def scraper():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_gpu, link) for link in links]
        returned_values = [f.result()[0] for f in futures]

    try:
        f = open("data.txt")
        data = json.load(f)
        c = 0
        for i in data["gpus"]:
            returned_values[c]["change"] = returned_values[c]["change"] - (i["price"] - int(returned_values[c]["price"]))
            c = c + 1
    except:
        pass

    with open("data.txt", "w") as outfile:
        outfile.write(json.dumps({"gpus": returned_values}, indent=4))

if __name__ == "__main__":
    scraper()
