# Weather-Wallpaper-Mac
Updates MacOs wallpaper with an image that matches the user's current location's weather through the use of the Open Weather API, Flickr API, and ipinfo.io.


## 🏔USAGE🏔
In order to have the program update your wallpaper with a 4K landscape image that matches the current weather in your city, run the program with no arguments. You will need to input your generated API keys for both Flickr and Open Weather.
```
python3 -m background_weather
```
## 🌦ALTERNATE USAGE🌦
To specify the search terms used to find the 4K wallpaper, pass arguments in line as a comma delimited list within quotes. These terms will be considered with AND logic. You will need to input your generated API keys for both Flickr and Open Weather.
```
python3 -m background_weather "nissan,car"
```
