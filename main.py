# -----------------------------------------------SETUP SECTION----------------------------------------------------------


# Required libraries to connect and control MySQL database with Python
from flask import Flask, render_template, url_for, redirect
from flask import request
import os
import mysql.connector

# Create flask application to manage routes
app = Flask(__name__)

# Define database configurations to connect to MySQL database
server_name = your_server
username = your_username
password = your_password
db_name = your_db_name


# -----------------------------------------------FUNCTIONALITIES SECTION------------------------------------------------


# select function created for reusable purpose
def select(query: str, params=None):
    """
        Executes a SELECT query and returns the results.
        :param query: The SELECT SQL query as a string.
        :param params: Optional tuple of parameters for the query.
        :return: List of tuples containing the query results.
    """
    try:
        connection = mysql.connector.connect(
            host=server_name,
            user=username,
            password=password,
            database=db_name)

        print("Connected Successfully")

        cursor = connection.cursor()

        cursor.execute(query)

        columns = [column[0] for column in cursor.description]

        results = cursor.fetchall()

        return columns, results

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
@app.route('/')
def landing_page():
    return render_template("FoodOnlineSystem.htm")


# -----------------------------------------------DISPLAY ENTITIES SECTION-----------------------------------------------

# Display restaurant table
@app.route('/restaurants.html')
def restaurants():
    query = 'SELECT * FROM RESTAURANTS;'
    restaurants_columns, restaurants_table = select(query)
    return render_template("restaurants.html", restaurants=restaurants_table, columns=restaurants_columns)


# Display shippers table
@app.route('/shippers.html')
def shippers():
    query = 'SELECT * FROM SHIPPERS;'
    shippers_columns, shippers_table = select(query)
    return render_template("shippers.html", shippers=shippers_table, columns=shippers_columns)


# Display customers table
@app.route('/customers.html')
def customers():
    query = 'SELECT * FROM CUSTOMERS;'
    customers_columns, customers_table = select(query)
    return render_template("customers.html", customers=customers_table, columns=customers_columns)


# Display delivery addresses table
@app.route('/delivery_addresses.html')
def delivery_addresses():
    query = 'SELECT * FROM DELIVERY_ADDRESSES;'
    delivery_addresses_columns, delivery_addresses_table = select(query)
    return render_template("delivery_addresses.html", delivery_addresses=delivery_addresses_table,
                           columns=delivery_addresses_columns)


# Display customer addresses table
@app.route('/customer_addresses.html')
def customer_addresses():
    query = 'SELECT * FROM CUSTOMER_ADDRESSES;'
    customer_addresses_columns, customer_addresses_table = select(query)
    return render_template("customer_addresses.html", customer_addresses=customer_addresses_table,
                           columns=customer_addresses_columns)


# Display orders table
@app.route('/orders.html')
def orders():
    query = 'SELECT * FROM ORDERS;'
    orders_columns, orders_table = select(query)
    return render_template("orders.html", orders=orders_table,
                           columns=orders_columns)


# -----------------------------------------------DISPLAY QUERIES SECTION------------------------------------------------


# Display query one table
@app.route('/query_one.html')
def query_one():
    query = "SELECT * FROM CUSTOMERS NATURAL JOIN ORDERS;"
    query_one_columns, query_one_table = select(query)
    return render_template("query_one.html", query_one=query_one_table,
                           columns=query_one_columns)


# Display query two table
@app.route('/query_two.html')
def query_two():
    query = """SELECT CUSTOMER_ID, SUM(ORDER_PRICE) AS 'TOTAL_PRICE', COUNT(ORDER_ID) AS 
               'TOTAL_ORDERS' FROM ORDERS GROUP BY CUSTOMER_ID;"""
    query_two_columns, query_two_table = select(query)
    return render_template("query_two.html", query_two=query_two_table,
                           columns=query_two_columns)


# Display query three
@app.route('/query_three.html')
def query_three():
    query = "SELECT * FROM ORDERS WHERE ORDER_PRICE > (SELECT AVG(ORDER_PRICE) FROM ORDERS);"
    query_three_columns, query_three_table = select(query)
    return render_template("query_three.html", query_three=query_three_table,
                           columns=query_three_columns)


# Display query four table
@app.route('/query_four.html')
def query_four():
    query = """SELECT RESTAURANTS.RESTAURANT_NUM, RESTAURANTS.RESTAURANT_NAME, AVG(RATING) AS 
    'AVERAGE_RATING' FROM ORDERS JOIN RESTAURANTS ON 
    ORDERS.RESTAURANT_NUM = RESTAURANTS.RESTAURANT_NUM GROUP BY RESTAURANTS.RESTAURANT_NUM,RESTAURANTS.RESTAURANT_NAME
    HAVING COUNT(ORDERS.ORDER_ID) > 5;"""
    query_four_columns, query_four_table = select(query)
    return render_template("query_four.html", query_four=query_four_table,
                           columns=query_four_columns)


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
    query_five_columns, query_five_table = select(query)
    return render_template("query_five.html", query_five=query_five_table,
                           columns=query_five_columns)


# -----------------------------------------------------------------------------------------------------------------------
# Run flask application
if __name__ == "__main__":
    app.run(debug=False)
