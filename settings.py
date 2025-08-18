import pygame
import json


class Settings:
    def __init__(self, pageManager):
        self.pageManager = pageManager
        self.screenSize = (1200, 800)
        try:
            with open("bgm/settings.json", "r") as f:
                temptDict = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            temptDict = {"defaultMusic": "bgm/bgm1 by tttiw.ogg", "defaultVolume": 1}
            print("error")
        self.defaultMusicPath = temptDict["defaultMusic"]
        self.defaultVolume = temptDict["defaultVolume"]

    def save_music_set(self):
        temptDict = {
            "defaultMusic": self.pageManager.musicPath,
            "defaultVolume": self.pageManager.volume,
        }
        with open("bgm/settings.json", "w", encoding="utf-8") as f:
            json.dump(temptDict, f, indent=4)


if __name__ == "__main__":
    print(pygame.image.get_extended())
