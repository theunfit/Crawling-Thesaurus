import requests
from lxml import html


def _get_synonyms(word):
    # XPATH = '//div[@class="synonyms"]/div[@class="filters"]/div[@class="relevancy-block"]/div/ul/li/a/span[@class="text"]/text()'
    # XPATH = '//div[@class="css-1kc5m8x e1qo4u830"]/section[@class="css-0 1991neq0"]/ul[/li/span/a/text()'
    XPATH = '/html/body/div/div[2]/div/div/div[2]/div/div/main/section/section/div[2]/section/ul/li/span/a/text()'
    url = ''.join(['http://www.thesaurus.com/browse/', 'crawl'])
    tree = html.fromstring(requests.get(url).text)
    # /html/body/div/div[2]/div/div/div[2]/div/div/main/section/section/div[2]/section/ul/li[3]
    return tree.xpath(XPATH)


def crawl(word, max_num_results):
    '''
		Return a list of at most "max_num_results" synonyms of "word."
	'''
    processed = []
    processing = [word]

    while len(processed) + len(processing) <= max_num_results:
        word_being_processed = processing.pop(0)
        synonyms_list = [elem for elem in _get_synonyms(word_being_processed) if elem not in processed]
        processing += synonyms_list
        processed.append(word_being_processed)

    overall_results = processed + processing
    if len(overall_results) > max_num_results:
        overall_results = overall_results[0:max_num_results]
    return overall_results

print(crawl('crawl', 20))
