import os
from flask import Flask,render_template,request,redirect,flash,url_for
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
from datetime import datetime, date

@app.route('/')
def p_layout():
    return render_template('index.html')
    
@app.route('/userlayout')
@login_required
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
@login_required
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
@login_required
def d_feedback():
    if request.method == 'POST':
        com=request.form['message']
        feed=Contact(name=current_user.username,email=current_user.email,message=com,mobileno = '',usertype='docter')
        try:
            db.session.add(feed)
            db.session.commit()
            flash('Feedback succsesfully','succses')
            return redirect('/d_feedback')
        except:
              return 'error'

    return render_template('d_feedback.html')

@app.route('/st_feedback',methods=['POST','GET'])
@login_required
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
        user=Registration(email=form.email.data,username=form.username.data)
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
@login_required
def u_layout():
    return render_template('u_layout.html')



@app.route('/us_kidadview')
@login_required
def kidadview():
    s = Kids.query.filter_by(ownerid=current_user.id).all()
    return render_template('us_kidadview.html',s=s)



@app.route('/us_elderadview')
@login_required
def elderadview():
    s = Addelder.query.filter_by(ownerid=current_user.id).all()
    return render_template('us_elderadview.html',s=s)



@app.route('/us_memberview')
@login_required
def memberview():
    s = Member.query.filter_by(ownerid=current_user.id).all()
    return render_template('us_memberview.html',s=s)




@app.route('/donation',methods=['POST','GET'])
@login_required
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
@login_required
def u_service():
    return render_template('u_service.html')

@app.route('/elderregistration',methods=['POST','GET'])
@login_required
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
            return redirect('/us_elderamount/'+str(elder.id))
        except:
            return 'error'

    return render_template('elderregistration.html')



@app.route('/kids',methods=['POST','GET'])
@login_required
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
            print(adm.id)
            return redirect('/us_amount/'+str(adm.id))
        except:
            return 'error'

    return render_template('kids.html')


@app.route('/member',methods=['POST','GET'])
@login_required
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
            return redirect('/us_healthamount/'+str(mem.id))
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
            return redirect(next_page) if next_page else redirect('/adminlayout')

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
@login_required
def eventview():
    s = Addevent.query.filter_by(status='approved').all()
    return render_template('us_eventview.html',s=s)

    
    #########################################Admin##############################


@app.route('/ad_layout')
@login_required
def admin():
    return render_template('ad_layout.html')

@app.route('/adminlayout')
@login_required
def adminlayout():
    return render_template("adminlayout.html")

@app.route('/ad_kidview')
@login_required
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

@app.route('/ad_elderview')
@login_required
def ad_elderview():
    t = Addelder.query.all()
    return render_template('ad_elderview.html',t=t)

@app.route('/elderapprove/<int:id>')
def elderapprove(id):
    t = Addelder.query.get_or_404(id)
    t.status = 'approved'
    db.session.commit()
    return redirect('/ad_elderview')


@app.route('/elderreject/<int:id>')
def elderreject(id):
    t = Addelder.query.get_or_404(id)
    t.status = 'rejected'
    db.session.commit()
    return redirect('/ad_elderview')


@app.route('/ad_healthview')
@login_required
def ad_healthview():
    t = Member.query.all()
    return render_template('ad_healthview.html',t=t)

@app.route('/healthapprove/<int:id>')
def healthapprove(id):
    t = Member.query.get_or_404(id)
    t.status = 'approved'
    db.session.commit()
    return redirect('/ad_healthview')


@app.route('/healthreject/<int:id>')
def healthreject(id):
    t = Member.query.get_or_404(id)
    t.status = 'rejected'
    db.session.commit()
    return redirect('/ad_healthview')


@app.route('/ad_viewcontp')
@login_required
def ad_viewcontp():
    a = Contact.query.filter_by(usertype='public').all()
    return render_template('ad_viewcontp.html',a=a)

@app.route('/ad_viewcontd')
@login_required
def ad_viewcontd():
    a = Contact.query.filter_by(usertype='docter').all()
    return render_template('ad_viewcontd.html',a=a)

@app.route('/ad_viewconts')
@login_required
def ad_viewconts():
    a = Contact.query.filter_by(usertype='staff').all()
    return render_template('ad_viewconts.html',a=a)

@app.route('/ad_viewcontu')
@login_required
def ad_viewcontu():
    a = Contact.query.filter_by(usertype='user').all()
    return render_template('ad_viewcontu.html',a=a)

@app.route('/ad_staff',methods=['POST','GET'])
@login_required
def viewstaff():
    form = StaffForm()
    if form.validate_on_submit():
        def randomString(stringLength=10):
            letters= string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(stringLength))
        f = randomString()
        print(f)
        hash=bcrypt.generate_password_hash(f).decode('utf-8')
        e =form.email.data
        staff=Addstaff(name=form.name.data,age=form.age.data,address=form.add.data,qualification=form.quali.data,experience=form.exp.data,email=form.email.data)
        staff1=Login(username=form.name.data,email=form.email.data,password=hash,usertype='staff')
        try:
            db.session.add(staff)
            db.session.add(staff1)
            db.session.commit()
            staffadd(f,e)
            flash('Send an email to Staff', 'success')
            return redirect('/ad_staff')
        except:
            return 'error'

    return render_template('ad_staff.html', form = form)

def staffadd(f,e):
    msg = Message('Approved',
                  recipients=[e])
    msg.body = f''' Your email : {e} and Password: {f} '''
    mail.send(msg) 

@app.route('/ad_staffedit/<int:id>',methods=['POST','GET'])
@login_required
def ad_staffedit(id):
    form = StaffeditForm()
    staff = Addstaff.query.get_or_404(id)
    stafflogin = Login.query.filter_by(email = staff.email).first()
    staffid = stafflogin.id
    staffpro = Login.query.get_or_404(staffid)
    if form.validate_on_submit():
        staff.name = form.name.data
        staff.age=form.age.data
        staff.address=form.add.data
        staff.qualification=form.quali.data
        staff.experience=form.exp.data
        staff.email=form.email.data
        staffpro.username = form.name.data
        staffpro.email=form.email.data
        db.session.commit()
        flash('updated succsessfully', 'success')
        return redirect('/ad_viewst')
    elif request.method == 'GET':
        form.name.data = staff.name
        form.age.data = staff.age
        form.add.data = staff.address
        form.quali.data = staff.qualification
        form.exp.data = staff.experience
        form.email.data = staff.email
    return render_template('ad_staff.html', form = form)


@app.route('/staffdelete/<int:id>')
def staffdelete(id):
    delete = Addstaff.query.get_or_404(id)
    stafflogin = Login.query.filter_by(email = delete.email).first()
    staffid = stafflogin.id
    staffpro = Login.query.get_or_404(staffid)
    db.session.delete(delete)
    db.session.delete(staffpro)
    db.session.commit()
    flash('Deleted successfully','danger')
    return redirect('/ad_viewst')

@app.route('/ad_docter',methods=['POST','GET'])
@login_required
def adddocter():
    form = DocterForm()
    if form.validate_on_submit():
        
        def randomString(stringLength=10):
            letters= string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(stringLength))
        f = randomString()
        print(f)
        hash=bcrypt.generate_password_hash(f).decode('utf-8')
        e=form.email.data
        docter=Adddocter(name=form.name.data,age=form.age.data,Qualification=form.quali.data,specilizedarea=form.speci.data,doctertype=form.doctype.data,email=form.email.data)
        doc=Login(username=form.name.data,email=form.email.data,password=hash,usertype='doctor')
        try:
            db.session.add(docter)
            db.session.add(doc)
            db.session.commit()
            docteradd(f,e)
            flash('Send an email to Docter', 'success')
            return redirect('/ad_docter')
        except:
            return 'error'

    return render_template('ad_docter.html', form =form)


def docteradd(f,e):
    msg = Message('Approved',
                  recipients=[e])
    msg.body = f''' Your email : {e} and Password: {f} '''
    mail.send(msg) 

@app.route('/ad_docteredit/<int:id>',methods=['POST','GET'])
@login_required
def ad_docteredit(id):
    form = DoctereditForm()
    docter = Adddocter.query.get_or_404(id)
    docterpro = Login.query.filter_by(email=docter.email).first()
    docterid = docterpro.id
    doc = Login.query.get_or_404(docterid)
    if form.validate_on_submit():
        docter.name=form.name.data
        docter.age=form.age.data
        docter.Qualification=form.quali.data
        docter.specilizedarea=form.speci.data
        docter.doctertype=form.doctype.data
        docter.email=form.email.data
        doc.username = form.name.data
        doc.email = form.email.data
        db.session.commit()
        flash('updated succsessfully...','success')
        return redirect('/ad_viewdoc')
    elif request.method == 'GET':
        form.name.data = docter.name
        form.age.data = docter.age
        form.quali.data = docter.Qualification
        form.speci.data = docter.specilizedarea
        form.doctype.data = docter.doctertype
        form.email.data = docter.email
    return render_template('ad_docter.html', form =form)


@app.route('/docterdelete/<int:id>')
def docterdelete(id):
    delete = Adddocter.query.get_or_404(id)
    docterlogin = Login.query.filter_by(email = delete.email).first()
    docterid = docterlogin.id
    docterpro = Login.query.get_or_404(docterid)
    db.session.delete(delete)
    db.session.delete(docterpro)
    db.session.commit()
    flash('Deleted successfully','danger')
    return redirect('/ad_viewdoc')


@app.route('/ad_viewdoc')
@login_required
def viewdoc():
    c = Adddocter.query.all()
    return render_template('ad_viewdoc.html',c=c)



@app.route('/ad_user')
@login_required
def aduser():
    user = Login.query.filter_by(usertype = 'user').all()
    return render_template('ad_user.html', user= user)


@app.route('/ad_viewst')
@login_required
def adstview():
    d = Addstaff.query.all()
    return render_template('ad_viewst.html',d=d)


@app.route('/ad_eventview')
@login_required
def viewevent():
    q = Addevent.query.filter_by(status='').all()
    return render_template('ad_eventview.html',q=q)

@app.route('/ad_approvedevents')
@login_required
def ad_approvedevents():
    q = Addevent.query.filter_by(status='approved').all()
    return render_template('ad_approvedevents.html',q=q)

@app.route('/ad_rejectedevents')
@login_required
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
@login_required
def stafflay():
    return render_template('staff_layout.html')

    
@app.route('/regview')
@login_required
def regview():
    f = Registration.query.all()
    return render_template('regview.html',f=f)


@app.route('/st_kidsview')
@login_required
def st_kidsview():
    a = Kids.query.all()
    return render_template('st_kidsview.html',a=a)



@app.route('/st_elder')
@login_required
def st_elder():
    x = Addelder.query.all()
    return render_template('st_elder.html',x=x)


@app.route('/st_memberview')
@login_required
def st_memberview():
    y = Member.query.all()
    return render_template('st_memberview.html',y=y)





@app.route('/st_eventview')
@login_required
def st_eventview():
    o = Addevent.query.filter_by(ownerid=current_user.id).all()
    return render_template('st_eventview.html',o=o)



@app.route('/addevent',methods=['POST','GET'])
@login_required
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
            return redirect('/st_eventview')
        except:
            return 'error'
    return render_template("addevent.html", staff = staff)


@app.route('/editevent/<int:id>',methods=['POST','GET'])
@login_required
def editevent(id):
    event = Addevent.query.get_or_404(id)
    staff=""
    staff1 = ""
    e = current_user.email
    staff = Addstaff.query.filter_by(email = e).first()
    print(staff)
    if request.method =='POST':
        event.eventname = request.form['evname']
        event.eventdate = request.form['date']
        event.eventtime = request.form['time']
        event.eventtype = request.form['type']
        try:
            db.session.commit()
            print('adf')
            return redirect('/st_eventview')
        except:
            return 'error'
    return render_template("editevent.html", staff = staff, event= event)

@app.route('/delevent/<int:id>')
def delevent(id):
    event = Addevent.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash ('Event Deleted ....')
    return redirect('/st_eventview')


@app.route('/docter_layout')
@login_required
def docterlay():
    return render_template('docter_layout.html')


@app.route('/doc_view')
@login_required
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
@login_required
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
            flash('Details addedd successfully..','success')
            return redirect('/doc_adddetails')
        except:
            return 'error'

    return render_template('doc_adddetails.html')


@app.route('/doc_editdetails/<int:id>',methods=['POST','GET'])
@login_required
def doc_editdetails(id):
    det = Patientdetails.query.get_or_404(id)
    if request.method == 'POST':
        det.name =request.form['name']
        det.age =request.form['age']
        det.checkingdate =request.form['date']
        det.details =request.form['details']
        db.session.commit()
        flash('updated details successfully','success')
        return redirect('/doc_view')
    return render_template('doc_editdetails.html',det=det)

@app.route('/ad_gallery',methods=['POST','GET'])
@login_required
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
@login_required
def ad_viewimage():
    d = Gallery.query.all()
    return render_template("ad_viewimage.html", d=d)

@app.route("/ad_galleryupdate/<int:id>", methods=['GET', 'POST'])
@login_required
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


@app.route('/uchat/<int:id>', methods=['GET', 'POST'])
@login_required
def uchat(id):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    today = date.today()
    print("Today's date:", today)
    staffid = id
    chat = Chat.query.filter_by(userid = current_user.id, staffid = staffid).all()
    if request.method == 'POST':
        msg =request.form['message']
        chat1 = Chat(userid =current_user.id,staffid = staffid,message=msg, sid = current_user.id, rid =staffid,date =today, time =  current_time )
        try:
            db.session.add(chat1)
            db.session.commit()
            return redirect("")
        except Exception as e:
            print(e)
    return render_template("uchat.html",chat=chat)

@app.route('/u_chatselect')
@login_required
def u_chatselect():
    user = Login.query.filter_by(usertype='staff').all()
    return render_template("u_chatselect.html",user=user)

@app.route('/st_chatselect')
@login_required
def st_chatselect():
    user = Login.query.filter_by(usertype='user').all()
    chat = Chat.query.all()
    return render_template("st_chatselect.html",user=user,chat=chat)


@app.route('/stchat/<int:id>', methods=['GET', 'POST'])
@login_required
def stchat(id):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    today = date.today()
    print("Today's date:", today)
    userid = id
    print(userid)
    sta = current_user.id
    print(sta)
    chat = Chat.query.filter_by(userid = userid, staffid = current_user.id).all()
    if request.method == 'POST':
        msg =request.form['message']
        chat1 = Chat(userid =userid,staffid = current_user.id,message=msg, sid = current_user.id, rid =userid, date =today, time =  current_time )
        try:
            db.session.add(chat1)
            db.session.commit()
            return redirect("")
        except Exception as e:
            print(e)
    return render_template("stchat.html",chat=chat)



@app.route('/us_payment/<int:id>')
@login_required
def us_payment(id):
    form1 = Creditcard()
    form2 = Paypal()
    user = Kids.query.get_or_404(id)
    return render_template('us_payment.html',user=user,form1 =form1,form2=form2)


@app.route('/creditcard/<int:id>',methods = ['GET','POST'])
@login_required
def creditcard(id):
    form1 = Creditcard()
    form2 = Paypal()
    user = Kids.query.get_or_404(id)
    admission = 'kid'
    if form1.validate_on_submit():
        user.payment = 'credit card'
        user.paymentstatus = 'completed'
        sendmail(admission)
        db.session.commit()
    if form1.validate_on_submit():
        credit = Credit(userid = current_user.id,admission='kid',admissionid=user.id,name = form1.name.data,card= form1.number.data ,cvv=form1.cvv.data , expdate=form1.date.data,amount = user.amount)
        db.session.add(credit)
        db.session.commit()
        return redirect('/successfull')
    return render_template('us_payment.html',form1 =form1,form2=form2)

@app.route('/paypal/<int:id>',methods = ['GET','POST'])
@login_required
def paypal(id):
    form1 = Creditcard()
    form2 = Paypal()
    user = Kids.query.get_or_404(id)
    admission = 'kid'
    if form2.validate_on_submit():
        user.payment = 'paypal'
        user.paymentstatus = 'completed'
        sendmail(admission)
        db.session.commit()
    if form2.validate_on_submit():
        pay = Pay(userid = current_user.id,admission='kid',admissionid=user.id,name = form2.name.data,card= form2.number.data ,cvv=form2.cvv.data , validdate=form2.date.data,amount = user.amount)
        db.session.add(pay)
        db.session.commit()
        return redirect('/successfull')
    return render_template('us_payment.html',form1 =form1,form2=form2)


@app.route('/us_amount/<int:id>',methods = ['GET','POST'])
@login_required
def us_amount(id):
    form=Amountform()
    kid = Kids.query.get_or_404(id)
    if form.validate_on_submit():
        kid.amount = '1000'
        db.session.commit()
        return redirect('/us_payment/'+str(id))
    elif request.method == 'GET':
        form.amount.data = '1000'
    return render_template("us_amount.html",form=form)


@app.route('/us_elderamount/<int:id>',methods = ['GET','POST'])
@login_required
def us_elderamount(id):
    form=Amountform()
    elder = Addelder.query.get_or_404(id)
    if form.validate_on_submit():
        elder.amount = '1000'
        db.session.commit()
        return redirect('/us_elderpayment/'+str(id))
    elif request.method == 'GET':
        form.amount.data = '1000'
    return render_template("us_amount.html",form=form)


@app.route('/us_elderpayment/<int:id>')
@login_required
def us_elderpayment(id):
    form1 = Creditcard()
    form2 = Paypal()
    user = Addelder.query.get_or_404(id)
    return render_template('us_elderpayment.html',user=user,form1 =form1,form2=form2)


@app.route('/eldercreditcard/<int:id>',methods = ['GET','POST'])
@login_required
def eldercreditcard(id):
    form1 = Creditcard()
    form2 = Paypal()
    user = Addelder.query.get_or_404(id)
    admission='elder'
    if form1.validate_on_submit():
        user.payment = 'credit card'
        user.paymentstatus = 'completed'
        sendmail(admission)
        db.session.commit()
    if form1.validate_on_submit():
        credit = Credit(userid = current_user.id,admission='elder',admissionid=user.id,name = form1.name.data,card= form1.number.data ,cvv=form1.cvv.data , expdate=form1.date.data,amount = user.amount)
        db.session.add(credit)
        db.session.commit()
        return redirect('/successfull')
    return render_template('us_elderpayment.html',form1 =form1,form2=form2)

@app.route('/elderpaypal/<int:id>',methods = ['GET','POST'])
@login_required
def elderpaypal(id):
    form1 = Creditcard()
    form2 = Paypal()
    user = Addelder.query.get_or_404(id)
    admission='elder'
    if form2.validate_on_submit():
        user.payment = 'paypal'
        user.paymentstatus = 'completed'
        sendmail(admission)
        db.session.commit()
    if form2.validate_on_submit():
        pay = Pay(userid = current_user.id,admission='elder',admissionid=user.id,name = form2.name.data,card= form2.number.data ,cvv=form2.cvv.data , validdate=form2.date.data,amount = user.amount)
        db.session.add(pay)
        db.session.commit()
        return redirect('/successfull')
    return render_template('us_elderpayment.html',form1 =form1,form2=form2)



@app.route('/us_healthamount/<int:id>',methods = ['GET','POST'])
@login_required
def us_healthamount(id):
    form=Amountform()
    health = Member.query.get_or_404(id)
    if form.validate_on_submit():
        health.amount = '1000'
        db.session.commit()
        return redirect('/us_healthpayment/'+str(id))
    elif request.method == 'GET':
        form.amount.data = '1000'
    return render_template("us_amount.html",form=form)

@app.route('/us_healthpayment/<int:id>')
@login_required
def us_healthpayment(id):
    form1 = Creditcard()
    form2 = Paypal()
    user = Member.query.get_or_404(id)
    return render_template('us_healthpayment.html',user=user,form1 =form1,form2=form2)


@app.route('/healthcreditcard/<int:id>',methods = ['GET','POST'])
@login_required
def healthcreditcard(id):
    form1 = Creditcard()
    form2 = Paypal()
    user = Member.query.get_or_404(id)
    admission = 'health'
    if form1.validate_on_submit():
        user.payment = 'credit card'
        user.paymentstatus = 'completed'
        sendmail(admission)
        db.session.commit()
    if form1.validate_on_submit():
        credit = Credit(userid = current_user.id,admission='health',admissionid=user.id,name = form1.name.data,card= form1.number.data ,cvv=form1.cvv.data , expdate=form1.date.data,amount = user.amount)
        db.session.add(credit)
        db.session.commit()
        return redirect('/successfull')
    return render_template('us_healthpayment.html',form1 =form1,form2=form2)

@app.route('/healthpaypal/<int:id>',methods = ['GET','POST'])
@login_required
def healthpaypal(id):
    form1 = Creditcard()
    form2 = Paypal()
    user = Member.query.get_or_404(id)
    admission = 'health'
    if form2.validate_on_submit():
        user.payment = 'paypal'
        user.paymentstatus = 'completed'
        sendmail(admission)
        db.session.commit()
    if form2.validate_on_submit():
        pay = Pay(userid = current_user.id,admission='health',admissionid=user.id,name = form2.name.data,card= form2.number.data ,cvv=form2.cvv.data , validdate=form2.date.data,amount = user.amount)
        db.session.add(pay)
        db.session.commit()
        return redirect('/successfull')
    return render_template('us_healthpayment.html',form1 =form1,form2=form2)


def sendmail(admission):
    msg = Message('successful',
                  recipients=[current_user.email])
    msg.body = f'''Your {admission} Admission Successfully Completed.... And Transactions Completed Successfully..  '''
    mail.send(msg)



@app.route('/successfull')
@login_required
def successfull():
    return render_template("successfull.html")


@app.route('/us_profile',methods = ['GET','POST'])
@login_required
def us_profile():
    form = Accountform()
    reg = Registration.query.filter_by(email = current_user.email).first()

    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            current_user.image = picture_file
        current_user.username = form.name.data
        current_user.email = form.email.data
        reg.username = form.name.data
        reg.email = form.email.data
        db.session.commit() 
    elif request.method == 'GET':
        form.name.data = reg.username
        form.email.data = reg.email
    return render_template("us_profile.html",form=form)


@app.route('/st_profile',methods = ['GET','POST'])
@login_required
def st_profile():
    form = Accountformstaff()
    staff = Addstaff.query.filter_by(email = current_user.email).first()

    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            current_user.image = picture_file
            staff.img = picture_file
        current_user.username = form.name.data
        current_user.email = form.email.data
        staff.name = form.name.data
        staff.email = form.email.data
        staff.age = form.age.data
        staff.experience = form.exp.data
        staff.address = form.add.data
        staff.qualification = form.quali.data
        db.session.commit() 
    elif request.method == 'GET':
        form.name.data = staff.name
        form.email.data = staff.email
        form.age.data = staff.age
        form.exp.data = staff.experience
        form.add.data = staff.address
        form.quali.data = staff.qualification
    return render_template("st_profile.html",form=form)

@app.route('/d_profile',methods = ['GET','POST'])
@login_required
def d_profile():
    form = Accountformdocter()
    docter = Adddocter.query.filter_by(email = current_user.email).first()

    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            current_user.image = picture_file
            docter.img = picture_file
        current_user.username = form.name.data
        current_user.email = form.email.data
        docter.name = form.name.data
        docter.email = form.email.data
        docter.age = form.age.data
        docter.Qualification = form.quali.data
        docter.specilizedarea = form.speci.data
        docter.doctertype = form.dtype.data
        db.session.commit() 
    elif request.method == 'GET':
        form.name.data = docter.name
        form.email.data = docter.email
        form.age.data = docter.age
        form.quali.data = docter.Qualification
        form.speci.data = docter.specilizedarea
        form.dtype.data = docter.doctertype
    return render_template("d_profile.html",form=form)


@app.route('/d_changepassword', methods=['GET', 'POST'])
@login_required
def d_changepassword():
    form = Changepassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        logout_user()
        flash('Your Password Has Been Changed')
        return redirect('/signin') 
    return render_template('d_changepassword.html', form=form)


@app.route('/us_changepassword', methods=['GET', 'POST'])
@login_required
def us_changepassword():
    form = Changepassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        logout_user()
        flash('Your Password Has Been Changed')
        return redirect('/signin') 
    return render_template('us_changepassword.html', form=form)

@app.route('/st_changepassword', methods=['GET', 'POST'])
@login_required
def st_changepassword():
    form = Changepassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        logout_user()
        flash('Your Password Has Been Changed')
        return redirect('/signin') 
    return render_template('st_changepassword.html', form=form)


@app.route('/resetrequest', methods=['GET','POST'])
def resetrequest():
    form = Reset()
    if form.validate_on_submit():
        user = Login.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect('/resetrequest')
    return render_template("resetrequest.html",form = form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('resettoken', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route("/resetpassword/<token>", methods=['GET', 'POST'])
def resettoken(token):
    user = Login.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect('/resetrequest')
    form = Changepassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect('/signin')
    return render_template('resetpassword.html', title='Reset Password', form=form)