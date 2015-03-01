import config
import auth
import song
import songsloader
import threading
import flag

cfg = config.config()
with open('problems.info', 'r') as f:
    info = f.read()
    print(info)
auth.try_auth(cfg)
songlist = list()
flg = flag.flag()
songsupd = threading.Thread(group=None, target=songsloader.loadsongs, name='Songsloader', args=[cfg, songlist, flg], daemon=False)
songsupd.start()
