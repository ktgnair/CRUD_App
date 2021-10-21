from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Hostname = db.Column(db.String(50),nullable=False)
    Description = db.Column(db.Text, nullable=False)
    Status = db.Column(db.String, nullable=False)
    Updated = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return 'Taskid: %r, Hostname:%s' % (self.id,self.Hostname)

@app.route("/",methods=['GET','POST'])
def home():
    if request.method == "POST":
        Hostname = request.form["Hostname"]
        Description = request.form["Description"]
        Status = request.form["Status"]
        
        details = Server(Hostname=Hostname,Description=Description,Status=Status)
        db.session.add(details)
        db.session.commit()
        return redirect("/view_server/")

    else:
        data = Server.query.all()
        return render_template("index.html",data=data)

@app.route("/view_server/")
def view():
    data = Server.query.all()
    return render_template("view_server.html",data=data)

@app.route("/add_server/")
def add():
    return render_template("add_server.html")

@app.route("/view_server/delete/<int:id>")
def delete(id):
    server_to_delete = Server.query.get_or_404(id)
    db.session.delete(server_to_delete)
    db.session.commit()
    return redirect("/view_server/")

@app.route("/view_server/update/<int:id>",methods=["GET","POST"])
def update(id):
    server_to_update = Server.query.get_or_404(id)
    if request.method == "POST":
        server_to_update.Hostname = request.form["Hostname"]
        server_to_update.Description = request.form["Description"]
        server_to_update.Status = request.form["Status"]
        db.session.commit()
        return redirect("/view_server/")
    
    else:
        return render_template("update.html",server = server_to_update)

if __name__ == "__main__":
    app.run(debug=True)