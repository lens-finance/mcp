

import os
from csv import DictReader

from mcp_server.tools.schemas.io import CategoryTaxonomy

def get_category_taxonomy() -> list[CategoryTaxonomy]:
    """
    Retrieves the category taxonomy from the Plaid API.
    
    Returns:
        list[CategoryTaxonomy]: A list of category taxonomies.
    """

    category_taxonomy: list[CategoryTaxonomy] = []
    file_path = os.path.join(os.path.dirname(__file__), "../storage/static/plaid_categories.csv")

    with open(file_path, "r") as file:
        reader = DictReader(file)
        for row in reader:
            category_taxonomy.append(CategoryTaxonomy(
                primary_category=row["PRIMARY"],
                sub_category=row["DETAILED"].replace(f"{row['PRIMARY']}_", ""),
                description=row["DESCRIPTION"]
            ))

    return category_taxonomy