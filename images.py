from bs4 import BeautifulSoup
import requests
from datetime import datetime
import csv
import re
import shutil
import lxml
import json
from PIL import Image
from io import BytesIO


hostnames = ['https://www.beyondexteriors.com']

def get_sitemap_locs(url):
    opens=requests.get(url)
    soup=BeautifulSoup(opens.text, 'lxml')
    locs=[]
    all_links = soup.findAll('loc')
    for link in all_links:
       url = str(link).replace("<loc>","").replace("</loc>","")
       locs.append(url)
    #print(locs)
    return locs
def get_sitemap(hostname):
    sitemaps = get_sitemap_locs("{}/sitemap_index.xml".format(hostname))
    urls = []
    for sitemap in sitemaps:
        urls += get_sitemap_locs(sitemap)
    #print(urls)
    return urls

def find_links(urls):
    hostname = 'https://www.beyondexteriors.com'
    all_links_list = []
    for url in urls:
        opens2 = requests.get(url)
        soup2 = BeautifulSoup(opens2.text, 'lxml')
        all_links = soup2.findAll('a')
    for link in all_links:
        urltwo= link.get('href')
        if urltwo not in all_links_list:
            all_links_list.append(urltwo)
    return all_links_list

def retrieve_image_tags(all_links_list):
    all_image_tags = []
    all_image_sources = []
    for link in all_links_list:
        try:
            content = requests.get(link).content
            soup = BeautifulSoup(content,'lxml') 
            image_tags = soup.findAll('img')
            all_image_tags += image_tags
        except:
            pass
    return all_image_tags
    
def retrieve_image_sources(allimagetags):
    all_image_sources = []
    for image_tag in allimagetags:
        try:
            all_image_sources.append(image_tag.get('src'))
        except:
            pass
    return all_image_sources

def getfilelengths(hostname):
    r=0
    sizedict = []
    site_map = get_sitemap(hostname)
    alllinks = find_links(site_map)
    allimagetags = retrieve_image_tags(alllinks)
    allimagesources = retrieve_image_sources(allimagetags)
    for source in allimagesources:
        r +=1 
        try:
            data= requests.head(source)
            length = (data.headers['Content-length'])/1000
            im = Image.open(BytesIO(data))
            size = im.size
            sizedict.append({"id": r, 
                        "source": source,
                        "size": length})
        except:
            pass
    print(sizedict)
    return sizedict


    
    
        
getfilelengths('https://www.beyondexteriors.com')


