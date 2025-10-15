pip install requests beautifulsoup4
import requests
from bs4 import BeautifulSoup
import sys

env:
  API_KEY: ${{ secrets.AZURE_TRANSLATOR_KEY }}
  ENDPOINT: ${{ secrets.AZURE_TRANSLATOR_ENDPOINT }}
  LOCATION: ${{ secrets.AZURE_TRANSLATOR_LOCATION }}

def translate_text(text, to_lang):
    path = '/translate?api-version=3.0'
    params = f'&to={to_lang}'
    constructed_url = ENDPOINT + path + params
    headers = {
        'Ocp-Apim-Subscription-Key': API_KEY,
        'Ocp-Apim-Subscription-Region': LOCATION,
        'Content-type': 'application/json'
    }
    body = [{'text': text}]
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
    return response[0]['translations'][0]['text']

def translate_html_file(src_path, dst_path, to_lang):
    with open(src_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # 텍스트만 추출해서 번역 (태그 구조 보존)
    for element in soup.find_all(text=True):
        parent = element.parent
        if parent.name not in ['script', 'style']:
            original = element.string
            if original and original.strip():
                translated = translate_text(original, to_lang)
                element.replace_with(translated)

    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == "__main__":
    src_file = sys.argv[1]       # 원본 HTML 파일
    dst_file = sys.argv[2]       # 번역 결과 HTML 파일
    target_lang = sys.argv[3]    # 번역할 언어코드 (예: 'en', 'ja')
    translate_html_file(src_file, dst_file, target_lang)
