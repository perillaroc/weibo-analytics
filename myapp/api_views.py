from flask import request, url_for, render_template, jsonify
from myapp import app

import pylibmc
from myapp.thirdparty import flickr as flickr

# update foreground image array in memcache from flickr


@app.route('/api/update-front-image')
def updateFrontImage():
    total_image_count = 10
    front_image_list = []
    import random
    photos = flickr.interestingness()
    photos_select_no_list = random.sample(
        range(0, len(photos) - 1), total_image_count)
    for a_photo_no in photos_select_no_list:
        a_front_image = {}
        a_front_image['index'] = a_photo_no
        a_front_image['title'] = photos[a_photo_no].title
        a_front_image['description'] = photos[a_photo_no].description
        # size
        a_photo_sizes = photos[a_photo_no].getSizes()
        a_front_image['url'] = a_photo_sizes[0]['source']
        for a_size in a_photo_sizes:
            if a_size['label'] == 'Medium 640':
                a_front_image['source'] = a_size['source']
                a_front_image['url'] = a_size['url']
        print a_photo_no
        front_image_list.append(a_front_image)
    print front_image_list

    # store in memcache
    mc = pylibmc.Client()
    mc.set("front_image_list", front_image_list)
    front_image_list_2 = mc.get("front_image_list")
    return jsonify(front_image_list=front_image_list_2)
