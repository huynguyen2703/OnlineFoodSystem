# -----------------------------------------------SETUP SECTION----------------------------------------------------------


# Required libraries to connect and control MySQL database with Python
from flask import Flask, render_template, url_for, redirect
from flask import request
import os
import mysql.connector
from mysql.connector import errorcode
import sqlparse
import requests
import logging
import re

# Create flask application to manage routes
app = Flask(__name__)

# Define database configurations to connect to MySQL database
server_name = os.environ['SERVER_NAME']
username = os.environ['USER_NAME']
password = os.environ['PASSWORD']
db_name = os.environ['DB_NAME']

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
        connection = mysql.connector.connect(
            host=server_name,
            user=username,
            password=password,
            database=db_name)

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

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return []
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Our main page
@app.route('/food_online_system.html')
def landing_page():
    return render_template("https://css1.seattleu.edu/~hnguyen37/templates/food_online_system.html")


# -----------------------------------------------DISPLAY ENTITIES SECTION-----------------------------------------------

# Display restaurant table
@app.route('/restaurants.html')
def restaurants():
    query = 'SELECT * FROM RESTAURANTS;'
    restaurants_columns, restaurants_table = reusable(query)
    return render_template("https://css1.seattleu.edu/~hnguyen37/templates/restaurants.html", restaurants=restaurants_table, columns=restaurants_columns)


# Display shippers table
@app.route('/shippers.html')
def shippers():
    query = 'SELECT * FROM SHIPPERS;'
    shippers_columns, shippers_table = reusable(query)

    html = "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Shippers Table</title><link rel='stylesheet' href='https://css1.seattleu.edu/~hnguyen37/static/tables.css'></head><body>"
    html += "<section><h1>Food Online System</h1><div class='table-container'><table class='table-center'>"

    # Add table headers (columns)
    html += "<thead><tr>"
    for column in shippers_columns:
        html += f"<th>{column}</th>"
    html += "</tr></thead><tbody>"

    # Add table rows (restaurant data)
    for shipper in shippers_table:
        html += "<tr>"
        for data in shipper:
            html += f"<td>{data if data is not None else 'N/A'}</td>"
        html += "</tr>"

    html += "</tbody></table></div></section></body></html>"

    # Return the generated HTML response
    return html
    # return render_template("shippers.html", shippers=shippers_table, columns=shippers_columns)


# Display customers table
@app.route('/customers.html')
def customers():
    query = 'SELECT * FROM CUSTOMERS;'
    customers_columns, customers_table = reusable(query)

    html = "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Customers Table</title><link rel='stylesheet' href='https://css1.seattleu.edu/~hnguyen37/static/tables.css'></head><body>"
    html += "<section><h1>Food Online System</h1><div class='table-container'><table class='table-center'>"

    # Add table headers (columns)
    html += "<thead><tr>"
    for column in customers_columns:
        html += f"<th>{column}</th>"
    html += "</tr></thead><tbody>"

    # Add table rows (restaurant data)
    for customer in customers_table:
        html += "<tr>"
        for data in customer:
            html += f"<td>{data if data is not None else 'N/A'}</td>"
        html += "</tr>"

    html += "</tbody></table></div></section></body></html>"

    # Return the generated HTML response
    return html
    #return render_template("customers.html", customers=customers_table, columns=customers_columns)


# Display delivery addresses table
@app.route('/delivery_addresses.html')
def delivery_addresses():
    query = 'SELECT * FROM DELIVERY_ADDRESSES;'
    delivery_addresses_columns, delivery_addresses_table = reusable(query)

    html = "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Delivery Addresses Table</title><link rel='stylesheet' href='https://css1.seattleu.edu/~hnguyen37/static/tables.css'></head><body>"
    html += "<section><h1>Food Online System</h1><div class='table-container'><table class='table-center'>"

    # Add table headers (columns)
    html += "<thead><tr>"
    for column in delivery_addresses_columns:
        html += f"<th>{column}</th>"
    html += "</tr></thead><tbody>"

    # Add table rows (restaurant data)
    for delivery_address in delivery_addresses_table:
        html += "<tr>"
        for data in delivery_address:
            html += f"<td>{data if data is not None else 'N/A'}</td>"
        html += "</tr>"

    html += "</tbody></table></div></section></body></html>"

    # Return the generated HTML response
    return html


    #return render_template("delivery_addresses.html", delivery_addresses=delivery_addresses_table,
    #                       columns=delivery_addresses_columns)


# Display customer addresses table
@app.route('/customer_addresses.html')
def customer_addresses():
    query = 'SELECT * FROM CUSTOMER_ADDRESSES;'
    customer_addresses_columns, customer_addresses_table = reusable(query)

    html = "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Customer Addresses Table</title><link rel='stylesheet' href='https://css1.seattleu.edu/~hnguyen37/static/tables.css'></head><body>"
    html += "<section><h1>Food Online System</h1><div class='table-container'><table class='table-center'>"

    # Add table headers (columns)
    html += "<thead><tr>"
    for column in customer_addresses_columns:
        html += f"<th>{column}</th>"
    html += "</tr></thead><tbody>"

    # Add table rows (restaurant data)
    for customer_address in customer_addresses_table:
        html += "<tr>"
        for data in customer_address:
            html += f"<td>{data if data is not None else 'N/A'}</td>"
        html += "</tr>"

    html += "</tbody></table></div></section></body></html>"

    # Return the generated HTML response
    return html
    # return render_template("customer_addresses.html", customer_addresses=customer_addresses_table,
    #                        columns=customer_addresses_columns)


# Display orders table
@app.route('/orders.html')
def orders():
    query = 'SELECT * FROM ORDERS;'
    orders_columns, orders_table = reusable(query)

    html = "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Shippers Table</title><link rel='stylesheet' href='https://css1.seattleu.edu/~hnguyen37/static/tables.css'></head><body>"
    html += "<section><h1>Food Online System</h1><div class='table-container'><table class='table-center'>"

    # Add table headers (columns)
    html += "<thead><tr>"
    for column in orders_columns:
        html += f"<th>{column}</th>"
    html += "</tr></thead><tbody>"

    # Add table rows (restaurant data)
    for order in orders_table:
        html += "<tr>"
        for data in order:
            html += f"<td>{data if data is not None else 'N/A'}</td>"
        html += "</tr>"

    html += "</tbody></table></div></section></body></html>"

    # Return the generated HTML response
    return html
    # return render_template("orders.html", orders=orders_table,
    #                        columns=orders_columns)


# -----------------------------------------------DISPLAY QUERIES SECTION------------------------------------------------


# Display query one table
@app.route('/query_one.html')
def query_one():
    query = "SELECT * FROM CUSTOMERS NATURAL JOIN ORDERS;"
    query_one_columns, query_one_table = reusable(query)

    html = "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Query One Table</title><link rel='stylesheet' href='https://css1.seattleu.edu/~hnguyen37/static/tables.css'></head><body>"
    html += "<section><h1>Food Online System</h1><div class='table-container'><table class='table-center' id='query-one'>"

    # Add table headers (columns)
    html += "<thead><tr>"
    for column in query_one_columns:
        html += f"<th>{column}</th>"
    html += "</tr></thead><tbody>"

    # Add table rows (restaurant data)
    for query_row in query_one_table:
        html += "<tr>"
        for data in query_row:
            html += f"<td>{data if data is not None else 'N/A'}</td>"
        html += "</tr>"

    html += "</tbody></table></div></section></body></html>"

    # Return the generated HTML response
    return html
    # return render_template("query_one.html", query_one=query_one_table,
    #                        columns=query_one_columns)


# Display query two table
@app.route('/query_two.html')
def query_two():
    query = """SELECT CUSTOMER_ID, SUM(ORDER_PRICE) AS 'TOTAL_PRICE', COUNT(ORDER_ID) AS 
               'TOTAL_ORDERS' FROM ORDERS GROUP BY CUSTOMER_ID;"""
    query_two_columns, query_two_table = reusable(query)

    html = "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Query Two Table</title><link rel='stylesheet' href='https://css1.seattleu.edu/~hnguyen37/static/tables.css'></head><body>"
    html += "<section><h1>Food Online System</h1><div class='table-container'><table class='table-center'>"

    # Add table headers (columns)
    html += "<thead><tr>"
    for column in query_two_columns:
        html += f"<th>{column}</th>"
    html += "</tr></thead><tbody>"

    # Add table rows (restaurant data)
    for query_row in query_two_table:
        html += "<tr>"
        for data in query_row:
            html += f"<td>{data if data is not None else 'N/A'}</td>"
        html += "</tr>"

    html += "</tbody></table></div></section></body></html>"

    # Return the generated HTML response
    return html
    # return render_template("query_two.html", query_two=query_two_table,
    #                        columns=query_two_columns)


# Display query three
@app.route('/query_three.html')
def query_three():
    query = "SELECT * FROM ORDERS WHERE ORDER_PRICE > (SELECT AVG(ORDER_PRICE) FROM ORDERS);"
    query_three_columns, query_three_table = reusable(query)

    html = "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Query Three Table</title><link rel='stylesheet' href='https://css1.seattleu.edu/~hnguyen37/static/tables.css'></head><body>"
    html += "<section><h1>Food Online System</h1><div class='table-container'><table class='table-center'>"

    # Add table headers (columns)
    html += "<thead><tr>"
    for column in query_three_columns:
        html += f"<th>{column}</th>"
    html += "</tr></thead><tbody>"

    # Add table rows (restaurant data)
    for query_row in query_three_table:
        html += "<tr>"
        for data in query_row:
            html += f"<td>{data if data is not None else 'N/A'}</td>"
        html += "</tr>"

    html += "</tbody></table></div></section></body></html>"

    # Return the generated HTML response
    return html
    # return render_template("query_three.html", query_three=query_three_table,
    #                        columns=query_three_columns)


# Display query four table
@app.route('/query_four.html')
def query_four():
    query = """SELECT RESTAURANTS.RESTAURANT_NUM, RESTAURANTS.RESTAURANT_NAME, AVG(RATING) AS 
    'AVERAGE_RATING' FROM ORDERS JOIN RESTAURANTS ON 
    ORDERS.RESTAURANT_NUM = RESTAURANTS.RESTAURANT_NUM GROUP BY RESTAURANTS.RESTAURANT_NUM,RESTAURANTS.RESTAURANT_NAME
    HAVING COUNT(ORDERS.ORDER_ID) > 5;"""
    query_four_columns, query_four_table = reusable(query)

    html = "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Query One Table</title><link rel='stylesheet' href='https://css1.seattleu.edu/~hnguyen37/static/tables.css'></head><body>"
    html += "<section><h1>Food Online System</h1><div class='table-container'><table class='table-center' id='query-one'>"

    # Add table headers (columns)
    html += "<thead><tr>"
    for column in query_four_columns:
        html += f"<th>{column}</th>"
    html += "</tr></thead><tbody>"

    # Add table rows (restaurant data)
    for query_row in query_four_table:
        html += "<tr>"
        for data in query_row:
            html += f"<td>{data if data is not None else 'N/A'}</td>"
        html += "</tr>"

    html += "</tbody></table></div></section></body></html>"

    # Return the generated HTML response
    return html
    # return render_template("query_four.html", query_four=query_four_table,
    #                        columns=query_four_columns)


# Display query five table
@app.route('/query_five.html')
def query_five():
    query = """SELECT CUSTOMERS.CUSTOMER_ID, CUSTOMERS.CUSTOMER_FNAME, CUSTOMERS.CUSTOMER_LNAME,
               DELIVERY_ADDRESSES.DELIVERY_ADDRESS_NUM, DELIVERY_ADDRESSES.STREET_ADDRESS, 
               DELIVERY_ADDRESSES.CITY, DELIVERY_ADDRESSES.STATE, DELIVERY_ADDRESSES.ZIP_CODE, 
               DELIVERY_ADDRESSES.LOCATION_INSTRUCTIONS
               FROM CUSTOMERS LEFT JOIN CUSTOMER_ADDRESSES ON CUSTOMERS.CUSTOMER_ID = CUSTOMER_ADDRESSES.CUSTOMER_ID
               LEFT JOIN DELIVERY_ADDRESSES ON 
               CUSTOMER_ADDRESSES.DELIVERY_ADDRESS_NUM = DELIVERY_ADDRESSES.DELIVERY_ADDRESS_NUM;"""
    query_five_columns, query_five_table = reusable(query)

    html = "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Query Five Table</title><link rel='stylesheet' href='https://css1.seattleu.edu/~hnguyen37/static/tables.css'></head><body>"
    html += "<section><h1>Food Online System</h1><div class='table-container'><table class='table-center'>"

    # Add table headers (columns)
    html += "<thead><tr>"
    for column in query_five_columns:
        html += f"<th>{column}</th>"
    html += "</tr></thead><tbody>"

    # Add table rows (restaurant data)
    for query_row in query_five_table:
        html += "<tr>"
        for data in query_row:
            html += f"<td>{data if data is not None else 'N/A'}</td>"
        html += "</tr>"

    html += "</tbody></table></div></section></body></html>"

    # Return the generated HTML response
    return html
    # return render_template("query_five.html", query_five=query_five_table,
    #                        columns=query_five_columns)


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
            return False

        # Step 3: Parse the cleaned query using sqlparse
        parsed_query = sqlparse.parse(query)

        # Step 4: Check if the parsed query has valid tokens
        if not parsed_query or not parsed_query[0].tokens:
            return False

        # Step 5: Define the valid SQL keywords
        sql_keywords = ['SELECT', 'INSERT', 'CREATE', 'UPDATE', 'DELETE', 'DROP']

        # Step 6: Get the first meaningful token (strip out irrelevant tokens)
        # Skip any non-SQL tokens such as whitespaces
        for token in parsed_query[0].tokens:
            if token.value.strip():  # First non-empty token
                first_token = token
                break
        else:
            return False  # No valid tokens found

        # Step 7: Check if the first token is one of the valid SQL keywords (case-insensitive)
        if first_token.value.strip().upper() not in sql_keywords:
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

        if not validate_query(user_query):
            error_message = "Invalid SQL query. Please try again."
        else:
            try:
                if user_query.upper().startswith('SELECT'):
                    columns, results = reusable(user_query)
                else:
                    reusable(user_query)
                success_message = "Query executed successfully"
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"

    html = "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Adhoc Query</title><link rel='stylesheet' href='https://css1.seattleu.edu/~hnguyen37/static/tables.css'></head><body>"
    html += "<section><h1>Food Online System</h1>"

    # Display an error message if any
    if error_message != "":
        html += f"<div class='failed-message'>Error: {error_message}</div>"

    # Display a success message if any
    if success_message != "":
        html += f"<div class='success-message'>{success_message}</div>"

    # Display query results in a table if available
    if columns and results:
        html += "<div class='table-container'><table class='table-center'><thead><tr>"
        # Table header (columns)
        for column in columns:
            html += f"<th>{column}</th>"
        html += "</tr></thead><tbody>"

        # Table body (query results)
        for query_row in results:
            html += "<tr>"
            for query_column in query_row:
                html += f"<td>{query_column if query_column is not None else 'N/A'}</td>"
            html += "</tr>"
        html += "</tbody></table></div>"

    html += "</section></body></html>"

    # Return the dynamically generated HTML
    return html

    # return render_template("adhoc.html", columns=columns, adhoc_query=results, success=success_message, error=error_message)


# ----------------------------------------------------------------------------------------------------------------------

# Run flask application
if __name__ == "__main__":
    app.run(debug=False)
