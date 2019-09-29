#!/usr/bin/env python

# Third party imports.
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
import urllib.parse

# Window configuration.
from pymongo import MongoClient

Window.size = (int(1080 * 0.25), int(1920 * 0.25))


class MyApp(App):

    def build(self):
        username = urllib.parse.quote_plus('testuser')
        password = urllib.parse.quote_plus('test')
        client = MongoClient(
            "mongodb+srv://%s:%s@hackathon2019-umbc-262bo.gcp.mongodb.net/" %
            (username, password))
        db = client["sample_airbnb"]

        return Label(text = str(db.list_collection_names()))


if __name__ == "__main__":
    
    MyApp().run()
