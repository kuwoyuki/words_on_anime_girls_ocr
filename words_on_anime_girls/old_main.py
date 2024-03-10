import cv2
import json
import praw
import pytesseract
import numpy as np

# import requests
from PIL import Image
import urllib.request


# def preprocess_final(im):
#     im = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
#     im = cv2.bilateralFilter(im, 5, 55, 60)
#     im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#     _, im = cv2.threshold(im, 248, 255, 1)
#     return im


reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent="",
)

# custom_config = """--oem 1 --psm 11 -c tessedit_char_whitelist="abcdefghijklmnopqrstuvwxyz_1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ?!,. '\\"\""""

for submission in reddit.subreddit("wordsonanimegirls").top(limit=None):
    if submission.score < 50:
        break
    # img = Image.open(requests.get(submission.url, stream=True).raw)
    url_response = urllib.request.urlopen(submission.url)
    img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, -1)
    if img is None or img.size == 0:
        continue

    img = preprocess_final(img)
    text = pytesseract.image_to_string(img, lang="meme-girls", config=custom_config)
    nfpath = f"imgs/{submission.id}"
    cv2.imwrite(f"{nfpath}.png", img)
    with open(f"{nfpath}.txt", "w") as f:
        f.write(text)
    print(submission.id)
    print(text)
    # gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img_caption = pytesseract.image_to_string(img)
