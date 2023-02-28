from flask import Flask,render_template,redirect,request,session
import pymongo as mo
from datetime import datetime


app=Flask(__name__)
client=mo.MongoClient("mongodb+srv://admin:admin@cluster0.bwx0wog.mongodb.net/?retryWrites=true&w=majority")
db=client["BLOG"]
coll=db["users"]
blog=db["blogs"]
app.secret_key="abc"


@app.route("/")
def home():
     if 'user' in session:
         data=session['user']
         blogs=blog.find({})
         return render_template("index.html",data=data,blogs=blogs)
     else:
         return render_template("index.html",data="")




@app.route("/logout")
def logout():
    session.pop('user',None)
    return redirect("/")


@app.route("/register")
def register():
    return render_template("reg.html")

@app.route("/regdb",methods=["POST"])
def regdb():
    if request.method=="POST":
        coll.insert_one({"name":request.form["f_name"]+request.form["l_name"],"email":request.form["email"],"ph_num":request.form["ph_no"],"pwd":request.form["pwd"],"gender":request.form["gender"]})        
        return redirect("/login")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logindb",methods=["POST"])
def logindb():
    data=coll.find_one({"email":request.form["email"]})
    if data["pwd"]==request.form["pwd"]:
        session["user"]=data['name']
        session["email"]=data['email']
        return redirect("/")
    else:
        return redirect("/login")
    

@app.route("/myblog")
def myblog():
    data=blog.find({"email":session["email"]})
    return render_template("blogs.html",data=data)

@app.route("/deletepost",methods=["post"])
def deletepost():
    blog.delete_one({"_id":request.form["name"]})
    return redirect("/myblog")

@app.route("/newpost")
def newpost():
    return render_template("newpost.html")

@app.route("/newpostdb",methods=["POST"])
def newpostdb():
    blog.insert_one({"Topic":request.form["topic"], "Content":request.form["content"],"Author":session["user"],"Date":datetime.now(),"email":session["email"]})
    return redirect("/myblog")


if __name__=="__main__":
    app.run(debug=True)