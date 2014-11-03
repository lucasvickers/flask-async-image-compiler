IMG1=http://www.we-inc.com/Solutions/solutions-graphics/Asset%20Areas.jpg
IMG2=http://www.rksolution.co.in/img/WheelAssetRegister.jpg
IMG3=http://www.independenceeventscenter.com/Photos/_MG_2698.jpg
IMG4=http://fc08.deviantart.net/fs70/i/2011/022/1/7/color_splash_by_adelenta-d37r9jo.jpg
POST=http://localhost:5000/post

curl --data "url1=$IMG1&url2=$IMG2&url3=$IMG3&url4=$IMG4&postUrl=$POST" http://localhost:5000/threaded
