static_dir="app/static/dependencies/"

if [ ! -d "$static_dir" ]
then
    mkdir $static_dir
else
rm "$static_dir"*
fi

echo "Downloading static files to ${static_dir}..."

# general js and bootstrap dependencies
wget https://code.jquery.com/jquery-3.4.0.min.js -P $static_dir
wget https://code.jquery.com/jquery-3.4.0.min.map -P $static_dir
wget https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css -P $static_dir
wget https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css.map -P $static_dir
wget https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js -P $static_dir
wget https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js.map -P $static_dir
# cornerstonde depencies
wget https://unpkg.com/cornerstone-core@2.2.8/dist/cornerstone.js -P $static_dir
wget https://cdn.jsdelivr.net/npm/cornerstone-math@0.1.6/dist/cornerstoneMath.js -P $static_dir
wget https://cdn.jsdelivr.net/npm/hammerjs@2.0.8/hammer.min.js -P $static_dir
wget https://cdn.jsdelivr.net/npm/hammerjs@2.0.8/hammer.min.js.map -P $static_dir

# conerstone and cornerstone tools
wget https://unpkg.com/dicom-parser@1.8.3/dist/dicomParser.js -P $static_dir
wget https://unpkg.com/cornerstone-wado-image-loader@3.0.6/dist/cornerstoneWADOImageLoader.min.js -P $static_dir
wget https://unpkg.com/cornerstone-wado-image-loader@3.0.6/dist/cornerstoneWADOImageLoader.min.js.map -P $static_dir
wget https://unpkg.com/cornerstone-web-image-loader@2.1.1/dist/cornerstoneWebImageLoader.min.js -P $static_dir
wget https://unpkg.com/cornerstone-web-image-loader@2.1.1/dist/cornerstoneWebImageLoader.min.js.map -P $static_dir
wget https://cdn.jsdelivr.net/gh/genskeu/csTools/cornerstoneTools.js -O "$static_dir"cornerstoneTools_mod.js
wget https://cdn.jsdelivr.net/npm/cornerstone-tools@6.0.6/dist/cornerstoneTools.min.js -P $static_dir
wget https://cdn.jsdelivr.net/npm/cornerstone-tools@6.0.6/dist/cornerstoneTools.min.js.map -P $static_dir

