import logging
from logging import Logger
from traceback import format_exc

from search_recipe import search_recipe


def recipe_input() -> str:
    """
    Ask user for the desired recipe

    :return: user input
    :rtype: str
    """
    desired_recipe = input('Please tell me, which recipe do you want to know ? \n')
    return desired_recipe


def create_logger() -> Logger:
    """
    Create project logger with desired format

    :return: project logger
    :rtype: Logger
    """
    logger = logging.getLogger('project_logger')
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


def main():
    # Create project logger
    logger = create_logger()
    try:
        # Get desired recipe from user
        desired_recipe = recipe_input()
        # Get recipe results
        search_recipe(desired_recipe)
    except:
        logger.error(format_exc())


if __name__ == '__main__':
    main()
