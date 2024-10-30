import re
import logging
from requests import get
from bs4 import BeautifulSoup
from googlesearch import search
from traceback import format_exc

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By


logger = logging.getLogger('project_logger')


def search_recipe(dish:str) -> None:
    """
    Search desired dish recipe on the internet

    :param recipe: _description_
    :type recipe: str
    """
    query = f"recette {dish}" if 'recette' not in dish else dish

    driver = webdriver.Chrome()
    driver.get(f"https://www.google.com/search?q={query}")

    # Refuser cookies
    button = driver.find_element(By.XPATH, '//div[text()="Tout refuser"]')
    button.click()

    # Afficher plus de recettes tant que possible
    try:
        while True:
            button = driver.find_element(By.XPATH, '//span[text()="Afficher plus"]')
            button.click()
    except:
        pass

    # Récuération de la page source pour scrapping
    page = BeautifulSoup(driver.page_source)

    # Récupération des composants recette avec notes
    recipes_previews = page.find_all('a', attrs={'class':'a-no-hover-decoration'})
    previews_with_rating = list()
    for preview in recipes_previews:
        if 'html' in preview.text:
            continue
        if preview.find('span', attrs={'aria-label':re.compile('.*Note.*')}):
            previews_with_rating.append(preview)
    
    # Association des recettes à des liens
    


def get_scores_for_recipes(recipes:list) -> dict:
    scores = dict()
    for recipe in recipes:
        try:
            rating = rating_scrapping(recipe)
            scores[recipe] = rating
        except:
            logger.error(format_exc())
        finally:
            if not scores.get(recipe):
                scores[recipe] = -1.0
            logger.debug(f'Page {recipe} was attributed the score {scores.get(recipe)}')


def rating_scrapping(recipe_link:str) -> float:
    """
    

    :param recipe_link: recipe link
    :type recipe_link: str
    :return: rating if found, else -1.0
    :rtype: float
    """
    


def attribute_weight_to_score() -> float:
    """
    """
    pass
