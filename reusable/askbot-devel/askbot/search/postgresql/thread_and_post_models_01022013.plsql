/* function testing for existence of a column in a table
   if table does not exists, function will return "false" */
CREATE OR REPLACE FUNCTION column_exists(colname text, tablename text)
RETURNS boolean AS 
$$
DECLARE
    q text;
    onerow record;
BEGIN

    q = 'SELECT attname FROM pg_attribute WHERE attrelid = ( SELECT oid FROM pg_class WHERE relname = '''||tablename||''') AND attname = '''||colname||''''; 

    FOR onerow IN EXECUTE q LOOP
        RETURN true;
    END LOOP;

    RETURN false;
END;
$$ LANGUAGE plpgsql;

/* function adding tsvector column to table if it does not exists */
CREATE OR REPLACE FUNCTION add_tsvector_column(colname text, tablename text)
RETURNS boolean AS
$$
DECLARE
    q text;
BEGIN
    IF NOT column_exists(colname, tablename) THEN
        q = 'ALTER TABLE ' || tablename || ' ADD COLUMN ' || colname || ' tsvector';
        EXECUTE q;
        RETURN true;
    ELSE
        q = 'UPDATE ' || tablename || ' SET ' || colname || '=NULL';
        EXECUTE q;
        RETURN false;
    END IF;
END;
$$ LANGUAGE plpgsql;

/* aggregate function that concatenates tsvectors */
CREATE OR REPLACE FUNCTION tsv_add(tsv1 tsvector, tsv2 tsvector)
RETURNS tsvector AS
$$
BEGIN
    RETURN tsv1 || tsv2;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION setup_aggregates() RETURNS boolean AS
$$
DECLARE
    onerow record;
BEGIN
    FOR onerow IN SELECT * FROM pg_proc WHERE proname = 'concat_tsvectors' AND proisagg LOOP
        DROP AGGREGATE concat_tsvectors(tsvector);
    END LOOP;
    CREATE AGGREGATE concat_tsvectors (
        BASETYPE = tsvector,
        SFUNC = tsv_add,
        STYPE = tsvector,
        INITCOND = ''
    );
    RETURN true;
END;
$$ LANGUAGE plpgsql;

SELECT setup_aggregates();

/* language name resolution function. todo: move languace conv to python code */
DROP FUNCTION IF EXISTS get_language_name_from_code(lang_code text);
CREATE OR REPLACE FUNCTION get_language_name_from_code(lang_code text)
RETURNS regconfig AS
$$
BEGIN
    IF lang_code = 'en' THEN
        RETURN 'english';
    ELSIF lang_code = 'da' THEN
        RETURN 'danish';
    ELSIF lang_code = 'nl' THEN
        RETURN 'danish';
    ELSIF lang_code = 'fi' THEN
        RETURN 'finnish';
    ELSIF lang_code = 'fr' THEN
        RETURN 'french';
    ELSIF lang_code = 'de' THEN
        RETURN 'german';
    ELSIF lang_code = 'hu' THEN
        RETURN 'hungarian';
    ELSIF lang_code = 'it' THEN
        RETURN 'italian';
    ELSIF lang_code = 'nb' THEN
        RETURN 'norwegian';
    ELSIF lang_code = 'pt' THEN
        RETURN 'portugese';
    ELSIF lang_code = 'ro' THEN
        RETURN 'romanian';
    ELSIF lang_code = 'ru' THEN
        RETURN 'russian';
    ELSIF lang_code = 'es' THEN
        RETURN 'spanish';
    ELSIF lang_code = 'sv' THEN
        RETURN 'swedish';
    ELSIF lang_code = 'tr' THEN
        RETURN 'turkish';
    ELSIF lang_code = 'ja' THEN
        RETURN 'japanese';
    END IF;
    RETURN 'english';
END;
$$ LANGUAGE plpgsql;

/* calculates text search vector for the individual thread row
DOES not include question body post, answers or comments */
DROP FUNCTION IF EXISTS get_thread_tsv(title text, tagnames text);
CREATE OR REPLACE FUNCTION get_thread_tsv(title text, tagnames text, lang_code text)
RETURNS tsvector AS
$$
DECLARE
    lang_name regconfig;
BEGIN
    lang_name = get_language_name_from_code(lang_code);
    /* todo add weight depending on votes */
    RETURN  setweight(to_tsvector(lang_name, coalesce(title, '')), 'A') ||
            setweight(to_tsvector(lang_name, coalesce(tagnames, '')), 'A');
END;
$$ LANGUAGE plpgsql;

/* calculates text seanch vector for the individual question row */
DROP FUNCTION IF EXISTS get_post_tsv(text text, post_type text);
CREATE OR REPLACE FUNCTION get_post_tsv(text text, post_type text, lang_code text)
RETURNS tsvector AS
$$
DECLARE
    lang_name regconfig;
BEGIN
    /* todo adjust weights to reflect votes */
    lang_name = get_language_name_from_code(lang_code);
    IF post_type='question' THEN
        RETURN setweight(to_tsvector(lang_name, coalesce(text, '')), 'B');
    ELSIF post_type='answer' THEN
        /* todo reflect whether the answer acepted or has many points */
        RETURN setweight(to_tsvector(lang_name, coalesce(text, '')), 'C');
    ELSIF post_type='comment' THEN
        RETURN setweight(to_tsvector(lang_name, coalesce(text, '')), 'D');
    ELSE
        RETURN to_tsvector('');
    END IF;
END;
$$ LANGUAGE plpgsql;

/* calculates text search vector for the question body part by thread id
here we extract question title and the text by thread_id and then
calculate the text search vector. In the future question
title will be moved to the askbot_thread table and this function
will be simpler.
*/
CREATE OR REPLACE FUNCTION get_thread_question_tsv(thread_id integer, language_code text)
RETURNS tsvector AS
$$
DECLARE
    query text;
    onerow record;
BEGIN
    query = 'SELECT text FROM askbot_post WHERE thread_id=' || thread_id ||
            ' AND post_type=''question'' AND deleted=false';
    FOR onerow in EXECUTE query LOOP
        RETURN get_post_tsv(onerow.text, 'question', language_code);
    END LOOP;
    RETURN to_tsvector('');
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS get_dependent_comments_tsv(object_id integer, tablename text);
CREATE OR REPLACE FUNCTION get_dependent_comments_tsv(parent_id integer)
RETURNS tsvector AS
$$
DECLARE
    query text;
    onerow record;
BEGIN
    query = 'SELECT concat_tsvectors(text_search_vector), count(*) FROM askbot_post' ||
        ' WHERE parent_id=' || parent_id || 
        ' AND post_type=''comment'' AND deleted=false';
    FOR onerow IN EXECUTE query LOOP
        IF onerow.count = 0 THEN
            RETURN to_tsvector('');
        ELSE
            RETURN onerow.concat_tsvectors;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS get_dependent_answers_tsv(question_id integer);
CREATE OR REPLACE FUNCTION get_dependent_answers_tsv(thread_id integer, language_code text)
RETURNS tsvector AS
$$
DECLARE
    query text;
    onerow record;
BEGIN
    query = 'SELECT concat_tsvectors(text_search_vector), count(*)' ||
       'FROM askbot_post WHERE post_type = ''answer'' AND thread_id = ' || thread_id ||
       ' AND deleted=false';
    FOR onerow IN EXECUTE query LOOP
        IF onerow.count = 0 THEN
            RETURN to_tsvector('');
        ELSE
            RETURN onerow.concat_tsvectors;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS thread_search_vector_update_trigger on askbot_thread;
DROP TRIGGER IF EXISTS thread_search_vector_insert_trigger on askbot_thread;
DROP TRIGGER IF EXISTS post_search_vector_update_trigger on askbot_post;

/* create tsvector columns in the content tables
 need to isolate these into own transactions, b/c of a weird mix
 of triggers/update and alter table statements
*/
SELECT add_tsvector_column('text_search_vector', 'askbot_thread');
COMMIT;
BEGIN;
SELECT add_tsvector_column('text_search_vector', 'askbot_post');
COMMIT;
BEGIN;
SELECT add_tsvector_column('title_search_vector', 'askbot_thread');
COMMIT;
BEGIN;

/* populate tsvectors with data */
-- post tsvectors
UPDATE askbot_post set text_search_vector = get_post_tsv(text, post_type, language_code) WHERE post_type IN ('answer', 'comment', 'question');
UPDATE askbot_post as q SET text_search_vector = text_search_vector ||
    get_dependent_comments_tsv(q.id) WHERE post_type IN ('question', 'answer');
--thread tsvector
UPDATE askbot_thread SET text_search_vector = get_thread_tsv(title, tagnames, language_code);
UPDATE askbot_thread as t SET text_search_vector = text_search_vector ||
    get_dependent_answers_tsv(t.id, t.language_code) ||
    get_thread_question_tsv(t.id, t.language_code);
UPDATE askbot_thread SET title_search_vector = get_thread_tsv(title, tagnames, language_code);

/* one trigger per table for tsv updates */

/* set up update triggers */
CREATE OR REPLACE FUNCTION thread_update_trigger() RETURNS trigger AS
$$
DECLARE
    title_tsv tsvector;
BEGIN
    title_tsv = get_thread_tsv(new.title, new.tagnames, new.language_code);
    new.title_search_vector = title_tsv;
    new.text_search_vector = title_tsv ||
                             get_thread_question_tsv(new.id, new.language_code) || 
                             get_dependent_answers_tsv(new.id, new.language_code);
    RETURN new;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER thread_search_vector_update_trigger 
BEFORE UPDATE ON askbot_thread FOR EACH ROW EXECUTE PROCEDURE thread_update_trigger();

CREATE OR REPLACE FUNCTION thread_insert_trigger() RETURNS trigger AS
$$
BEGIN
    new.text_search_vector = get_thread_tsv(new.title, new.tagnames, new.language_code);
    RETURN new;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER thread_search_vector_insert_trigger
BEFORE INSERT ON askbot_thread FOR EACH ROW EXECUTE PROCEDURE thread_insert_trigger();

/* post trigger */
CREATE OR REPLACE FUNCTION post_trigger() RETURNS trigger AS
$$
BEGIN
    IF new.post_type = 'question' THEN
        new.text_search_vector = get_post_tsv(new.text, 'question', new.language_code) ||
                                 get_dependent_comments_tsv(new.id);
    ELSIF new.post_type = 'answer' THEN
        new.text_search_vector = get_post_tsv(new.text, 'answer', new.language_code) ||
                                 get_dependent_comments_tsv(new.id);
    ELSIF new.post_type = 'comment' THEN
        new.text_search_vector = get_post_tsv(new.text, 'comment', new.language_code);
    END IF;
    UPDATE askbot_thread SET id=new.thread_id WHERE id=new.thread_id;
    return new;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER post_search_vector_update_trigger 
AFTER INSERT OR UPDATE ON askbot_post FOR EACH ROW EXECUTE PROCEDURE post_trigger();

COMMIT;
BEGIN;

DROP INDEX IF EXISTS askbot_search_idx;
CREATE INDEX askbot_search_idx ON askbot_thread USING gin(text_search_vector);
