import os
from flask import Flask,render_template,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from health import app,db,bcrypt, mail
from health.models import Registration
import string
import random
from health.models import *
from flask_login import current_user, login_user, logout_user, login_required
from health.forms import *
from random import randint
from PIL import Image
from flask_mail import Message

@app.route('/')
def p_layout():
    return render_template('index.html')
    
@app.route('/userlayout')
def userlayout():
    return render_template('userlayout.html')
    
@app.route('/gallery')
def gallery():
    g = Gallery.query.all()
    return render_template('gallery.html', g=g)


@app.route('/layout')
def layout():
    return render_template('layout.html')

@app.route('/u_feedback',methods=['POST','GET'])
def u_feedback():
    if request.method == 'POST':
        com=request.form['message']
        feed=Contact(name=current_user.username,email=current_user.email,message=com,mobileno = '',usertype='user')
        try:
            db.session.add(feed)
            db.session.commit()
            return redirect('/u_feedback')
        except:
              return 'error'

    return render_template('u_feedback.html')

@app.route('/d_feedback',methods=['POST','GET'])
def d_feedback():
    if request.method == 'POST':
        com=request.form['message']
        feed=Contact(name=current_user.username,email=current_user.email,message=com,mobileno = '',usertype='docter')
        try:
            db.session.add(feed)
            db.session.commit()
            return redirect('/d_feedback')
        except:
              return 'error'

    return render_template('d_feedback.html')

@app.route('/st_feedback',methods=['POST','GET'])
def st_feedback():
    if request.method == 'POST':
        com=request.form['message']
        feed=Contact(name=current_user.username,email=current_user.email,message=com,mobileno = '',usertype='staff')
        try:
            db.session.add(feed)
            db.session.commit()
            return redirect('/st_feedback')
        except:
              return 'error'

    return render_template('st_feedback.html')

@app.route('/mycontact',methods=['POST','GET'])
def cot():
    if request.method =='POST':
        na=request.form['name']
        ema=request.form['email']
        mob=request.form['tel']
        mes=request.form['msg']
        con=Contact(name=na,email=ema,mobileno=mob,message=mes, usertype = 'public')
        try:
            db.session.add(con)
            db.session.commit()
            return redirect('/mycontact')
        except:
            return'error'
    return render_template('mycontact.html')


@app.route('/registration',methods=['POST','GET'])
def reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=Registration(email=form.email.data,username=form.username.data,password=hash)
        user1=Login(username=form.username.data,email=form.email.data,password=hash,usertype='user')
        try:
            db.session.add(user)
            db.session.add(user1)
            db.session.commit()
            flash('Regsieration successfully completed... You can login now..', 'success')
            return redirect('/signin')
        except:
            flash('Regsieration unsuccessfull..','danger')

    return render_template('registration.html', form = form)
    ######################################user########################################


@app.route('/u_layout')
def u_layout():
    return render_template('u_layout.html')



@app.route('/us_kidadview')
def kidadview():
    s = Kids.query.filter_by(ownerid=current_user.id).all()
    return render_template('us_kidadview.html',s=s)



@app.route('/us_elderadview')
def elderadview():
    s = Addelder.query.filter_by(ownerid=current_user.id).all()
    return render_template('us_elderadview.html',s=s)



@app.route('/us_memberview')
def memberview():
    s = Member.query.filter_by(ownerid=current_user.id).all()
    return render_template('us_memberview.html',s=s)



@app.route('/profile')
def profile():
    return render_template('profile.html')
    
@app.route('/payment')
def payment():
    return render_template('payment.html')



@app.route('/donation',methods=['POST','GET'])
def donation():
    if request.method =='POST':
        na=request.form['name']
        ema=request.form['email']
        don=request.form['donation']
        mes=request.form['mess']
        don=Donation(name=na,email=ema,donation=don,message=mes)
        try:
            db.session.add(don)
            db.session.commit()
            return redirect('/donation')
        except:
            return'error'
    return render_template('donation.html')

@app.route('/u_service')
def u_service():
    return render_template('u_service.html')

@app.route('/elderregistration',methods=['POST','GET'])
def elder():
    if request.method == 'POST':
        b =request.form['name']
        c =request.form['age']
        d =request.form['gender']
        e =request.form['mobile']
        f =request.form['gname']
        elder=Addelder(ownerid=current_user.id,name=b,age=c,gender=d,mobilenoofguardian=e,guardianname=f)
        try:
            db.session.add(elder)
            db.session.commit()
            return redirect('/elderregistration')
        except:
            return 'error'

    return render_template('elderregistration.html')



@app.route('/kids',methods=['POST','GET'])
def kid():
    if request.method == 'POST':
        a =request.form['name']
        b =request.form['add']
        c =request.form['gname']
        d =request.form['mobile']
        e =request.form['age']
        adm =Kids(ownerid=current_user.id,kidname=a,address=b,guadianname=c,mobileno=d,age=e)
        try:
            db.session.add(adm)
            db.session.commit()
            return redirect('/payment')
        except:
            return 'error'

    return render_template('kids.html')


@app.route('/member',methods=['POST','GET'])
def mem():
    if request.method == 'POST':
        a =request.form['name']
        b =request.form['add']
        c =request.form['cou']
        d =request.form['time']
        mem =Member(ownerid=current_user.id,name=a,address=b,course=c,time=d)
        try:
            db.session.add(mem)
            db.session.commit()
            return redirect('/payment')
        except:
            return 'error'

    return render_template('member.html')





@app.route("/signin", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Login.query.filter_by(email=form.email.data, usertype = 'user' ).first()
        user1 = Login.query.filter_by(email=form.email.data,  usertype = 'doctor').first()
        user2 = Login.query.filter_by(email=form.email.data,  usertype = 'staff').first()
        user3 = Login.query.filter_by(email=form.email.data,  usertype = 'admin').first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/userlayout')
        if user1 and bcrypt.check_password_hash(user1.password, form.password.data):
            login_user(user1, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/docter_layout')
        if user2 and bcrypt.check_password_hash(user2.password, form.password.data):
            login_user(user2, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/staff_layout')
        if user3 and user3.password== form.password.data:
            login_user(user3, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/ad_layout')

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('signin.html', title='Login', form =form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')



@app.route('/service')
def service():
    return render_template('service.html')



@app.route('/us_eventview')
def eventview():
    s = Addevent.query.filter_by(status='approved').all()
    return render_template('us_eventview.html',s=s)

    
    #########################################Admin##############################


@app.route('/ad_layout')
def admin():
    return render_template('ad_layout.html')


@app.route('/ad_kidview')
def kidview():
    t = Kids.query.all()
    return render_template('ad_kidview.html',t=t)

@app.route('/kidapprove/<int:id>')
def kidapprove(id):
    t = Kids.query.get_or_404(id)
    t.status = 'approved'
    db.session.commit()
    return redirect('/ad_kidview')


@app.route('/kidreject/<int:id>')
def kidreject(id):
    t = Kids.query.get_or_404(id)
    t.status = 'rejected'
    db.session.commit()
    return redirect('/ad_kidview')

@app.route('/ad_viewcontp')
def ad_viewcontp():
    a = Contact.query.filter_by(usertype='public').all()
    return render_template('ad_viewcontp.html',a=a)

@app.route('/ad_viewcontd')
def ad_viewcontd():
    a = Contact.query.filter_by(usertype='docter').all()
    return render_template('ad_viewcontd.html',a=a)

@app.route('/ad_viewconts')
def ad_viewconts():
    a = Contact.query.filter_by(usertype='staff').all()
    return render_template('ad_viewconts.html',a=a)

@app.route('/ad_viewcontu')
def ad_viewcontu():
    a = Contact.query.filter_by(usertype='user').all()
    return render_template('ad_viewcontu.html',a=a)

@app.route('/ad_staff',methods=['POST','GET'])
def viewstaff():
    if request.method =='POST':
        a=request.form['name']
        b=request.form['age']
        c=request.form['add']
        d = request.form['quali']
        ex = request.form['experi']
        e= request.form['email']
        def randomString(stringLength=10):
            letters= string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(stringLength))
        f = randomString()
        print(f)
        hash=bcrypt.generate_password_hash(f).decode('utf-8')
        staff=Addstaff(name=a,age=b,address=c,qualification=d,experience=ex,email=e,password=hash)
        staff1=Login(username=a,email=e,password=hash,usertype='staff')
        try:
            db.session.add(staff)
            db.session.add(staff1)
            db.session.commit()
            staffadd(f,e)
            flash('Send an email to Staff', 'success')
            return redirect('/ad_staff')
        except:
            return 'error'

    return render_template('ad_staff.html')


def staffadd(f,e):
    msg = Message('Approved',
                  recipients=[e])
    msg.body = f''' Your email : {e} and Password: {f} '''
    mail.send(msg) 


@app.route('/ad_docter',methods=['POST','GET'])
def adddocter():
    if request.method =='POST':
        n = request.form['name']
        a = request.form['age']
        q = request.form['qua']
        s = request.form['spe']
        d = request.form['doc']
        e = request.form['email']
        def randomString(stringLength=10):
            letters= string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(stringLength))
        f = randomString()
        print(f)
        hash=bcrypt.generate_password_hash(f).decode('utf-8')
        docter=Adddocter(name=n,age=a,Qualification=q,specilizedarea=s,doctertype=d,email=e,password=hash)
        doc=Login(username=n,email=e,password=hash,usertype='doctor')
        try:
            db.session.add(docter)
            db.session.add(doc)
            db.session.commit()
            docteradd(f,e)
            return redirect('/ad_docter')
        except:
            return 'error'

    return render_template('ad_docter.html')


def docteradd(f,e):
    msg = Message('Approved',
                  recipients=[e])
    msg.body = f''' Your email : {e} and Password: {f} '''
    mail.send(msg) 


@app.route('/ad_viewdoc')
def viewdoc():
    c = Adddocter.query.all()
    return render_template('ad_viewdoc.html',c=c)

@app.route('/ad_admission')
def addadmi():
    return render_template('ad_admission.html')


@app.route('/ad_user')
def aduser():
    user = Login.query.filter_by(usertype = 'user').all()
    return render_template('ad_user.html', user= user)


@app.route('/ad_viewst')
def adstview():
    d = Addstaff.query.all()
    return render_template('ad_viewst.html',d=d)


@app.route('/ad_eventview')
def viewevent():
    q = Addevent.query.filter_by(status='').all()
    return render_template('ad_eventview.html',q=q)

@app.route('/ad_approvedevents')
def ad_approvedevents():
    q = Addevent.query.filter_by(status='approved').all()
    return render_template('ad_approvedevents.html',q=q)

@app.route('/ad_rejectedevents')
def ad_rejectedevents():
    q = Addevent.query.filter_by(status='rejected').all()
    return render_template('ad_rejectedevents.html',q=q)

@app.route('/approve/<int:id>',methods=['GET','POST'])
def appro(id):
    a=Addevent.query.get_or_404(id)
    if request.method == 'POST':
        a.status = 'approved'
        try:
            db.session.commit()
            return redirect('/ad_eventview')
        except Exception as e:
            print(e)
    return render_template('approve.html',a=a)

@app.route('/eventreject/<int:id>')
def eventreject(id):
    a=Addevent.query.get_or_404(id)
    a.status='rejected'
    db.session.commit()
    return redirect("/ad_eventview")





################################staff##########################################



@app.route('/staff_layout')
def stafflay():
    return render_template('staff_layout.html')

    
@app.route('/regview')
def regview():
    f = Registration.query.all()
    return render_template('regview.html',f=f)


@app.route('/st_kidsview')
def st_kidsview():
    a = Kids.query.all()
    return render_template('st_kidsview.html',a=a)


@app.route('/st_elder')
def st_elder():
    x = Addelder.query.all()
    return render_template('st_elder.html',x=x)


@app.route('/st_memberview')
def st_memberview():
    y = Member.query.all()
    return render_template('st_memberview.html',y=y)





@app.route('/st_eventview')
def st_eventview():
    o = Addevent.query.filter_by(ownerid=current_user.id).all()
    return render_template('st_eventview.html',o=o)



@app.route('/addevent',methods=['POST','GET'])
def events():
    staff=""
    staff1 = ""
    e = current_user.email
    staff = Addstaff.query.filter_by(email = e).first()
    print(staff)
    if request.method =='POST':
        v = request.form['evname']
        b = request.form['date']
        c = request.form['time']
        d = request.form['type']
        adf = Addevent(ownerid = current_user.id,eventname=v,eventdate=b,eventtime=c,eventtype=d,staffid=staff.id,staffname=staff.name,status='')
        try:
            db.session.add(adf)
            db.session.commit()
            print('adf')
            return redirect('/addevent')
        except:
            return 'error'
    return render_template("addevent.html", staff = staff)


###########################################Docter#######################################




@app.route('/docter_layout')
def docterlay():
    return render_template('docter_layout.html')


@app.route('/doc_view')
def docview():
    s = Patientdetails.query.all()
    return render_template('doc_view.html',s=s)
    
@app.route('/docdel/<int:id>')
def docdel(id):
    det = Patientdetails.query.get_or_404(id)
    db.session.delete(det)
    db.session.commit()
    flash('Deleted...','success')
    return redirect('/doc_view')


@app.route('/doc_adddetails',methods=['POST','GET'])
def doc_adddetails():
    if request.method == 'POST':
        a =request.form['name']
        b =request.form['age']
        c =request.form['date']
        d =request.form['details']
        details =Patientdetails(name=a,age=b,details=d,checkingdate	=c)
        try:
            db.session.add(details)
            db.session.commit()
            return redirect('/doc_adddetails')
        except:
            return 'error'

    return render_template('doc_adddetails.html')


@app.route('/doc_editdetails/<int:id>',methods=['POST','GET'])
def doc_editdetails(id):
    det = Patientdetails.query.get_or_404(id)
    if request.method == 'POST':
        det.name =request.form['name']
        det.age =request.form['age']
        det.checkingdate =request.form['date']
        det.details =request.form['details']
        db.session.commit()
        flash('not update details','danger')
        return redirect('/doc_view')
    return render_template('doc_editdetails.html',det=det)

@app.route('/ad_gallery',methods=['POST','GET'])
def ad_gallery():
    form = Imageform()
    if form.validate_on_submit():

        if form.pic.data:
            pic_file = save_picture(form.pic.data)
            view = pic_file
        print(view)  
    
        gallery = Gallery(name=form.name.data,img=view )
       
        db.session.add(gallery)
        db.session.commit()
        print(gallery)
        flash('image added','success')
        return redirect('/ad_viewimage')
    return render_template('ad_gallery.html', form = form)

@app.route('/ad_viewimage')
def ad_viewimage():
    d = Gallery.query.all()
    return render_template("ad_viewimage.html", d=d)

@app.route("/ad_galleryupdate/<int:id>", methods=['GET', 'POST'])
def ad_galleryupdate(id):
    gallery = Gallery.query.get_or_404(id)
    form = Imageform()
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            gallery.img = picture_file
        gallery.name = form.name.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/ad_viewimage')
    elif request.method == 'GET':
        form.name.data = gallery.name
    return render_template('ad_galleryupdate.html',form=form)

@app.route('/delimage/<int:id>')
def delimage(id):
    det = Gallery.query.get_or_404(id)
    db.session.delete(det)
    db.session.commit()
    flash('Image deleted...','success')
    return redirect('/ad_viewimage')

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def save_picture(form_picture):
    random_hex = random_with_N_digits(14)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(random_hex) + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn










