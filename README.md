# Dictionary Extractor

This is a small, simple package to more idiomatically extract items from a python dictionary.

This package enables us to specify an expected schema of a dictionary by tagging places where we want to extract variables. This expected schema can then be used to extract a flat dictionary with new names.

For example, say we have a dictionary that describes a book. Perhaps this is a multi-level dictionary that we got from calling the Google Books API.

```python
our_book = {
    "title": "Harry Potter and the Philosopher's Stone",
    "authors": ["J.K. Rowling"],
    "...": "...",
    "identifiers": {
        "isbn": "9781408855898",
        "isbn10": "1408855895"
    }
}
```


From this dictionary, we want to extract the title, authors, and isbn13. Normally, we would define unique key paths for each of these variables. Something like:

```python
our_data = {
    "title": our_book["title"],
    "authors": our_book["authors"],
    "isbn13": our_book["identifiers"]["isbn"],
    "isbn10": our_book["identifiers"]["isbn10"],
}
```

This is a fine approach. However, it requires us to mentally map between the two formats when writing code and the code gets non-linearly harder to follow with additional layers in depth. Even worse, if our API owner decided to change the name "identifiers" to something like "industry_identifiers" then we would be required to make changes in multiple places.

Another option is to specify the schema we expect, condensing the logic into a single place.

```python
schema = {
    "title": "{title}",
    "authors": "{authors}",
    "...": "...",
    "identifiers": {
        "isbn": "{isbn13}",
        "isbn10": "{isbn10}"
    }
}
```


Now we have an exceptionally clear representation of what we expect the dictionary to look like, and critically were able to define the fields we want captured: e.g., we want isbn13 to be set to x["identifiers"]["isbn"].

The tool in this database allows us to use a dictionary of the above format, using braces specifying the fields, to extract values from dictionaries. The code refers to the braced item as a tag. We simply build our extractor and then use it to extract each tag:

```python
from dict_extractor import Extractor

Extractor(schema).extract(x)

# This would return something like the following
# // -> {
#     "title": "Harry Potter and the Philosopher's Stone",
#     "authors:" ["J.K. Rowling"],
#     "isbn13": "9781408855898",
#     "isbn10": "1408855895"
}
```
