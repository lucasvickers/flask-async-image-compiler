from flask import Flask, request
from threading import Thread
from PIL import Image
import time
import urllib, cStringIO
from decimal import Decimal
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

def async_print(app, urls, postUrl):
    with app.app_context():

        targetX = 11520
        targetY = 3240

        imgs = []
        for url in urls:
            iofile = cStringIO.StringIO(urllib.urlopen(url).read())
            img = Image.open(iofile)
            # convert to RBG
            rgb = img.convert('RGB')
            szd = rgb.resize((targetX/2, targetY/2), Image.BICUBIC) 
            imgs.append(szd)


        target = Image.new('RGB', (targetX, targetY), "white")

        target.paste(imgs[0], (0,           0,         targetX/2,  targetY/2))
        target.paste(imgs[1], (targetX/2,   0,         targetX,    targetY/2))
        target.paste(imgs[2], (0,           targetY/2, targetX/2,  targetY))
        target.paste(imgs[3], (targetX/2,   targetY/2, targetX,    targetY))

        name = str(Decimal(time.time() * 100000)) + ".jpg"
        path = "/tmp/" + name
        target.save(path)

        print "image stored at: ", path

        requests.post(postUrl, files={'image': open(path, 'rb')})


@app.route('/threaded', methods=['GET', 'POST'])
def threaded_response():

    urls = []
    postUrl = None

    if  request.form.get('url1') and request.form.get('url2') and \
        request.form.get('url3') and request.form.get('url4') and \
        request.form.get('postUrl'):
            print "Using provided URLs"
            print request.form.get('url1')
            urls.append(request.form.get('url1'))
            print request.form.get('url2')
            urls.append(request.form.get('url2'))
            print request.form.get('url3')
            urls.append(request.form.get('url3'))
            print request.form.get('url4')
            urls.append(request.form.get('url4'))
            print request.form.get('postUrl')
            postUrl = request.form.get('postUrl')

    else:
        print "Using canned URLs"
        urls.append("http://www.we-inc.com/Solutions/solutions-graphics/Asset%20Areas.jpg")
        urls.append("http://www.rksolution.co.in/img/WheelAssetRegister.jpg")
        urls.append("http://www.independenceeventscenter.com/Photos/_MG_2698.jpg")
        urls.append("http://fc08.deviantart.net/fs70/i/2011/022/1/7/color_splash_by_adelenta-d37r9jo.jpg")


    thr = Thread(target=async_print, args=[app, urls, postUrl])
    thr.start()
    return 'OK'

@app.route('/post', methods=['POST'])
def post_save():
    imgFile = request.files['image']
    imgFile.save('/tmp/saved.jpg')
    return 'Saved'


if __name__ == '__main__':
    app.debug = True
    app.run()
