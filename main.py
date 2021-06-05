from flask import Flask, render_template, request, session, redirect, send_from_directory
from mysql.connector import connect
from flask_mail import Mail, Message
import random
from random import randint
import string
import os
from werkzeug.utils import secure_filename

otp = 0
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png', 'gif'}
app = Flask(__name__)
app.secret_key = '------'
app.config['UPLOAD_FOLDER'] = '-----------------------------------------'
app.config['MAX_CONTENT_PATH'] = 3145728
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='------',
    MAIL_PASSWORD='--------'
)

mail = Mail(app)


def getlogindetail():
    connection = connect(host="localhost", database="ecommerce", user="root", password="-----------")
    cur = connection.cursor()
    if "User_Id" not in session:
          loggedIn = False
          FirstName =''
          noOfItems = 0
    else:
         loggedIn = True
         query1="select User_Id,FirstName from customer_info where User_Id='{}'".format(session['User_Id'])
         cur.execute(query1)
         User_Id,FirstName =cur.fetchone()
         query2="select count(productId) from cart where User_Id='{}'".format(User_Id)
         cur.execute(query2)
         noOfItems=cur.fetchone()
    return (loggedIn,FirstName,noOfItems)


@app.route("/")
def home():
    return redirect('/index.html')


@app.route("/SignUp.html")
def signup():
    return render_template('signUp.html')


@app.route('/register', methods=['post'])
def register():
    email = request.form.get('email')
    firstname = request.form.get('firstName')
    lastname = request.form.get('lastName')
    address1 = request.form.get('address1')
    address2 = request.form.get('address2')
    city = request.form.get('city')
    pincode = request.form.get('pin-code')
    state = request.form.get('state')
    country = request.form.get('country')
    password = request.form.get('pwd')
    phone = request.form.get('Phone Number')
    connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
    cur = connection.cursor()
    query1 = "select * from customer_info where email='{}'".format(email)
    cur.execute(query1)
    xyz = cur.fetchone()
    if xyz == None:
        query = "insert into customer_info(EMail,FirstName,LastName,Password,City,State,Country,pincode,Address1,Address2,Phone_No) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                                                        email,
                                                        firstname, lastname,
                                                        password, city, state, country, pincode, address1, address2, phone)
        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        return redirect('/index.html')

    else:
        return render_template('index.html', xyz='you are already register')


@app.route("/login.html")
def login():
    return render_template('login.html')


@app.route('/checkLogin', methods=['post'])
def checkLog():
    email = request.form.get('email')
    Password = request.form.get('pwd')
    connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
    cur = connection.cursor()
    query1 = "select * from customer_info where EMail='{}'".format(email)
    cur.execute(query1)
    xyz = cur.fetchone()
    if xyz == None:
        return render_template('login.html')
    else:
        if Password == xyz[10]:
            session['EMail'] = email
            session['User_Id'] = xyz[0]
            query2 = "select * from admin where email='{}'".format(email)
            cur.execute(query2)
            xyz1 = cur.fetchone()
            if xyz1 == None:
                return redirect('/index1.html')
            else:
                return redirect('/admin.html')
        else:
            return redirect('/login.html')


@app.route("/forget")
def forget():
    email = request.form.get("email")
    return render_template('forget.html', email=email)


@app.route("/forgetPassword", methods=["POST"])
def forgetPassword():
    global otp
    email = request.form.get("email")
    connection = connect(host='localhost', database='ecommerce', user='root', password='--------')
    cur = connection.cursor()
    query1 = "select * from customer_info where EMail='{}'".format(email)
    cur.execute(query1)
    xyz = cur.fetchone()
    print(xyz)
    if (xyz == None):
        return render_template('forget.html', error="email no exist")
    else:
        otp = randint(1111, 9999)

        return redirect('/mailbhejo')


@app.route("/checkotp", methods=['POST'])
def checkotp():
    email = request.form.get("email")
    otp = request.form.get("OTP")
    connection = connect(host='localhost', database='ecommerce', user='root', password='--------')
    cur = connection.cursor()
    query1 = "select * from customer_info where EMail='{}'".format(email)
    cur.execute(query1)
    xyz = cur.fetchone()
    print(xyz)
    if xyz == None:
        return render_template("forget.html", error="NOT MATCHED!!")
    else:
        return render_template("ResetPassword.html", email=email, otp=otp)


@app.route('/mailbhejo')
def mailbhejo():
    new = str(otp)
    msg = Message(subject='mail sender', sender='--------',
                  recipients=['--------'], body=new)
    # msg.cc = ['']
    # email="--------"
    mail.send(msg)
    return render_template('OTP.html')


@app.route('/mailbhejo1')
def mailbhejo1():
    msg = Message(subject='mail sender', sender='--------',
                  recipients=['--------'], body='password updated sucessfully')
    mail.send(msg)
    return render_template('login.html')


@app.route("/reset", methods=['POST'])
def reset():
    email = request.form.get("email")
    password = request.form.get("pwd")
    connection = connect(host='localhost', database='ecommerce', user='root', password='--------')
    cur = connection.cursor()
    query1 = "update customer_info set Password='{}' where EMail='{}'".format(password, email)
    cur.execute(query1)
    connection.commit()
    return redirect('/mailbhejo1')


@app.route('/logout')
def logout():
    session.pop('User_Id', None)
    return redirect('/index.html')


@app.route("/Catagori.html")
def category():
    return render_template('Catagori.html')


@app.route("/index.html")
def index():
    connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
    cur = connection.cursor()
    query1 = "select * from products "
    cur.execute(query1)
    xyz = cur.fetchall()
    return render_template('index.html',xyz=xyz)


@app.route("/index1.html")
def index1():
    if 'User_Id' in session:
        connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
        cur = connection.cursor()
        query1 = "select * from products "
        cur.execute(query1)
        xyz = cur.fetchall()
        return render_template('index1.html',xyz=xyz)
    else:
        return redirect('index.html')


@app.route("/product_list.html")
def productlist():
    return render_template('product_list.html')


@app.route("/blog.html")
def blog():
    loggedIn, FirstName, noOfItems = getlogindetail()
    return render_template('blog.html',loggedIn=loggedIn, FirstName=FirstName, noOfItems = noOfItems)


@app.route("/single-blog.html")
def sblog():
    return render_template('single-blog.html')


@app.route("/elements.html")
def elements():
    return render_template('elements.html')


@app.route("/about.html")
def about():
    loggedIn, FirstName, noOfItems = getlogindetail()
    return render_template('about.html',loggedIn=loggedIn, FirstName=FirstName, noOfItems = noOfItems)



@app.route("/contact.html")
def contact():
    if 'User_Id' in session:
        return render_template('contact.html')
    else:
        return render_template('login.html')


@app.route("/contact1", methods=['POST'])
def contact1():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')
    connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
    cur = connection.cursor()
    query = "insert into contact(EMail,Name,Subject,Message) values('{}','{}','{}','{}')".format(
        email,
        name, subject, message)
    cur.execute(query)
    connection.commit()
    return redirect('/index1.html')


@app.route("/customerQuery.html")
def customerQuery():
    connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
    cur = connection.cursor()
    query1 = "select * from contact "
    cur.execute(query1)
    xyz = cur.fetchall()
    # print(xyz)
    return render_template('customerQuery.html', xyz=xyz)


@app.route("/admin.html")
def admin():
    return render_template('admin.html')


@app.route("/profile.html")
def profile():
    if 'User_Id' in session:
        email = session['EMail']
        id = session['User_Id']
        connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
        cur = connection.cursor()
        query1 = "select * from customer_info where User_Id='{}'".format(id)
        cur.execute(query1)
        xyz = cur.fetchone()
        return render_template('profile.html', xyz=xyz)
    return render_template('login.html')


@app.route("/edit", methods=['POST'])
def edit():
    if 'User_Id' in session:
        EMail = session['EMail']
        Id = session['User_Id']
        id = request.form.get('id')
        email = request.form.get('email')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        pincode = request.form.get('pincode')
        city = request.form.get('city')
        phone_no = request.form.get('phone')
        return render_template("edit.html", id=id, email=email, address1=address1, address2=address2, pincode=pincode,
                               city=city, phone=phone_no)
    return render_template("login.html")


@app.route("/update", methods=['POST'])
def update():
    if 'User_Id' in session:
        EMail = session['EMail']
        Id = session['User_Id']
        id = request.form.get('id')
        email = request.form.get('email')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        pincode = request.form.get('pincode')
        city = request.form.get('city')
        phone_no = request.form.get('phone')
        connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
        cur = connection.cursor()
        query1 = "update customer_info set EMail ='{}', Address1 ='{}', Address2 ='{}', pincode ='{}', City ='{}'," \
                 "Phone_No='{}' where User_Id={}".format(email, address1, address2, pincode, city, phone_no, id)
        cur.execute(query1)
        connection.commit()
        return redirect('/profile.html')
    return render_template("login.html")


@app.route("/add.html")
def add():
    connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
    cur = connection.cursor()
    query = "SELECT categoryId, name FROM categories"
    cur.execute(query)
    categories = cur.fetchall()
    return render_template('add.html', categories=categories)


@app.route("/additem",methods=['post'])
def additem():
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    stock = request.form.get('stock')
    categoryId = request.form.get('category')
    if request.method == 'POST':
        if 'img' not in request.files:
            print("file not uploaded")
        f = request.files['img']
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(f.filename)))
        image= f.filename
        print("file uploaded")


    connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
    cur = connection.cursor()

    query = "insert into products(name,price,stock,categoryId,description,image) values('{}','{}','{}','{}','{}','{}')".format(name,price,stock,categoryId,description,image)

    cur.execute(query)
    connection.commit()
    return render_template('admin.html')


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("static/uploadedimages/", filename)


@app.route("/men.html")
def men():
    loggedIn, FirstName, noOfItems = getlogindetail()
    connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
    cur = connection.cursor()
    query1 = "select * from products where categoryId='{}'".format(1)
    cur.execute(query1)
    xyz = cur.fetchall()
    return render_template('men.html', xyz=xyz,loggedIn=loggedIn, FirstName=FirstName, noOfItems = noOfItems)


@app.route("/women.html")
def women():
    loggedIn, FirstName, noOfItems = getlogindetail()
    connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
    cur = connection.cursor()
    query1 = "select * from products where categoryId='{}'".format(2)
    cur.execute(query1)
    xyz = cur.fetchall()
    return render_template('women.html', xyz=xyz,loggedIn=loggedIn, FirstName=FirstName, noOfItems = noOfItems)


@app.route("/kids.html")
def kids():
    loggedIn, FirstName, noOfItems = getlogindetail()
    connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
    cur = connection.cursor()
    query1 = "select * from products where categoryId='{}'".format(3)
    cur.execute(query1)
    xyz = cur.fetchall()
    return render_template('kids.html', xyz=xyz,loggedIn=loggedIn, FirstName=FirstName, noOfItems = noOfItems)



@app.route("/description",methods=['POST'])
def description():
    p_id=request.form.get('p_id')
    print(p_id)
    connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
    cur = connection.cursor()
    query = "select * from products where productId='{}'".format(p_id)
    cur.execute(query)
    xyz = cur.fetchall()
    return render_template('single-product.html',xyz=xyz)



@app.route("/addcart",methods=['POST'])
def addcart():
    if 'User_Id' in session:
        email = session['EMail']
        Id = session['User_Id']
        productId = request.form.get('productId')
        quantity = request.form.get('quantity')
        connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
        cur = connection.cursor()
        query1="insert into cart(User_id,productId,quantity) values('{}','{}','{}')".format(Id, productId,quantity)
        cur.execute(query1)
        connection.commit()
        return redirect('/index1.html')
    return render_template('login.html')


@app.route("/cart.html", methods=['POST'])
def cart():
    if 'User_Id' in session:
        Id = session['User_Id']
        connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
        cur = connection.cursor()
        query1="SELECT products.productId,products.name,products.price,products.description,products.image,cart.quantity from products,cart where products.productId = cart.productId  AND cart.User_Id='{}'".format(Id)
        cur.execute(query1)
        xyz = cur.fetchall()
        totalPrice = 0
        for row in xyz:
            totalPrice += int(row[2])*row[5]
        return render_template('cart.html',xyz=xyz,totalPrice=totalPrice)
    return render_template('login.html')


@app.route("/myorder.html", methods=['POST'])
def myorder():
    if 'User_Id' in session:
        Id = session['User_Id']
        connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
        cur = connection.cursor()
        query1="SELECT products.productId,products.name,products.price,products.description,products.image,cart1.quantity from products,cart1 where products.productId = cart1.productId  AND cart1.User_Id='{}'".format(Id)
        cur.execute(query1)
        xyz = cur.fetchall()
        totalPrice = 0
        for row in xyz:
            totalPrice += int(row[2])*row[5]
        return render_template('myorder.html',xyz=xyz,totalPrice=totalPrice)
    return render_template('login.html')



@app.route("/removefromcart", methods=['POST'])
def removefromcart():
    if 'User_Id' in session:
        Id = session['User_Id']
        productId = request.form.get('productId')
        connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
        cur = connection.cursor()
        query="DELETE FROM cart WHERE productID='{}' AND User_Id='{}'".format(productId, Id)
        cur.execute(query)
        connection.commit()
        query1 = "SELECT products.productId,products.name,products.price,products.description,products.image,cart.quantity from products,cart where products.productId = cart.productId  AND cart.User_Id='{}'".format(
            Id)
        cur.execute(query1)
        xyz = cur.fetchall()
        totalPrice = 0
        for row in xyz:
            totalPrice += int(row[2]) * row[5]
        return render_template('cart.html', xyz=xyz, totalPrice=totalPrice)
    return render_template('login.html')


@app.route("/bill.html")
def bill():
    if 'User_Id' in session:
        return render_template('bill.html')
    return render_template('login.html')

@app.route("/bill1",methods=['POST'])
def bill1():
    if 'User_Id' in session:
        Id = session['User_Id']
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        address1 = request.form.get('add1')
        address2 = request.form.get('add2')
        city = request.form.get('city')
        pincode = request.form.get('pin-code')
        district = request.form.get('district')
        state = request.form.get('state')
        country = request.form.get('country')
        phone = request.form.get('phone')
        connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
        cur = connection.cursor()
        query = "insert into billdetails(firstName,lastName,address1,address2,email,pincode,city,district,country,state,Phone,User_Id) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                firstname, lastname,address1,address2,email,pincode,
                 city,district, country, state , phone, Id)
        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        return redirect('/checkout.html')
    return render_template("login.html")


@app.route("/checkout.html")
def checkout():
    if 'User_Id' in session:
        Id = session['User_Id']
        connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
        cur = connection.cursor()
        query1 = "SELECT products.productId,products.name,products.price,products.description,products.image,cart.quantity from products,cart where products.productId = cart.productId  AND cart.User_Id='{}'".format(
            Id)
        cur.execute(query1)
        xyz = cur.fetchall()
        subtotal = 0
        for row in xyz:
            subtotal += int(row[2]) * row[5]
        totalprice=subtotal+50
        return render_template('checkout.html',xyz=xyz,subtotal=subtotal,totalprice=totalprice)
    return render_template('login.html')




@app.route("/confirmation.html")
def confirmation():
    if 'User_Id' in session:
        Id = session['User_Id']
        connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
        cur = connection.cursor()
        query1 = "SELECT products.productId,products.name,products.price,products.description,products.image,cart.quantity from products,cart where products.productId = cart.productId  AND cart.User_Id='{}'".format(
            Id)
        cur.execute(query1)
        xyz = cur.fetchall()
        subtotal = 0
        for row in xyz:
            subtotal += int(row[2]) * row[5]
        totalprice = subtotal + 50
        query2 = "SELECT * FROM billdetails where User_Id={} order by Bill_Id desc".format(Id)
        cur.execute(query2)
        xyz1 = cur.fetchone()
        return render_template('confirmation.html',xyz=xyz,subtotal=subtotal,totalprice=totalprice,xyz1=xyz1)
    return render_template("login.html")


@app.route("/confirm", methods=['POST'])
def confirm():
    if 'User_Id' in session:
        Id = session['User_Id']
        connection = connect(host="localhost", database="ecommerce", user="root", password="--------")
        cur = connection.cursor()
        query1 = "select * from cart where User_Id='{}'".format(Id)
        cur.execute(query1)
        xyz = cur.fetchall()
        for item in xyz:
            query2 = "insert into cart1(User_id,productId,quantity) values('{}','{}','{}')".format(item[0],item[1],item[2])
            cur.execute(query2)
            connection.commit()
        query="DELETE FROM cart WHERE User_Id='{}'".format(Id)
        cur.execute(query)
        connection.commit()
        return render_template('/confirmation1.html')
    return render_template('login.html')



if __name__ == "__main__":
    app.run()
