from flask import Flask, request, jsonify, send_file, render_template
from Duplicate_Finder_Application import process_file


app = Flask(__name__)


LATEST_FILE = None



@app.route("/")
def home():

    return render_template("index.html")




@app.route("/upload", methods=["POST"])
def upload():

    global LATEST_FILE


    try:

        file = request.files["file"]


        result = process_file(file)


        LATEST_FILE = result["file"]


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

    if LATEST_FILE is None:

        return "No file available",404



    return send_file(

        LATEST_FILE,

        as_attachment=True,

        download_name="final_clean_data.xlsx"

    )




if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )