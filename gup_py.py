from flask import Flask, redirect

app = Flask(__name__)

@app.route("/<id>")
def index(id):
    return_content = ""
    if id == "":
        # fix this, for some reason its not working 
        return_content = "<center><h1>Hello from Gup.pu URL Shortner</h1></center>"
    else:
        # eventually pull out a url from a database, that consumers clan go and link their urls to, also be able to track metrics
        return_content = redirect("http://www.google.com", code=303)
    return return_content
    

if __name__ == '__main__':
    app.run()