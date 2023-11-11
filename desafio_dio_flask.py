import pandas as pd
from flask import Flask, render_template, Response

app = Flask(__name__)


df = pd.DataFrame({
    "Number": [1, 2, 3, 4, 5],
    "Name": ["Douglas", "Thais", "Brian", "Anya", "Mimi"],
    "Age": [33, 26, 12, 2, 7],
    "City": ["Paraibuna", "Conchal", "Conchal", "Araras", "Mogi"],
    "Country": ["Jp", "Br", "Uk", "Br", "Eua"]
})


@app.route("/")
def index():
    return Response(
        df.to_html(),
        mimetype="text/html",
    )

if __name__ == "__main__":
    app.run(debug=True)
