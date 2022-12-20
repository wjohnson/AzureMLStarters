from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Home</h1>"

@app.route('/am/alive')
def liveness():
    return {"alive":True}

@app.route('/am/ready')
def readiness():
    return {"ready":True}

@app.route('/score',methods=["GET", "POST"] )
def score():
    return [
        1,1,1,1,0,1,1,0,0
    ]

if __name__ == "__main__":
    app.run(debug=False)