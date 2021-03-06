from db import DatabaseCursor
from flask import current_app
import psycopg2

# This script contains all queries for the tag table


def get_all_tags():
    with DatabaseCursor() as cursor:
        cursor.execute('SELECT * FROM tag;')
        return cursor.fetchall()


def get_tag_by_id(tag_id):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting tag with tag ID {} from database".format(tag_id))
        cursor.execute('select * from tag where tag_id = %s;', (tag_id,))
        return cursor.fetchone()


def insert_tag(name):
    try:
        with DatabaseCursor() as cursor:
            cursor.execute('INSERT INTO tag VALUES(DEFAULT, %s);', name)
            current_app.logger.info("Tag added to database: [{}]"
                                    .format(name))
            return True
    except psycopg2.IntegrityError:
        current_app.logger.error("INSERTION FAILED: [{}]".format(name))
        return False


def update_tag(tag_id, name):
    try:
        with DatabaseCursor() as cursor:
            cursor.execute('UPDATE tag SET name = %s'
                           'where tag_id = %s;',
                           (name, tag_id))
            current_app.logger.info("Tag {} updated: [{}]"
                                    .format(tag_id, name))
            return True
    except psycopg2.Error:
        current_app.logger.error("UPDATE FAILED: [{}, {}]".format(tag_id, name))
        return False


def delete_tag(tag_id):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Deleting tag {} from database".format(tag_id))
        cursor.execute("delete from tag where tag_id = %s", tag_id)



def insert_listing_tag(tag_id, listing_name, owner_id):
    try:
        with DatabaseCursor() as cursor:
            cursor.execute('INSERT INTO listing_tag VALUES(%s, %s, %s);', (tag_id, listing_name, owner_id))
            return True
    except psycopg2.IntegrityError:
        current_app.logger.error("listing_tag insertion failed: [{}]".format(listing_name))
        return False


def get_most_common_tag_of_owner(owner_name):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting most common tag name of owner name {} from database".format(owner_name))
        cursor.execute("SELECT tag.name AS tag_name, COUNT(lt.tag_id) AS count FROM listing_tag lt "
                       "LEFT JOIN tag AS tag ON lt.tag_id = tag.tag_id "
                       "WHERE lt.owner_id = (SELECT u.id FROM users u WHERE u.username = %s) "
                       "GROUP BY tag.name ORDER BY count DESC LIMIT 1;",
                       (owner_name,))
        return cursor.fetchone()


def get_tagids_under_listing(listing_name, owner_id):
    with DatabaseCursor() as cursor:
        sql = ('''select tag_id, listing_name, owner_id from listing_tag group by listing_name, tag_id, owner_id
                  having listing_name like '%{}%' and owner_id = {}''').format(listing_name, owner_id)
        cursor.execute(sql)
        return cursor.fetchall()


def delete_listing_tags(listing_name, owner_id):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Deleting tags for listing '{}' from listing_tag table.".format(listing_name))
        cursor.execute('delete from listing_tag where listing_name = %s and owner_id = %s', (listing_name, owner_id))
