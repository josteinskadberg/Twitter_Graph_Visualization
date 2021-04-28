from flask import Flask, flash, render_template, url_for, request, redirect
from source.graph_renderer import render_graph
from source.Jumper import Twitter_BFS
import networkx as nx
import re

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
G = render_graph()[2]


def clean(tag, jumps, expand=None):
    tag.strip()
    if not tag.startswith('#'):
        tag = "#"+tag
    if re.fullmatch("#[A-Za-zæøåÆøå1-9_-]+", tag) is None:
        return None
    return tag, int(jumps), bool(expand)


def scrape(tag, jumps, graph=None):
    scraper = Twitter_BFS(tag, int(jumps), graph=graph)
    scraper.crawl()
    if nx.is_empty(scraper.network):
        print("found no edges for", tag)
        return render_graph()
    return render_graph(scraper.network)


@app.route('/', methods=['POST', "GET"])
def index():
    global G
    if request.method == "POST":
        params = clean(*request.form.getlist('scrape_param'))
        if not params:
            flash(
                "The search tag cannot contain spaces or special characters other than '-' and '_'", "error")
            return redirect("/")
        if params[2]:
            script, div, G = scrape(params[0], params[1], G)
        else:
            script, div, G = scrape(params[0], params[1])
        return render_template("index.html", plot_script=script, plot_div=div)
    else:
        script, div, _ = render_graph()
        return render_template("index.html", plot_script=script, plot_div=div)


if __name__ == "__main__":
    app.run(debug=True)
