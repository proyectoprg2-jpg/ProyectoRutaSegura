import mysql.connector
from mysql.connector import Error

def test_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',  # Pon tu password aquí
            database='siniestros_viales'
        )
        
        if conn.is_connected():
            print(" Conexión exitosa a MySQL!")
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print("\n Tablas encontradas:")
            for table in tables:
                print(f"  - {table[0]}")
            cursor.close()
            conn.close()
        
    except Error as e:
        print(f" Error de conexión: {e}")

if __name__ == "__main__":
    test_connection()