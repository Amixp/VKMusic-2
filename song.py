class song:
    def __init__(self, newbie):
        if isinstance(newbie, dict):
            self.aid = newbie["aid"] if "aid" in newbie else "0"
            self.url = newbie["url"]
            self.artist = newbie["artist"] if "artist" in newbie else ""
            self.title = newbie["title"] if "title" in newbie else ""
            self.lyrics_id = newbie["lyrics_id"] if "lyrics_id" in newbie else "0"
            self.duration = newbie["duration"] if "duration" in newbie else "0"
        else:
            self.aid = "0"
            self.url = ""
            self.artist = ""
            self.title = ""
            self.lyrics_id = "0"
            self.duration = "0"

    def _print(self):
        obj = ""
        obj += str(self.aid)
        obj += str(self.url)
        obj += str(self.artist)
        obj += str(self.title)
        obj += str(self.lyrics_id)
        obj += str(self.duration)
        print(obj)

    def do_replacement(self, symbol):
        bad_symb = ['\\', '/', ':', '*', '?', '<', '>', '|']
        for s in bad_symb:
            self.artist = self.artist.replace(s, symbol)
            self.title = self.title.replace(s, symbol)
        self.artist = self.artist.replace('\"', "\'\'")
        self.title = self.title.replace('\"', "\'\'")