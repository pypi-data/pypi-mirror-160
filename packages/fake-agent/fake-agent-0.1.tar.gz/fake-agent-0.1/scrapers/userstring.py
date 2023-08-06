from json import dump
from requests import get
from bs4 import BeautifulSoup


def write_to(name: str, content: list):
    to_wrtie = {num: agent for num, agent in enumerate(content)}
    with open(name, 'w') as f:
        dump(to_wrtie, f, indent=4)


name = "Edge"

resp = get(f"http://useragentstring.com/pages/useragentstring.php?name={name}")
soup = BeautifulSoup(resp.text, "html.parser")
agents = []

for ul in soup.find_all("div", attrs={"id": "liste"}):
    for li in ul.find_all("ul"):
        for item in li.find_all("li"):
            agents.append(item.text)

write_to(f"FakeAgent/data/{name}.json", agents)
