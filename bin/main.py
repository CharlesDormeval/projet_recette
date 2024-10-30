import logging

from search_recipe import search_recipe


def recipe_input() -> str:
    """
    Ask user for the desired recipe

    :return: user input
    :rtype: str
    """
    desired_recipe = input('Please tell me, which recipe do you want to know ? \n')
    return desired_recipe


def create_logger() -> None:
    """
    Create project logger with desired format
    """
    logger = logging.getLogger('project_logger')
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)


def main():
    # Create project logger
    create_logger()
    # Get desired recipe from user
    desired_recipe = recipe_input()
    # Get recipe results
    search_recipe(desired_recipe)


if __name__ == '__main__':
    main()
