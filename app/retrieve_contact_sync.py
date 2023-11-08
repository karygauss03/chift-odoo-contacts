import odoorpc
import schedule
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from os import getenv
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')

def connect_db():
    try:
        conn = connect(
            dbname = getenv("DATABASE_NAME"), 
            user = getenv("DATABASE_USERNAME"), 
            host = getenv("DATABASE_HOSTNAME"), 
            password = getenv("DATABASE_PASSWORD")
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        print("I am unable to connect to the database - ", e)
  
def insert_update_delete(contacts, conn, cursor):
    try:
        cursor.execute("SELECT id FROM contacts")
        current_ids = {row[0] for row in cursor.fetchall()}
        retrieved_ids = {contact['id'] for contact in contacts}
        to_delete = current_ids - retrieved_ids
        if to_delete:
            sql_delete = "DELETE FROM contacts WHERE id = ANY(%s)"
            cursor.execute(sql_delete, (list(to_delete), ))
        
        contacts_to_sync = [(contact['id'], contact['name'], contact['email'], contact['name'], contact['email']) for contact in contacts if contact['id'] not in list(to_delete)]
        sql_insert_update = """
            INSERT INTO contacts(id, name, email) 
            VALUES (%s, %s, %s)
            ON CONFLICT (id) 
            DO UPDATE SET name = %s, email = %s;
            """
        cursor.executemany(sql_insert_update, contacts_to_sync)
        conn.commit()
        print("#####DONE#####")
    except Exception as e:
        print("Failed to insert, update or delete contact data - ", e)

def retrieve_odoo_contacts():
    odoo = odoorpc.ODOO('chift-employees.odoo.com', protocol='jsonrpc+ssl', port=443)
    odoo.login('chift-employees', 'karimomrane0@gmail.com', 'kary&gauss')
    contacts = odoo.env['res.partner'].search_read([], ['id', 'name', 'email'])
    contacts_list = [contact for contact in contacts if contact['email'] != False]
    insert_update_delete(contacts_list, conn, cursor)

conn, cursor = connect_db()

schedule.every(10).seconds.do(retrieve_odoo_contacts)

while True:
    schedule.run_pending()
