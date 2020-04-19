# ======================================= #
# MAKE SURE THIS FILE DOES NOT GET PUSHED #
# ======================================= #

# Set the following fields to your database's credentials
db_credentials = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'schema': 'SampleInventory',
    'charset': 'utf8mb4',
    'password': None
}

if __name__ == '__main__':
    print(db_credentials)
