import os
import openai
from requests import post
import base64
from dotenv import load_dotenv
load_dotenv()

def write(command):
  openai.api_key = '' # openai APY KEY
  response = openai.Completion.create(model="text-davinci-002",prompt=command,temperature=0.7,max_tokens=1000,top_p=1,frequency_penalty=0,presence_penalty=0)
  return response["choices"][0]["text"].strip()

key = os.getenv('key')
secret = os.getenv('secret')
tag = os.getenv('tag')
country = os.getenv('country')
name = os.getenv('username')
password = os.getenv('password')
credential = f'{name}:{password}'
token = base64.b64encode(credential.encode())
header = {'Authorization': 'Basic ' + token.decode("utf-8")}

def text_formating(text):
    text = text.replace('.','.---').split('---')
    retun_text1 = '<!-- wp:paragraph --><p>' + ''.join(text[0:2]) + '</p><!-- /wp:paragraph -->'
    retun_text2 = '<!-- wp:paragraph --><p>' + ''.join(text[2:4]) + '</p><!-- /wp:paragraph -->'
    retun_text3 = '<!-- wp:paragraph --><p>' + ''.join(text[4:6]) + '</p><!-- /wp:paragraph -->'
    retun_text4 = '<!-- wp:paragraph --><p>' + ''.join(text[6:8]) + '</p><!-- /wp:paragraph -->'
    retun_text5 = '<!-- wp:paragraph --><p>' + ''.join(text[8:10]) + '</p><!-- /wp:paragraph -->'
    return retun_text1+retun_text2+retun_text3+retun_text4+retun_text5

def wp_heading_two(text):
    code = f'<!-- wp:heading --><h2>{text}</h2><!-- /wp:heading -->'
    return code

with open('keyword.txt', 'r+') as file:
    keyword = file.read()

def buying_guide():
    intro = '<!-- wp:paragraph --><p>' + text_formating(write(f'write an intro on what to consider before buying a {keyword}.') + '</p><!-- /wp:paragraph -->').strip().strip('\n')
    heading1 = "<!-- wp:heading --><h2>Price:</h2><!-- /wp:heading -->"
    price = text_formating(write(f"talk about why consider price when buying a {keyword}.")).strip().strip('\n')
    heading2 = "<!-- wp:heading --><h2>Durability</h2><!-- /wp:heading -->"
    durability = text_formating(write(f"talk about why consider durability when buying a {keyword}.")).strip().strip('\n')
    heading3 = "<!-- wp:heading --><h2>Durability</h2><!-- /wp:heading -->"
    feature = text_formating(write(f"talk about why consider features when buying a {keyword}.")).strip().strip('\n')
    heading_conclusion = "<!-- wp:heading --><h2>Conclusion:</h2><!-- /wp:heading -->"
    conclusion = '<!-- wp:paragraph --><p>' + text_formating(write(f'Write a conclusion for the blog post about {keyword}.') + '</p><!-- /wp:paragraph -->').strip().strip('\n')
    generated_body = intro + heading1 + price + heading2 + durability + heading3 + feature + heading_conclusion + conclusion
    return generated_body


title = keyword + "Buying Guide"
my_title = title.title()
section = buying_guide()


def wp_posting(my_title, slug, content, status='publish'):
    Api_url = 'https://example.com/wp-json/wp/v2/posts'
    data = {
        'title': my_title,
        'slug': slug,
        'content': content,
        'status': status
    }
    res = post(Api_url, headers=header, data=data)
    if res.status_code == 201:
        print('successfully posted')
    else:
        print('something wrong')


full_content = section
wp_posting(my_title, full_content)



