# -*- coding: utf-8 -*-
#!/usr/bin/python

import scrapy
import re
import locale

def pass_to_int(data):
    if data is not None:
        return int(re.sub(r'[^ 0-9]','',data).strip())
    
def filter_text_recent(data):
    
    clean_data = re.sub(r'[^ 0-9]','',data).lstrip().rstrip().split(' ')
    filter_object = filter(lambda x: x != "", clean_data)
    return [int(num) for num in filter_object]
    
def filter_text_past(data):

    if "(sem classificação anterior)" in data:
        return ['sem classificação anterior']

    clean_data = re.sub(r'[^ 0-9]','',data).lstrip().rstrip().split(' ')
    clean_data = list(filter(lambda x: x != "", clean_data))
    return [int(num) for num in clean_data[::-1]]

def pass_to_float(data):
    
    if data is not None:
        data = re.split(r'(\d+,\d+)',data)
        if len(data) == 3:
            data = float(data[1].replace(',','.'))
        elif len(data) == 5:
            data = float(data[3].replace(',','.'))
        
    return data
        
   
def min_max(data):
    
    if data is not None:
        data = re.split(r'(\d+,\d+)',data)
        if len(data) == 3:
            data = float(data[1].replace(',','.'))
            return [data,None]
        
        elif len(data) == 5:
            min = float(data[1].replace(',','.'))
            max = float(data[3].replace(',','.'))
            return[min,max]
            
    return [None,None]

class AmazonSpider(scrapy.Spider):
    name = 'Amazon'
    allowed_domains = ['amazon.com.br']
    start_urls = ['http://www.amazon.com.br/gp/movers-and-shakers/grocery']
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    


    def parse(self, response, **args):
        
        for item in response.css('li.zg-item-immersion'):
            
            name = item.css('img::attr(alt)').get()
            link = item.css('a.a-link-normal::attr(href)').get()
            image_link = item.css('img::attr(src)').get()
            thermometer_rank = item.css('span.zg-badge-text::text').get()
            recent_category_rank = item.css('span.zg-sales-movement::text').get()
            past_category_rank = item.css('span.zg-sales-movement::text').get()
            rank_percent_change = item.css('span.zg-percent-change::text').get()
            average_rate = item.css('span.a-icon-alt::text').get()
            rate_qty = item.css('a.a-size-small.a-link-normal::text').get()
            offers_qty = item.css('span.a-color-secondary::text').get()
            min_max_price = item.css('span.a-size-base.a-color-price').get()
            
        
            yield {
                
                'name': name,
                'link': link,
                'image_link': image_link,
                'thermometer_rank': pass_to_int(thermometer_rank),
                'recent_category_rank': filter_text_recent(recent_category_rank)[0],
                'past_category_rank': filter_text_past(past_category_rank)[0],
                'rank_percent_change': pass_to_int(rank_percent_change),
                'average_rate': pass_to_float(average_rate),
                'rate_qty': pass_to_int(rate_qty),
                'offers_qty': pass_to_int(offers_qty),
                'min_price': min_max(min_max_price)[0],
                'max_price' : min_max(min_max_price)[1]
                
            }
