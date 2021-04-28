from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import os
import networkx as nx


class Crawler():

    def __init__(self, start, jump_cap,  graph=None, driver_path="./drivers/chromedriver",):
        self.start = start
        self.jump_cap = jump_cap
        if graph:
            self.network = graph
        else:
            self.network = nx.Graph()
        self.visited = []
        self.todo = []
        self.setup(driver_path)

    """
    instanciate a driver object 
    """

    def setup(self, driver_path=None):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        if driver_path is None:
            chrome_options.binary_location = os.environ.get(
                "GOOGLE_CHROME_BIN")
            driver_path = os.environ.get("CHROMEDRIVER_PATH")
        self.driver = webdriver.Chrome(
            executable_path=driver_path, options=chrome_options)

    """
    end program by closing chromedriver 
    """

    def end(self):
        self.driver.quit()

    def to_graphml(self, filename):
        nx.write_graphml(self.network, filename)

    def scroll_down(self):
        pass


class Twitter_BFS(Crawler):
    def __init__(self, start, jump_cap, graph=None, driver_path='./drivers/chromedriver'):
        super().__init__(start, jump_cap, graph=graph, driver_path=driver_path)
        start_url = f'https://twitter.com/hashtag/{start[1:]}?src=hashtag_click'
        self.current_tag = start
        self.todo.append((self.current_tag, start_url))

    """ 
    scrape current pages hastag urls 
    returns a tuple (tagname, url)
    """

    def get_tags(self):
        try:
            hashtags = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_all_elements_located(
                    (By.XPATH,
                     "//a[@class='css-4rbku5 css-18t94o4 css-901oao css-16my406 r-1n1174f r-1loqt21 r-poiln3 r-bcqeeo r-qvutc0' and contains(@href, 'hashtag_click')]")
                ))
        except TimeoutException:
            print("found no tweets")
            return []
        return [(h.text, h.get_attribute("href")) for h in hashtags]

    """
    takes a list of tuples and adds to current networkX graph adds relevant links to todo
    """

    def append_nodes(self, tag_url):
        for tu in tag_url:
            self.network.add_edge(self.current_tag.upper(), tu[0].upper())
            if tu[1] not in set(self.visited):
                self.todo.append(tu)
    """
    crawls in a bfs pattern until jump cap and expands the networkx graph with hashtag nodes. 
    """

    def crawl(self):
        jumps = 0
        while self.jump_cap >= jumps and len(self.todo) > 0:
            current = self.todo.pop(0)
            self.current_tag = current[0]
            self.visited.append(current[1])
            print(f"{jumps} visting {current[0]}")
            self.driver.get(current[1])
            print(current)
            tags = self.get_tags()
            self.append_nodes(tags)
            jumps += 1
        self.end()
