'''

Adapted excerpt from Getting Started with Raspberry Pi by Matt Richardson

Modified by Rui Santos
Complete project details: https://randomnerdtutorials.com

'''

from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/")
def main():
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
    print("yo")

if __name__ == "__main__":
   from waitress import serve
   app.run(host='0.0.0.0', port=80, debug=True)