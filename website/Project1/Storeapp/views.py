from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password , check_password
from .models.product import Product
from .models.category import Category
from .models.customer import Customer



print(make_password('123456'))
print(check_password('123456' ,
                     'pbkdf2_sha256$180000$E2HOryWMXI5E$Re9fqcvPLixrFtEDZjOrxuoIXIHXoZ/Uo0y/rG3T79I='))


# Create your views here.
def index(request):
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products();
    data = {}
    data['products'] = products
    data['categories'] = categories
    print('you are : ' , request.session.get('email'))

    return render(request , 'index.html' , data)


def signup(request):
    if request.method == 'GET':
        return render(request , 'signup.html')
    else:
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        Mobile = postData.get('mobile')
        email = postData.get('email')
        password = postData.get('password')

        #validation
        value = {
            'first_name' : first_name,
            'last_name' : last_name,
            'Mobile' : Mobile,
            'email' : email,
            'password' : password
        }
        error_message = None

        customer = Customer(first_name=first_name, last_name=last_name, Mobile=Mobile , email = email , password = password)

        if(not first_name):
            error_message = "First Name Required !! "
        elif len(first_name) < 2:
            error_message = 'First name must be 2 char long or more'
        elif not last_name:
            error_message = 'Last Name Required'
        elif len(last_name) < 2:
            error_message = 'Last name must be 2 char long or more'
        elif not Mobile:
            error_message = 'Mobile Number Required'
        elif len(Mobile) < 10:
            error_message = 'Mobile Number must be 10 Char Long'
        elif len(email) < 5:
            error_message = 'email must be 5 char long or more'
        elif len(password) < 6:
            error_message = 'password must be 6 char long or more',

        elif customer.isExists():
            error_message = 'Email Address Already Register..'
         #saving
        if not error_message:
            print(first_name , last_name , Mobile , email , password)
            customer.password = make_password(customer.password)
            customer.register()

            return redirect('homepage')
        else:
            data = {
                'error' : error_message,
                'values' : value

            }
            return render(request , 'signup.html' , data)


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)

        error_message = None
        if customer:
            flag = check_password(password, customer.password)

            if flag:
                request.session['customer_id'] = customer.id
                request.session['email'] = customer.email
                return redirect('homepage')

            else:
                error_message = 'Email or Password invalid!!'
        else:
            error_message = 'Email or Password invalid'

        print(email, password)
        return render(request, 'login.html', {'error': error_message})



