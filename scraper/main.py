import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import bs4, time

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
        item = soup.find("a", {"class": "ctn-produto"})

        gpus.append({
            "name": item.find("div", {"class": "pnome"}).text[15:70],
            "price": item.find("span", {"class": "pvalor"}).findChildren("strong", recursive=True)[0].text[4:]
        })

    if webdriver:
        append_gpu(webdriver)
    else:
        webdriver = create_driver()
        append_gpu(webdriver)
        webdriver.quit()

    return gpus

links = [
    "https://m.kabum.com.br/busca?string=rtx+3050",
    "https://m.kabum.com.br/busca?string=rx+6600",
    "https://m.kabum.com.br/busca?string=rtx+2060",
]

def scraper():
    time_start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_gpu, link) for link in links]
        return_value = [f.result()[0] for f in futures]

        return return_value, "{:.2f}".format(time.time() - time_start)

print(scraper())
