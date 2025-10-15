from googletrans import Translator
import sys

src_file = sys.argv[1]
dst_file = sys.argv[2]
lang = sys.argv[3]

translator = Translator()
with open(src_file, "r", encoding="utf-8") as f:
    text = f.read()
translated = translator.translate(text, dest=lang).text
with open(dst_file, "w", encoding="utf-8") as f:
    f.write(translated)
