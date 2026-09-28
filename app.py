from flask import Flask, request, jsonify, send_file, render_template
from Duplicate_Finder_Application import process_file
import os


app = Flask(__name__)


LATEST_FILE = None
LATEST_TYPE = None



@app.route("/")
def home():

    return render_template("index.html")




@app.route("/upload", methods=["POST"])
def upload():

    global LATEST_FILE, LATEST_TYPE


    try:


        file = request.files["file"]


        result = process_file(file)



        LATEST_FILE = result["file"]

        LATEST_TYPE = result["file_type"]



        return jsonify({

            "total": result["total"],

            "clean": result["clean"],

            "duplicate": result["duplicate"],

            "cid": result["cid"],

            "domain": result["domain"],

            "client": result["client"]

        })



    except ValueError as e:


        return jsonify({

            "error": str(e)

        }),400




    except Exception as e:


        return jsonify({

            "error": str(e)

        }),500







@app.route("/download")
def download():


    global LATEST_FILE



    if LATEST_FILE is None:

        return "No file available",404



    if not os.path.exists(LATEST_FILE):

        return "File expired",404




    if LATEST_TYPE == "csv":

        filename = "final_clean_data.csv"


    else:

        filename = "final_clean_data.xlsx"




    return send_file(

        LATEST_FILE,

        as_attachment=True,

        download_name=filename

    )







if __name__ == "__main__":


    app.run(

        host="0.0.0.0",

        port=5000

    )