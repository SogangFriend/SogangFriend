from json.decoder import JSONDecodeError
from unicodedata import normalize
from django.apps import AppConfig
from django.core.cache import cache
import os
from SGFriend.settings import STATICFILES_DIRS
import json


class LoadConfig(AppConfig):
    name = 'MainApp'
    verbose_name = "MainApp"

    path = STATICFILES_DIRS[0] + "/gsons/"
    gsons_dir = os.listdir(path)

    def delete_all(self):
        for i in self.gsons_dir:
            i = normalize('NFC', i)
            if os.path.isdir(self.path + i):
                gsons_per_do = os.listdir(self.path + i)
                for gson in gsons_per_do:
                    if gson == ".DS_Store":
                        continue
                    gson = normalize('NFC', i)
                    if i != gson[:len(gson) - 8]:
                        key = i + "_" + gson[:len(gson) - 8]
                        cache.delete(key)

    def ready(self):
        # TODO: Write your codes to run on startup
        print(self.gsons_dir)
        self.delete_all()
        for i in self.gsons_dir:
            i = normalize('NFC', i)
            if os.path.isdir(self.path+i):
                gsons_per_do = os.listdir(self.path+i)
                for gson in gsons_per_do:
                    if gson == ".DS_Store":
                        continue
                    # gson = normalize('NFC', i)
                    if i != gson[:len(gson)-8]:
                        key = i + "_" + gson[:len(gson)-8]
                        print(key)
                        with open(self.path+i+"/"+gson, "r") as f:
                            try:
                                json_data = json.load(f)
                            except json.decoder.JSONDecodeError:
                                continue
                            else:
                                features = json_data['features']
                                coords = []
                                for feature in features:
                                    data = {
                                        'name': feature['properties']['adm_nm'].split()[2],
                                        'coords': feature['geometry']['coordinates']
                                    }
                                    coords.append(data)
                                cache.set(key, coords)
        print(cache.get("서울특별시_금천구"))

