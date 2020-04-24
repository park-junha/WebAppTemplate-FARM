# Import this file into API codebase

# API internal status codes
API_CODES = {
    'SUCCESS_READ': 280
    , 'SUCCESS_WRITE': 281
    , 'ERROR_MYSQL_EXECUTE': 490
    , 'ERROR_DB_CONN_FAIL': 580
    , 'ERROR_EXECUTE_METHOD': 590
    , 'ERROR_BAD_SQL_TYPE': 591
}

if __name__ == '__main__':
    print(API_CODES)
