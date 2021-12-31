import os
import getpass
import flickrapi
import pprint
import json
import requests
import sys
import urllib.request

api_key = os.getenv("FLICKR_API_KEY")
api_secret = os.getenv("FLICKR_SECRET")
ow_api_key = os.getenv("OPEN_WEATHER_API_KEY")
ow_base_url = "http://api.openweathermap.org/data/2.5/weather?"
username = getpass.getuser()

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

def get_location():
  # Request IP address location from ipinfo
  try:
    return json.load(urllib.request.urlopen('http://ipinfo.io/json'))
  except urllib.error.HTTPError:
    return False
  

def get_weather_desc():
  # Find current weather in user city using Open Weather API
  city_name = get_location()['city'] + ", " + get_location()['country']
  weather_url = ow_base_url + "appid=" + ow_api_key + "&q=" + city_name
  json_ow_response = requests.get(weather_url).json()

  if json_ow_response["cod"] != "404":
    return json_ow_response['weather'][0]['description']


def create_folder(path):
  if not os.path.isdir(path):
    os.makedirs(path)

def download_image(path, url):
  create_folder(path)
  image_name = 'bg' + '.jpg'
  image_path = os.path.join(path, image_name)

  response=requests.get(url, stream=True)
  with open(image_path, 'wb') as out_image:
    out_image.write(response.content)

def update_wallpaper(path, url):
  download_image(path, url)
  cmd = """"""
  cmd += ("osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"/Users/"+username+"/Desktop/background_images/bg.jpg\"'")
  os.system(cmd)
  # Restart dock to see changes
  cmd = "killall Dock"
  os.system(cmd)

def new_wallpaper(search_term):
  # Find relevant large images that match search terms through Flickr API
  photo_ids = []
  photo_group = flickr.photos.search(api_key=api_key,
                                tags=search_term,
                                tag_mode = 'all',
                                extras="url_l",
                                per_page=10,
                                sort='interestingness-desc')

  for img in photo_group['photos']['photo']:
    photo_ids.append(img['id'])
  
  # Only use 4K images
  for id in photo_ids:
    for size_dict in flickr.photos.getSizes(api_key=api_key,photo_id=id)['sizes']['size']:
        if size_dict['label'] == 'X-Large 4K':
          update_wallpaper("/Users/"+username+"/Desktop/background_images", size_dict['source'])
          break
    else:
      continue
    break


def main():
  if len(sys.argv) < 2:
    #Run with no search terms to have wallpaper match local weather
    pprint(get_weather_desc() + " in " + get_location()['city'] + ", " + get_location()['country'])
    search_tags = get_weather_desc().split()[-1] + ", wallpaper"
    new_wallpaper(search_tags)
  else:
    #Specify search term if you would like to manually search for topic
    new_wallpaper(sys.argv[1])

if main:
  main()
