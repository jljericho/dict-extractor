I want to be able to systematically specify how I am extracting objects from a dictionary, specifically in a way that is easy to change.

The basic idea is to allow us to specify an expected schema in a dictionary that matches the dictionary itself, and thus is easy to compare, understand, and change. For example, say we have a dictionary that describes a book.

x = {
    "title": "Harry Potter and the Philosopher's Stone",
    "authors:" ["J.K. Rowling"],
    ...,
    "identifiers": {
        "isbn": "9781408855898",
        "isbn10": "1408855895"
    }
}

Now our goal is to take this dictionary, and extract the values we care about, perhaps to standardize with other input sources or to put into a relational database.

Normally, we would define certain paths to each key, possibly abstracting out some of the work with defining regular functions to do the work. However, we lose of knowing what to change if the dictionary schema changes. Our logic may be spread out over multiple places.

Another option is to specify the schema we expect, condensing the logic into a single place.

schema = {
    "title": "{title}",
    "authors": "{authors}",
    ...,
    "identifiers": {
        "isbn": "{isbn13}",
        "isbn10": "{isbn10}"
    }
}

Now we have an exceptionally clear representation of what we expect the dictionary to look like, and critically were able to define the fields we want captured: e.g., we want isbn13 to be set to x["identifiers"]["isbn"].

The tool in this database allows us to use a dictionary of the above format, using braces specifying the fields, to extract values from dictionaries. We simply build our extractor and then use it to extract on data:

Extractor(schema).extract(x)

This would return something like the following
// -> {
    "title": "Harry Potter and the Philosopher's Stone",
    "authors:" ["J.K. Rowling"],
    "isbn13": "9781408855898",
    "isbn10": "1408855895"
}