import wikipedia
from fuzzywuzzy import process
from SqliteDataBase import SqliteDataBase

db = SqliteDataBase('wiki.db', check_thread=False)

try:
    db.create_table('wiki', ['query', 'summary'])

except Exception:
    pass


def get_wiki_summary(query: str, lang: str = 'ru') -> str:
    wikipedia.set_lang(lang)
    options = wikipedia.search(query)

    for word in query.split():
        options += wikipedia.search(word)

    try:
        nearest, _ = process.extractOne(query, set(options))
        return wikipedia.summary(nearest)

    except Exception:
        return ''


def get_wiki_summary_with_db_check(query):
    try:
        record = db.get_records('wiki', 1, where=f"query='{query}'")

    except Exception:
        return ''

    if len(record):
        return record['summary']

    else:
        summary = get_wiki_summary(query)
        db.add_record('wiki', {'query': query, 'summary': summary})

        return summary
