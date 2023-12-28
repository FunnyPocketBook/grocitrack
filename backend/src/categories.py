from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import time
from typing import Optional
import logging

from supermarktconnector.ah import AHConnector

from database.DbHandler import DbHandler
from classes.Category import Category


logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(module)s: %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)
log = logging.getLogger(__name__)


def get_category(
    category_dict: dict, parent: Optional[Category] = None, timeout: int = 3
):
    r = random.randint(1, 100)
    if r > 70:
        time.sleep(timeout)
    connector = AHConnector()
    category = Category(
        taxonomy_id=category_dict["id"],
        name=category_dict["name"],
        slug=category_dict["slugifiedName"],
        parent=parent,
        images=category_dict["images"],
    )
    if parent:
        parent.add_child(category)
        category.set_parent(parent)
    try:
        children = connector.get_sub_categories(category.taxonomy_id)["children"]
        if children:
            get_categories(children, category)
    except Exception as e:
        log.error(f"Error getting subcategories of {category.name}: {e}")
    return category


def get_categories(categories: list, parent: Optional[Category] = None):
    result = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(get_category, category, parent) for category in categories
        ]
        for future in as_completed(futures):
            result.append(future.result())
    return result


if __name__ == "__main__":
    connector = AHConnector()
    categories = connector.get_categories()
    categories = get_categories(categories)
    for category in categories:
        db_handler = DbHandler()
        db_handler.add_category(category)
