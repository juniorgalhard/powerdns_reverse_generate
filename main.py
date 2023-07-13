import mysql.connector
from netaddr import IPNetwork
from mysql.connector import Error
import argparse
import datetime
import dotenv
import os

dotenv.find_dotenv()

dotenv.load_dotenv(dotenv.find_dotenv())

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')
DNS_NAME =  os.getenv('DNS_NAME')
NS1_HOSTNAME= os.getenv('NS1_HOSTNAME')
NS2_HOSTNAME=  os.getenv('NS2_HOSTNAME')

def insert_domain(domain_name, db):
    cursor = db.cursor()
    select_query = f"SELECT id FROM domains WHERE name = '{domain_name}'"
    cursor.execute(select_query)
    result = cursor.fetchone()
    if result:
        return result[0]
    insert_query = f"INSERT INTO domains (name, type) VALUES ('{domain_name}', 'NATIVE')"
    cursor.execute(insert_query)
    db.commit()
    return cursor.lastrowid

def create_common_records(domain_id, domain_name, db):
    cursor = db.cursor()
    current_time = datetime.datetime.now()
    current_serial = int(current_time.strftime("%Y%m%d%H"))
    record_data = [
        (domain_id, domain_name, 'SOA', f'{NS1_HOSTNAME} hostmaster.{DNS_NAME} {current_serial} 10800 3600 604800 3600', 86400),
        (domain_id, domain_name, 'NS', f'{NS1_HOSTNAME}', 86400),
        (domain_id, domain_name, 'NS', f'{NS2_HOSTNAME}', 86400)
    ]
    cursor.executemany("INSERT INTO records (domain_id, name, type, content, ttl, disabled, auth) VALUES (%s, %s, %s, %s, %s, 0, 1)", record_data)
    db.commit()

def create_records(cidr_block):
    db = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE)
    ip_net = IPNetwork(cidr_block)
    for ip in ip_net.iter_hosts():
        # Crie um domínio para cada /24 no bloco CIDR
        if ip.words[-1] == 1:
            reversed_ip_components = list(reversed(ip.words))
            domain_name = f"{reversed_ip_components[1]}.{reversed_ip_components[2]}.{reversed_ip_components[3]}.in-addr.arpa"
            domain_id = insert_domain(domain_name, db)
            create_common_records(domain_id, domain_name, db)
        record_name = f"{list(reversed(ip.words))[0]}.{domain_name}"
        content = f"{str(ip).replace('.', '-')}.cliente.{DNS_NAME}"
        cursor = db.cursor()
        # Verifique se o registro já existe
        select_query = f"SELECT id FROM records WHERE name = '{record_name}' AND type = 'PTR' ORDER BY id ASC"
        cursor.execute(select_query)
        records = cursor.fetchall()
        if records:
            # Se existir mais de um registro, remova todos exceto o com menor ID
            if len(records) > 1:
                for record in records[1:]:
                    cursor.execute(f"DELETE FROM records WHERE id = {record[0]}")
                    db.commit()
        else:
            insert_query = f"INSERT INTO records (domain_id, name, type, content, ttl, prio, disabled, auth) VALUES ({domain_id}, '{record_name}', 'PTR', '{content}', 60, 0, 0, 1)"
            cursor.execute(insert_query)
            db.commit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create reverse DNS records for a CIDR block.')
    parser.add_argument('cidr_block', type=str, help='The CIDR block for which to create records.')
    args = parser.parse_args()
    create_records(args.cidr_block)