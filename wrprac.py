from wordcloud import WordCloud
from PIL import Image
import numpy as np

text = ''
with open("data/KakaoTalkChats_ob.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines[5:]:
        if ' : ' in line:
            text += line.split(' : ')[1].replace('사진\n', '').replace('이모티콘\n', '').replace('ㅋ', '').replace('샵검색', '').replace('ㅇㅇ', '').replace('으으', '').replace('오오', '').replace('https', '').replace('ㅠ_ㅠ', '')

mask = np.array(Image.open('images/cloud.png'))
wc = WordCloud(font_path='/System/Library/Fonts/Supplemental/AppleGothic.ttf', background_color="white", mask=mask)
wc.generate(text)
wc.to_file("results/result_masked.png")
