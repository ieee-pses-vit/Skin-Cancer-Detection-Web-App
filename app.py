from flask import Flask, render_template, request, jsonify, abort
from firebase import Firebase
# import base64

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
        "image_data":image_data
    }

    # recov_image_jpg = base64.decodestring(image_data)
    # f = open("temp.jpg","w")
    # f.write(recov_image_jpg)
    # f.close()

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
    # storage.child(user_id).child(time_stamp).child("temp1.jpg").put("temp.jpg")
    return jsonify(output)
    
@app.route("/predict",methods=["GET"])
def prediction():
    return render_template("prediction_main.html")



@app.route("/api/register",methods=["POST"])
def registration():
    req_json = request.get_json()
    if req_json:
        new_user = req_json["user"]
        new_user_id = new_user["user-id"]
        print(new_user["email-id"])
        # print()
        all_users = dict(db.child("users").get().val())
        
        check = True
        if new_user_id not in all_users:
            for user in list(all_users.keys()):
                if "email-id" in list(all_users[user].keys()):
                    if all_users[user]["email-id"] == new_user["email-id"]:
                        check = False
                        break
            if check:
                db.child("users").child(new_user_id).update(new_user)
                response = {"status":"Success","message":f"User with username {new_user_id} registered, now you may login."}
                return jsonify(response)
            else:
                response = {"status":"Failed","message":"Invalid Request - email already registered"}
                return jsonify(response)
        else:
            response = {"status":"Failed","message":"Invalid Request - User Id is already registered"}
            return jsonify(response)
    else:
        print(req_json)
        return render_template("404.html")


@app.route("/api/getusers/<username>",methods=["GET"])
def user_details(username):
    all_users = dict(db.child("users").get().val())
    response = {}
    print(all_users.keys())
    if username in all_users.keys():
        op_user = all_users[username]
        response["Status"] = "Found :)"
        response["first-name"] = op_user["first-name"]
        response["last-name"] = op_user["last-name"]
        response["user-id"] = op_user["user-id"]
        response["email-id"] = op_user["email-id"]
        response["age"] = op_user["age"]
        response["mobile-number"] = op_user["mobile-number"]
        response["gender"] = op_user["gender"]
        return jsonify(response)
    else:
        response["Status"] = "User not found :( "
        return jsonify(response)
    

@app.route("/api/login",methods=["POST"])
def logging():
    all_users = dict(db.child("users").get().val())

    input_creds = request.get_json()
    if input_creds:
        if input_creds['user-id'] in all_users.keys():
            temp = all_users[input_creds['user-id']]
            if input_creds["user-id"]==temp["user-id"] and input_creds["password"] == temp["password"]:
                tokenId = "abc"
                response = {"status":"Success","tokenId":tokenId,"message":"tokenId will be refreshed in every two hours."}
                db.child("users").child(input_creds["user-id"]).update({"tokenId":tokenId})
                return jsonify(response)    
            else:
                response = {"status":"Failed","message":"Either user-id or password is incorrect"}
                return jsonify(response)    
        else:
            response = {"status":"Failed","message":"User is not registered"}
            return jsonify(response)
    else:
        # print(req_json)
        return render_template("404.html")

# @app.route()

if __name__ == "__main__":
    app.run(port = 4568,debug=True)
    

