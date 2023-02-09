import requests
from bs4 import BeautifulSoup
from pathlib import Path
import pickle
import time
import requests_cache

requests_cache.install_cache('cache/aws_document_cache')
start = time.time()

base_url = "https://docs.aws.amazon.com/ja_jp/IAM/latest/UserGuide/"
target_url = base_url + "reference_policies_actions-resources-contextkeys.html"

def to_soup(url):
    return BeautifulSoup(requests.get(url).content, 'html.parser')


def gen_data():
    soup = to_soup(target_url)
    html = ""
    links = []
    for li in soup.find_all('li'):
        a_tag = li.find("a")
        if a_tag is None:
            continue
        href = a_tag.get("href")
        if not href.startswith("./list_"):
            continue
        links.append(href)
    # print(links)
    contents = {}
    for link in links:
        print(link)
        service_name = link.replace("./list_", "").replace(".html", "")
        if service_name not in contents.keys():
            contents[service_name] = []
        url = base_url + link.replace("./", "")
        html += f"<h1><a href='{url}'>{service_name}</a></h1>"
        soup = to_soup(url)
        tables = soup.find_all("table")
        if len(tables) == 0:
            print("len tables is 0")
            continue
        
        table = tables[0]
        html += str(table)
        for tr in table.find_all("tr"):
            td = tr.find("td")
            if td is None:
                continue
            txt = td.text
            if len(txt) == 0:
                continue
            contents[service_name].append(txt.strip())

    return contents, html


# pkl_path = Path("cache/data.pkl")
# if pkl_path.exists():
#     with open(pkl_path, "rb") as f:
#         data = pickle.load(f)
# else:
#     data = gen_data()
#     with open(pkl_path, "wb") as f:
#         pickle.dump(data, f)

print("こんにちは")
data, html = gen_data()
with open("all_services.html", "w") as f:
    f.write(html)
print("time: ", time.time() - start)

# print(data)