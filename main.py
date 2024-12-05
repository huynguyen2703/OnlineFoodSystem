# -----------------------------------------------SETUP SECTION----------------------------------------------------------


# Required libraries to connect and control MySQL database with Python
from flask import Flask, render_template, url_for, redirect
from flask import request
import os
import sqlite3
import sqlparse
import requests
import logging
import re

# Create flask application to manage routes
app = Flask(__name__)


# Define database configurations to connect to MySQL database
# server_name = os.environ['SERVER_NAME']
# username = os.environ['USER_NAME']
# password = os.environ['PASSWORD']
# db_name = os.environ['DB_NAME']

# server_name = '127.0.0.1'
# username = 'root'
# password = os.environ['MY_PASSWORD']
# db_name = os.environ['MY_DB']


# -----------------------------------------------FUNCTIONALITIES SECTION------------------------------------------------


# select function created for reusable purpose
def reusable(query: str):
    """
        Executes a SELECT query and returns the results.
        :param query: The SELECT SQL query as a string.
        :return: List of tuples containing the query results.
    """
    connection = None
    cursor = None
    try:
        connection = sqlite3.connect('food_online_system.db')

        print("Connected Successfully")

        cursor = connection.cursor()

        cursor.execute(query)

        if query.strip().upper().startswith('SELECT'):
            columns = [column[0] for column in cursor.description]

            results = cursor.fetchall()

            return columns, results
        else:
            connection.commit()
            return cursor.rowcount
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Our main page
@app.route('/')
def landing_page():
    return render_template("food_online_system.html")


# -----------------------------------------------DISPLAY ENTITIES SECTION-----------------------------------------------

# Display restaurant table
@app.route('/restaurants.html')
def restaurants():
    query = 'SELECT * FROM RESTAURANTS;'
    restaurants_columns, restaurants_table = reusable(query)
    return render_template("restaurants.html", restaurants=restaurants_table, columns=restaurants_columns)


# Display shippers table
@app.route('/shippers.html')
def shippers():
    query = 'SELECT * FROM SHIPPERS;'
    shippers_columns, shippers_table = reusable(query)
    return render_template("shippers.html", shippers=shippers_table, columns=shippers_columns)


# Display customers table
@app.route('/customers.html')
def customers():
    query = 'SELECT * FROM CUSTOMERS;'
    customers_columns, customers_table = reusable(query)

    return render_template("customers.html", customers=customers_table, columns=customers_columns)


# Display delivery addresses table
@app.route('/delivery_addresses.html')
def delivery_addresses():
    query = 'SELECT * FROM DELIVERY_ADDRESSES;'
    delivery_addresses_columns, delivery_addresses_table = reusable(query)
    return render_template("delivery_addresses.html", delivery_addresses=delivery_addresses_table,
                           columns=delivery_addresses_columns)


# Display customer addresses table
@app.route('/customer_addresses.html')
def customer_addresses():
    query = 'SELECT * FROM CUSTOMER_ADDRESSES;'
    customer_addresses_columns, customer_addresses_table = reusable(query)
    return render_template("customer_addresses.html", customer_addresses=customer_addresses_table,
                           columns=customer_addresses_columns)


# Display orders table
@app.route('/orders.html')
def orders():
    query = 'SELECT * FROM ORDERS;'
    orders_columns, orders_table = reusable(query)
    return render_template("orders.html", orders=orders_table,
                           columns=orders_columns)


# -----------------------------------------------DISPLAY QUERIES SECTION------------------------------------------------


# Display query one table
@app.route('/query_one.html')
def query_one():
    query = "SELECT * FROM CUSTOMERS INNER JOIN ORDERS ON CUSTOMERS.CUSTOMER_ID = ORDERS.CUSTOMER_ID;"
    query_one_columns, query_one_table = reusable(query)
    return render_template("query_one.html", query_one=query_one_table,
                           columns=query_one_columns)


# Display query two table
@app.route('/query_two.html')
def query_two():
    query = """SELECT CUSTOMER_ID, SUM(ORDER_PRICE) AS 'TOTAL_PRICE', COUNT(ORDER_ID) AS 'TOTAL_ORDERS' FROM ORDERS
               GROUP BY CUSTOMER_ID;"""
    query_two_columns, query_two_table = reusable(query)
    return render_template("query_two.html", query_two=query_two_table,
                           columns=query_two_columns)


# Display query three
@app.route('/query_three.html')
def query_three():
    query = "SELECT * FROM ORDERS WHERE ORDER_PRICE > (SELECT AVG(ORDER_PRICE) FROM ORDERS)ORDER BY ORDER_PRICE DESC;"
    query_three_columns, query_three_table = reusable(query)
    return render_template("query_three.html", query_three=query_three_table,
                           columns=query_three_columns)


# Display query four table
@app.route('/query_four.html')
def query_four():
    query = """SELECT RESTAURANTS.RESTAURANT_NUM, RESTAURANTS.RESTAURANT_NAME, AVG(RATING) AS 'AVERAGE_RATING' 
               FROM ORDERS
               JOIN RESTAURANTS ON ORDERS.RESTAURANT_NUM = RESTAURANTS.RESTAURANT_NUM
               GROUP BY RESTAURANTS.RESTAURANT_NUM, RESTAURANTS.RESTAURANT_NAME
               HAVING COUNT(ORDERS.ORDER_ID) > 5;"""
    query_four_columns, query_four_table = reusable(query)
    return render_template("query_four.html", query_four=query_four_table,
                           columns=query_four_columns)


# Display query five table
@app.route('/query_five.html')
def query_five():
    query = """SELECT CUSTOMERS.CUSTOMER_ID, CUSTOMERS.CUSTOMER_FNAME, CUSTOMERS.CUSTOMER_LNAME,
               DELIVERY_ADDRESSES.DELIVERY_ADDRESS_NUM, DELIVERY_ADDRESSES.STREET_ADDRESS, 
               DELIVERY_ADDRESSES.CITY, DELIVERY_ADDRESSES.STATE, DELIVERY_ADDRESSES.ZIP_CODE, 
               DELIVERY_ADDRESSES.LOCATION_INSTRUCTIONS
               FROM CUSTOMERS
               LEFT JOIN CUSTOMER_ADDRESSES ON CUSTOMERS.CUSTOMER_ID = CUSTOMER_ADDRESSES.CUSTOMER_ID
               LEFT JOIN DELIVERY_ADDRESSES ON CUSTOMER_ADDRESSES.DELIVERY_ADDRESS_NUM = DELIVERY_ADDRESSES.DELIVERY_ADDRESS_NUM;"""
    query_five_columns, query_five_table = reusable(query)
    return render_template("query_five.html", query_five=query_five_table,
                           columns=query_five_columns)


# --------------------------------------------------AD_HOC QUERY SECTION------------------------------------------------

def validate_query(query: str) -> bool:
    try:
        # Step 1: Remove single-line and multi-line comments
        query = query.strip()  # Remove leading/trailing spaces
        query = re.sub(r'--.*$', '', query, flags=re.MULTILINE)  # Remove single-line comments
        query = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)  # Remove multi-line comments

        query = query.strip()  # Strip spaces again after comment removal

        # Step 2: Check if the query is empty after cleaning
        if not query:
            logging.error("Query is empty after comment removal.")
            return False

        # Step 3: Parse the cleaned query using sqlparse
        parsed_query = sqlparse.parse(query)

        # Step 4: Check if the parsed query has valid tokens
        if not parsed_query or not parsed_query[0].tokens:
            logging.error("No valid tokens found after parsing the query.")
            return False

        # Step 5: Define the valid SQL keywords (common to SQLite)
        sql_keywords = ['SELECT', 'INSERT', 'CREATE', 'UPDATE', 'DELETE', 'DROP', 'ALTER']

        # Step 6: Get the first meaningful token (strip out irrelevant tokens)
        for token in parsed_query[0].tokens:
            if token.value.strip():  # First non-empty token
                first_token = token
                break
        else:
            logging.error("No valid tokens found in query.")
            return False  # No valid tokens found

        # Step 7: Check if the first token is one of the valid SQL keywords (case-insensitive)
        if first_token.value.strip().upper() not in sql_keywords:
            logging.error(f"First token '{first_token.value.strip()}' is not a valid SQL keyword.")
            return False

        return True

    except sqlparse.exceptions.SQLParseError as e:
        logging.error(f"SQLParseError: {e}")
        return False
    except IndexError as e:
        logging.error(f"IndexError: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return False


@app.route('/adhoc.html', methods=['GET', 'POST'])
def submit_query():
    error_message = None
    success_message = None
    columns = []
    results = []

    if request.method == 'POST':
        user_input = request.form['user_input']
        user_query = user_input.strip()

        # Validate SQL query
        if not validate_query(user_query):
            error_message = "Invalid SQL query. Please try again."
        else:
            try:
                if user_query.upper().startswith('SELECT'):
                    # Handle SELECT query by fetching columns and results
                    columns, results = reusable(user_query)
                else:
                    # Execute non-SELECT queries (no need to store columns/results)
                    reusable(user_query)
                    success_message = "Query executed successfully"

            except Exception as e:
                # Catch specific errors (e.g., database errors, SQL errors)
                logging.error(f"Error executing query: {str(e)}")
                error_message = f"An error occurred: {str(e)}"

    return render_template("adhoc.html", columns=columns, adhoc_query=results, success=success_message,
                           error=error_message)


# ----------------------------------------------------------------------------------------------------------------------

# Run flask application
if __name__ == "__main__":
    app.run(debug=False)
