import re
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                       for filename in filenames if filename.endswith(".md")))


def entry_exists(entry_name):
    return bool(entry_name in list_entries())


def entry_exists_case_insens(entry_name):
    for entry in list_entries():
        if bool(entry.lower() == str(entry_name).lower()):
            return True

    return False


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    print(title + " " + content)
    f = open(filename, "w", encoding='utf-8')
    f.write(f"#{title}\n\n{content}")


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def similar_results(search_string):
    results = []

    for entry in list_entries():
        if search_string.lower() in entry.lower():
            results.append(entry)

    return results
