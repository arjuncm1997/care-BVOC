from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from health import app,db,login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id):
    return Login.query.get(int(id))


class Login(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String)
    email = db.Column(db.String)
    password=db.Column(db.String)
    usertype=db.Column(db.String)
    image = db.Column(db.String)

class Adddocter(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200))
    age=db.Column(db.Integer)
    Qualification=db.Column(db.String)
    specilizedarea=db.Column(db.String)
    doctertype=db.Column(db.String)
    email=db.Column(db.String)
    password=db.Column(db.String)
    img=db.Column(db.String(30),nullable=False,default="default.jpg")


class Addstaff(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200))
    age=db.Column(db.Integer)
    address=db.Column(db.String)
    qualification=db.Column(db.String)
    experience=db.Column(db.String)
    email=db.Column(db.String)
    password=db.Column(db.String)
    img=db.Column(db.String(30),nullable=False,default="img.jpg")


class Contact(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200))
    email=db.Column(db.String(200))
    mobileno=db.Column(db.Integer)
    message=db.Column(db.String)
    usertype = db.Column(db.String(100))



class Addevent(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    ownerid = db.Column(db.String(100))
    eventname=db.Column(db.String(200))
    eventdate=db.Column(db.String)
    eventtime=db.Column(db.Integer)
    eventtype=db.Column(db.String)
    staffid=db.Column(db.Integer)
    staffname=db.Column(db.String)
    status=db.Column(db.String)
    


class Registration(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String)
    username=db.Column(db.String)
    password=db.Column(db.String)
    


class Addelder(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    ownerid=db.Column(db.String)
    name=db.Column(db.String(200))
    age=db.Column(db.Integer)
    gender=db.Column(db.String)
    mobilenoofguardian=db.Column(db.Integer)
    guardianname=db.Column(db.String)
    img=db.Column(db.String(30),nullable=False,default="img2.jpg")


class Donation(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200))
    email=db.Column(db.String(200))
    donation=db.Column(db.String)
    message=db.Column(db.String)
    


class Schedule(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200))
    section=db.Column(db.String(200))
    time=db.Column(db.Integer)
    date=db.Column(db.Date)


class Payment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200))
    section=db.Column(db.String(200))
    amount=db.Column(db.Integer)
    paymenttype=db.Column(db.String)


class Patientdetails(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200))
    age=db.Column(db.Integer)
    checkingdate=db.Column(db.String)
    details=db.Column(db.String)



class Kids(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    ownerid=db.Column(db.String)
    kidname=db.Column(db.String(200))
    address=db.Column(db.String(200))
    guadianname=db.Column(db.String)
    mobileno=db.Column(db.Integer)
    age=db.Column(db.Integer)
    img=db.Column(db.String(30),nullable=False,default="img5.jpg")
    status=db.Column(db.String)


class Member(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    ownerid=db.Column(db.String)
    name=db.Column(db.String(200))
    address=db.Column(db.String(200))
    course=db.Column(db.String)
    time=db.Column(db.Integer)
    img=db.Column(db.String(30),nullable=False,default="img7.jpg")

class Daily(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    date=db.Column(db.Date)
    time=db.Column(db.Integer)
    programme=db.Column(db.String)
    staffname=db.Column(db.String)
    membersattend=db.Column(db.Integer)
    

class Gallery(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.VARCHAR)
    img = db.Column(db.String(20), nullable=False, default='default.jpg')  
    
    
class Chat(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    userid=db.Column(db.String)
    staffid=db.Column(db.String)
    message=db.Column(db.String(200))
    sid=db.Column(db.String)
    rid=db.Column(db.String)
    date = db.Column(db.String)
    time = db.Column(db.String)
    status=db.Column(db.String)