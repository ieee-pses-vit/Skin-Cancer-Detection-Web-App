from flask import Flask, render_template, request, jsonify, abort
from firebase import Firebase
import base64

config = {
  "apiKey": "AIzaSyArL9WuBVYY04Nmt519xi08wnF6muZDIao",
  "authDomain": "skin-cancer-detection-e1c4c.firebaseapp.com",
  "databaseURL": "https://skin-cancer-detection-e1c4c.firebaseio.com",
  "projectId": "skin-cancer-detection-e1c4c",
  "storageBucket": "skin-cancer-detection-e1c4c.appspot.com",
  "serviceAccount": "skin-cancer-detection-e1c4c-firebase-adminsdk-ssryp-79ea70418c.json"
}

firebase = Firebase(config)
db = firebase.database()
storage = firebase.storage()

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def landing():
    return render_template("landing.html")

@app.route("/api/predict",methods=["POST"])
def prediction_api():
    # if request.method == "POST":
    req_json = request.get_json()
    # print(req_json)

    if req_json and "user_id" in req_json and "time_stamp" in req_json and "image_data" in req_json and "user_name" in req_json:
        user_id = req_json["user_id"]
        image_data = req_json["image_data"]
        time_stamp = req_json["time_stamp"]
        user_name = req_json["user_name"]
    else:
        return render_template("404.html")        
    
    firebase_data = {
        "user_name":user_name,
        # "image_data":image_data
    }

    recov_image_jpg = base64.decodestring(image_data)
    f = open("temp.jpg","w")
    f.write(recov_image_jpg)
    f.close()

    output = {
        user_id:{
            time_stamp:[
                firebase_data,
                {
                    "val1":1,
                    "val2":2,
                    "val3":3,
                    "val4":4,
                    "val5":5,
                }
            ]
        }
    }

    db.child(user_id).child(time_stamp).update(firebase_data)
    storage.child(user_id).child(time_stamp).child("temp1.jpg").put("temp.jpg")
    return jsonify(output)
    


@app.route("/predict",methods=["GET"])
def prediction():
    return render_template("prediction_main.html")

if __name__ == "__main__":
    app.run(port = 4568,debug=True)
    

