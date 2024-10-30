import re
import logging
from typing import List
from requests import get
from bs4 import BeautifulSoup, Tag
from traceback import format_exc
from urllib.parse import parse_qs

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By


logger = logging.getLogger('project_logger')


def search_recipe(dish:str) -> None:
    """
    Search desired dish recipes on the internet

    :param recipe: _description_
    :type recipe: str
    """
    # Create query string
    query = f"recette {dish}" if 'recette' not in dish else dish

    # Extract search page to make it scrappable
    search_page = extract_search_page(query)

    # Récupération des composants recette avec notes
    recipes_components_with_ratings = get_recipe_components_with_ratings(search_page)
    
    # Association des recettes à des liens
    recipes = dict()
    for preview in previews_with_rating:
        url_preview_tag = preview.find('a', attrs={'class':'a-no-hover-decoration'})
        url_preview = parse_qs(url_preview_tag.get('href',''))
        if url_preview:
            recipes[url_preview]['n_ratings'] = None
            recipes[url_preview]['mean'] = None
            recipes


def extract_search_page(query:str) -> BeautifulSoup:
    """
    Get google search page for query

    :param query: query to use in search bar
    :type query: str
    :return: search page
    :rtype: BeautifulSoup
    """
    driver = webdriver.Chrome()
    logger.debug(f'Searching for {query} on google')
    driver.get(f"https://www.google.com/search?q={query}")

    # Refuse all cookies
    disable_cookies_button = driver.find_element(By.XPATH, '//div[text()="Tout refuser"]')
    disable_cookies_button.click()

    # Load all recipes
    try:
        while True:
            button = driver.find_element(By.XPATH, '//span[text()="Afficher plus"]')
            button.click()
    except:
        # Will happen when "Afficher plus" button will not be available anymore
        logger.debug('All recipes loaded')

    # Récuération de la page source pour scrapping
    return BeautifulSoup(driver.page_source)


def get_recipe_components_with_ratings(search_page:BeautifulSoup) -> List[Tag]:
    """
    Extract recipe component from search page

    :param search_page: search page (scrappable)
    :type search_page: BeautifulSoup
    :return: list of tags containing ratings (no ratings -> not usable for next steps)
    :rtype: List[Tag]
    """
    recipes_components_with_ratings = list()
    # Recipe components are instances of class a-no-hover-decoration
    recipes_components = search_page.find_all('a', attrs={'class':'a-no-hover-decoration'})
    if not recipes_components:
        return recipes_components_with_ratings
    
    for component in recipes_components:
        # Ignore component containing all search page code + select those with note
        if not 'html' in component.text and component.find('span', attrs={'aria-label':re.compile('.*Note.*')}):
            recipes_components_with_ratings.append(component)
    
    return recipes_components_with_ratings
