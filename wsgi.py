import os

os.environ["FIREBASE_KEY_PATH"] = "serviceAccountKey.json"
os.environ["NEWSDATA_API_KEY"] = "pub_6fa311d44ab545f289e80f78441c3d7c"

import sys
path = "/home/israel00/news-guy"
if path not in sys.path:
    sys.path.insert(0, path)

from main import app as application
