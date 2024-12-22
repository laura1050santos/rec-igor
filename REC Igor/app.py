from flask import Flask,Blueprint
from controller.user import userController

app=Flask(__name__)
app.register_blueprint(userController)
app.secret_key="chava-foda"

if __name__=="__main__":
    app.run(debug=True)