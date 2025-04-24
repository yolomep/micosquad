import mysql.connector

# Try with hardcoded values first (use your actual password)
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Your actual password here
        database="flight_tracking",
        auth_plugin='mysql_native_password'
    )
    print("✅ Connection successful!")
    db.close()
except mysql.connector.Error as err:
    print(f"❌ Connection failed: {err}")