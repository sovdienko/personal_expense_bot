"""Working with Categories of Expenses"""
from typing import Dict, List, NamedTuple

import db


class Category(NamedTuple):
    """Category structure"""
    codename: str
    name: str
    is_base_expense: bool
    aliases: List[str]


class Categories:
    def __init__(self):
        self._cagegories = self._load_categories()

    def _load_categories(self) -> List[Category]:
        """Pulling Categories List from DB"""
        categories = db.fetchall(
            'category', "codename name is_base_expense aliases".split()
        )
        categories = self._fill_aliases(categories)
        return categories

    def _fill_aliases(self, categories: List[Dict]) -> List[Category]:
        """Fill Categories within their aliases from DB"""
        categories_result = []
        for index, category in enumerate(categories):
            aliases = category['aliases'].split(',')
            aliases = list(filter(None,map(str.strip, aliases)))
            aliases.append(category['codename'])
            aliases.append(category['name'])
            categories_result.append(Category(
                codename=category['codename'],
                name=category['name'],
                is_base_expense=category['is_base_expense'],
                aliases=aliases
            ))
        return categories_result

    def get_all_categories(self) -> List[Dict]:
        """Return list of Categories"""
        return self._cagegories

    def get_category(self, category_name: str) -> Category:
        """Return Category by its alias"""
        found = None
        other_category = None
        for category in self._cagegories:
            if category.codename == 'other':
                other_category = category
            for alias in category.aliases:
                if category_name in alias:
                    found = category
        if not found:
            found = other_category
        return found
