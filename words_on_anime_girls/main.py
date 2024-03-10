import cv2
import easyocr
import numpy as np
import os
import praw
import urllib.request

reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent="wordsonanimegirls",
)

# yeah lmao i don't have a gpu
reader = easyocr.Reader(["en"], gpu=False, recog_network="meme_font")

for submission in reddit.subreddit("wordsonanimegirls").top(limit=None):
    nfpath = f"ocr_girls/{submission.id}"
    if os.path.isfile(f"{nfpath}.png"):
        continue
    if submission.score < 50:
        break

    url_response = urllib.request.urlopen(submission.url)
    img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)

    if img_array is None or img_array.size == 0:
        continue

    img = cv2.imdecode(img_array, -1)
    if img is None:
        continue

    # img = preprocess_final(img)
    # text = pytesseract.image_to_string(img, lang="meme-girls", config=custom_config)
    cv2.imwrite(f"{nfpath}.png", img)
    ocr_result = reader.readtext(
        image=img,
        detail=0,
        paragraph=True,
        decoder="greedy",
        # decoder="wordbeamsearch",
        batch_size=4,
        workers=8,
        min_size=10,
        text_threshold=0.6,
    )
    text = "\n".join(ocr_result)

    with open(f"{nfpath}.txt", "w") as f:
        f.write(text)
    print(submission.id)
    print(text)

    # gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img_caption = pytesseract.image_to_string(img)
