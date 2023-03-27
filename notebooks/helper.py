"""
Single source of truth for functions used across notebooks.
"""

import logging


def parse_soup(soup, id, type='Attraction'):
    # HTML container depends on tripadviser classification
    if type == 'Attraction':
        reviews = soup.find_all('div', {'data-automation': 'reviewCard'})
        if len(reviews) == 0:
            logging.info('No more reviews to parse.')
            return False
        # Initialize list for scrapings
        page = []
        # Scrape 'about' and 'address' only once per page
        try:
            about_tag = soup.find('div', class_='_d MJ').text
            if about_tag:
                logging.debug('Found About section.')
                tags = {}
                tags['id'] = id
                tags['about'] = about_tag
                # Scrape 'address' only once per page
                address_tag = soup.find(
                    'div', class_='wgNTK').find('span').text
                if address_tag:
                    logging.debug('Found Address section.')
                    tags['address'] = address_tag
                page.append(tags)
        except AttributeError:
            logging.info('No About section.')

        # Loop through each review on page
        for review in reviews:
            # check if tags present
            try:
                date_tag = review.find('div', class_='RpeCd').text
                if date_tag:
                    tags = {}
                    tags['id'] = id
                    tags['date'] = date_tag
                    tags['rating'] = review.find(
                        'svg', class_='UctUV d H0').get('aria-label')
                    tags['title'] = review.find(
                        'div', class_='biGQs _P fiohW qWPrE ncFvv fOtGX').text
                    # get review text and strip any newlines
                    text_extract = review.find(
                        'div', class_='biGQs _P pZUbB KxBGd').text
                    text_extract = text_extract.replace('\n', '')
                    tags['review'] = text_extract
                    page.append(tags)
            except AttributeError:
                logging.info('No Review section.')
        return page

    elif type == 'Restaurant':
        reviews = soup.find_all('div', class_='review-container')
        if len(reviews) == 0:
            logging.info('No more reviews to parse.')
            return False
        # Initialize list for scrapings
        page = []
        # Scrape 'address' only once per page. 'About' tag not available for restaurants
        address_tag = soup.find('span', class_='yEWoV').text
        if address_tag:
            logging.debug('Found Address section.')
            tags = {}
            tags['id'] = id
            tags['address'] = address_tag
        page.append(tags)

        # Loop through each review on page
        for review in reviews:
            # check if tags present
            date_tag = review.find('span', class_='ratingDate').get('title')
            if date_tag:
                tags = {}
                tags['id'] = id
                tags['date'] = date_tag
                tags['rating'] = review.find(
                    'span', class_="ui_bubble_rating").get('class')[1]
                tags['title'] = review.find('span', class_='noQuotes').text
                # get review text and strip any newlines
                text_extract = review.find('p', class_='partial_entry').text
                text_extract = text_extract.replace('\n', '')
                tags['review'] = text_extract
                page.append(tags)
        return page
    else:
        raise TypeError('Unsupported review type')


if __name__ == '__main__':
    pass
