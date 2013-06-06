"""Procedures to initialize the full text search in PostgresQL"""
from django.db import connection
from django.conf import settings as django_settings
from django.utils.translation import get_language

#mapping of "django" language names to postgres
LANGUAGE_NAMES = {
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'fi': 'finnish',
    'fr': 'french',
    'de': 'german',
    'hu': 'hungarian',
    'it': 'italian',
    'ja': 'japanese',
    'nb': 'norwegian',
    'pt': 'portugese',
    'ro': 'romanian',
    'ru': 'russian',
    'es': 'spanish',
    'sv': 'swedish',
    'tr': 'turkish'
}

def setup_full_text_search(script_path):
    """using postgresql database connection,
    installs the plsql language, if necessary
    and runs the stript, whose path is given as an argument
    """
    fts_init_query = open(script_path).read()

    cursor = connection.cursor()
    try:
        #test if language exists
        cursor.execute("SELECT * FROM pg_language WHERE lanname='plpgsql'")
        lang_exists = cursor.fetchone()
        if not lang_exists:
            cursor.execute("CREATE LANGUAGE plpgsql")
        #run the main query
        cursor.execute(fts_init_query)
    finally:
        cursor.close()

def run_full_text_search(query_set, query_text, text_search_vector_name):
    """runs full text search against the query set and
    the search text. All words in the query text are
    added to the search with the & operator - i.e.
    the more terms in search, the narrower it is.

    It is also assumed that we ar searching in the same
    table as the query set was built against, also
    it is assumed that the table has text search vector
    stored in the column called with value of`text_search_vector_name`.
    """
    table_name = query_set.model._meta.db_table
 
    rank_clause = 'ts_rank(' + table_name + \
                    '.' + text_search_vector_name + \
                    ', plainto_tsquery(%s, %s))'
 
    where_clause = table_name + '.' + \
                    text_search_vector_name + \
                    ' @@ plainto_tsquery(%s, %s)'

    language_code = get_language()

    #a hack with japanese search for the short queries
    if language_code == 'ja' and len(query_text) in (1, 2):
        mul = 4/len(query_text) #4 for 1 and 2 for 2
        query_text = (query_text + ' ')*mul

    #the table name is a hack, because user does not have the language code
    is_multilingual = getattr(django_settings, 'ASKBOT_MULTILINGUAL', True)
    if is_multilingual and table_name == 'askbot_thread':
        where_clause += " AND " + table_name + \
                        '.' + "language_code='" + language_code + "'"

    search_query = '|'.join(query_text.split())#apply "OR" operator
    language_name = LANGUAGE_NAMES.get(language_code, 'english')
    extra_params = (language_name, search_query,)
    extra_kwargs = {
        'select': {'relevance': rank_clause},
        'where': [where_clause,],
        'params': extra_params,
        'select_params': extra_params,
    }

    return query_set.extra(**extra_kwargs)

def run_thread_search(query_set, query):
    """runs search for full thread content"""
    return run_full_text_search(query_set, query, 'text_search_vector');

run_user_search = run_thread_search #an alias

def run_title_search(query_set, query):
    """runs search for title and tags"""
    return run_full_text_search(query_set, query, 'title_search_vector')
