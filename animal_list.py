import requests
from bs4 import BeautifulSoup

# Send a GET request 
url = "https://en.wikipedia.org/wiki/List_of_animal_names"
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the table containing the desired data using the CSS selector
table = soup.select_one("#mw-content-text > div.mw-parser-output > table:nth-child(17)")

# Process the rows in the table
rows = table.select("tbody tr")
output_rows = []

for row in rows:
    cells = row.select("td")

    # Skip rows without enough cells
    if len(cells) < 6:
        continue

    animal = cells[0].text.strip()

    # Handle cases where multiple collective nouns or collateral adjectives are present
    collective_nouns = []
    collateral_adjectives = []

    for child_node in cells[4].children:
        if child_node.name == "a":
            collective_nouns.append(child_node.text.strip())
        elif isinstance(child_node, str):
            collective_nouns.append(child_node.strip())

    for child_node in cells[5].children:
        if child_node.name == "a":
            collateral_adjectives.append(child_node.text.strip())
        elif isinstance(child_node, str):
            collateral_adjectives.append(child_node.strip())

    # Skip rows without animal or collective noun
    if not animal or not collective_nouns:
        continue

    # Generate output rows
    if len(collective_nouns) > 1:
        for noun in collective_nouns:
            output_rows.append(f"{animal} - {noun}")
    else:
        collective_noun = collective_nouns[0] if collective_nouns else ""
        if collateral_adjectives:
            for adjective in collateral_adjectives:
                output_rows.append(f"{animal} - {adjective}")
        else:
            output_rows.append(f"{animal} - {collective_noun}")

# Print the output rows
for row in output_rows:
    print(row)
