from flask import Flask, request, url_for, render_template, make_response
from myapp import app
from myapp.thirdparty import flickr as flickr
import pylibmc


@app.route('/')
@app.route('/index')
def welcome():
    import random
    # fetch for
    mc = pylibmc.Client()
    front_image_list = mc.get("front_image_list")
    if not front_image_list:
        front_image = {}
        photos = flickr.interestingness()
        photo_no = random.randint(0, len(photos) - 1)
        photos_sizes = photos[photo_no].getSizes()
        front_image['index'] = photo_no
        front_image['url'] = photos_sizes[0]['source']
        for a_size in photos_sizes:
            if a_size['label'] == 'Medium 640':
                front_image['source'] = a_size['source']
                front_image['url'] = a_size['url']
        front_image_list = []
        front_image_list.append(front_image)
    else:
        random.shuffle(front_image_list)

    return render_template('welcome.html', front_image_list=front_image_list)
