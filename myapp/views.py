from flask import Flask,request,url_for,render_template,make_response
from myapp import app
from myapp.thirdparty import flickr as flickr

@app.route('/')
@app.route('/index')
def welcome():
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