from flask import Flask, request, render_template, redirect
import json
import os

app = Flask(__name__)
TOOLS_FILE = "tools.json"

def load_tools():
    if not os.path.exists(TOOLS_FILE):
        return []
    with open(TOOLS_FILE, "r") as f:
        return json.load(f)

def save_tools(tools):
    with open(TOOLS_FILE, "w") as f:
        json.dump(tools, f, indent=2)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        tools = load_tools()
        tools.append({
            "name": request.form["name"],
            "url": request.form["url"],
            "webhook": request.form["webhook"],
            "parser": request.form["parser"]
        })
        save_tools(tools)
        return redirect("/")
    return render_template("index.html", tools=load_tools())

@app.route("/run-summary", methods=["POST"])
def run_summary():
    from your_module import extract_and_summarize_all_tools
    extract_and_summarize_all_tools()  # Implement this function to run for all tools
    
    return redirect("/")
