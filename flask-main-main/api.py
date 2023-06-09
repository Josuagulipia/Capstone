import os
from datetime import timedelta
from flask import Flask,jsonify,request
from util import Preprocessing
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity
from database import init,getalluser,registerdb,logindb
from flask_cors import CORS
from waitress import serve
from flask_swagger_ui import get_swaggerui_blueprint

#init flask and sql
app = Flask(__name__)
CORS(app)
mysql = init(app)

#load tensorflow model
##preprocess = Preprocessing("model.h5")
#prediction_results = preprocess.predict()

#JWT
app.config["JWT_SECRET_KEY"] = "capstone-secret-key" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=90)
jwt = JWTManager(app)


#SWAGGER_URL = '/doc'
#API_URL = '/static/swagger.json'
#SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
   # SWAGGER_URL,
    #API_URL,
    #config={
     #   'app_name': "Leftover app"
    #}
#)
#app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

@app.route('/', methods=['GET'])
def index():
    #current_user = get_jwt_identity()
    #return jsonify(logged_in_as=current_user), 200
    return "Hello World"

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    pwd = request.form['password']
    try:
        user = logindb(mysql,email,pwd)
        if user != "":
            access_token = create_access_token(identity=email)
            data = {"message": "Login Successful" , "user": user, "access_token" : access_token}
            return jsonify(data),200
        return jsonify({"msg": "Wrong Email or Password"}), 401
    except Exception as e:
         err = jsonify(msg=f'{e}'),500
         return err

#@app.route('/predict', methods=['GET'])
#@jwt_required()
#def predict():
 #   try:
  #      data = {'success': 'true','data': prediction_results}                                                                                                                                                                                                                                                 
   #     return jsonify(data)
    #except Exception as e:
     #    err = jsonify(msg=f'{e}'),500
      #   return err


#@app.route("/predict/<product_name>", methods=['GET','POST'])
#@jwt_required()
#def predictByProductName(product_name):
 #   try:
  #      try:
   #         data = next(product for product in prediction_results if product["product_name"] == product_name)
    #        copied_dict = data.copy()
     #   except:
      #      return jsonify(status_code=404, content = {"message": f"Product '{product_name}' doesn\'t exist"}),404
       # #if method request is POST
        #if request.method == 'POST':
         #  sold = float(request.form['sold'])
          #  prediction = next(item for item in data["predictions"] if item["date"] == input_date)
           # prediction["real"] = sold
            #return data
        #GET
        #days = request.args.get('days', type = int)
        #if (days != None):
         #   copied_dict["predictions"] = copied_dict["predictions"][:days]
          #  return copied_dict
        #return data
   # except Exception as e:
    #     err = jsonify(msg=f'{e}'),500
     #    return err

@app.route('/register', methods=['POST'])
def register():
    username = request.form['name']
    email = request.form['email']
    pwd = request.form['password']
    try:
        return registerdb(mysql,username,email, pwd)
    except Exception as e:
         err = jsonify(msg=f'{e}'),500
         return err
 
@app.route('/users',methods=['GET'])
def userlist():
    try:
        user = getalluser(mysql)
        return jsonify(user)
    except Exception as e:
         err = jsonify(msg=f'{e}'),500
         return err


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=int(os.environ.get('PORT', 80)))
    #app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 80)))
    #$Env:PORT=4000