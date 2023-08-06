import bs4, requests
from bs4 import BeautifulSoup

from deep_translator import GoogleTranslator

def translate(lang, text):
	return GoogleTranslator(source='auto', target=lang).translate(text)

response = requests.get('http://rzhunemogu.ru/')
soup = BeautifulSoup(response.text, 'html.parser')

def joke(lang):
	text = soup.find(id='ctl00_ContentPlaceHolder1_Accordion1_Pane_0_content_LabelText').getText()
	return translate(lang, text)

def story(lang):
	text = soup.find(id='ctl00_ContentPlaceHolder1_Accordion2_Pane_0_content_LabelText').getText()
	return translate(lang, text)

def poem(lang):
	text = soup.find(id='ctl00_ContentPlaceHolder1_Accordion3_Pane_0_content_LabelText').getText()
	return translate(lang, text)

def aphorism(lang):
	text = soup.find(id='ctl00_ContentPlaceHolder1_Accordion4_Pane_0_content_LabelText').getText()
	return translate(lang, text)

def quote(lang):
	text = soup.find(id='ctl00_ContentPlaceHolder1_Accordion5_Pane_0_content_LabelText').getText()
	return translate(lang, text)

def toast(lang):
	text = soup.find(id='ctl00_ContentPlaceHolder1_Accordion6_Pane_0_content_LabelText').getText()
	return translate(lang, text)

def status(lang):
	text = soup.find(id='ctl00_ContentPlaceHolder1_Accordion8_Pane_0_content_LabelText').getText()
	return translate(lang, text)
