from flask import Flask,request,url_for,render_template,make_response
from thirdparty import flickr as flickr


app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    forgroud_image = {}
    import random
    photos = flickr.interestingness()
    photo_no = random.randint(0,len(photos)-1)
    photos_sizes = photos[photo_no].getSizes()
    forgroud_image['no']=photo_no
    forgroud_image['url']=photos_sizes[0]['source']
    for a_size in photos_sizes:
        if a_size['label']=='Medium':
            forgroud_image['source']=a_size['source']
            forgroud_image['url']=a_size['url']
    
    return render_template('welcome.html',forgroud_image=forgroud_image)

# @app.route('/windroc',methods=['GET','POST'])
# def windroc():
#     if request.method=='POST':
#         return "Hello, windroc in POST"
#     else:
#         return "Hello, windroc in GET"

# @app.route('/<int:year>/<int:month>/<int:day>')
# def date(year,month,day):
#     return "This is "+str(year)+"-"+str(month)+"-"+str(day)

# @app.route('/url/<var>')
# def urlvar(var):
#     return var

# @app.route('/url')
# def myurl():
#     return url_for("urlvar",var=2013)

# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('hello.html', name=name)