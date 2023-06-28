# RESTful-web-API

# Prerequisites:

To run the code successfully, install several software’s. 

Python: Install Python from website (https://www.python.org) based on operating system.

Tornado: Tornado is a web framework for Python. You can install it using the following command pip install tornado.

MySQL database: Install mysql client in using Homebew. brew install mysql, which runs on 3306.

Redis: Install redis using Homebrew. brew install redis, which runs on port 6379.

SQL Workbench: Download the installer for your operating system and install

Please note that you'll also need to have Redis and MySQL installed and running on your system. Once you have installed the necessary components and have Redis and MySQL running, you should be able to run the provided code without any issues.

# How to run the code:

# Step 1: Create database Connection in SQL Workbench

•	Open SQL Workbench.

•	Click on "Open Connection" in the toolbar or go to "File" > "Open Connection Profile" to create a new connection.

•	Fill in the connection details:

                  Name: Provide a name for the connection profile.
                  
                  Driver: Select the MySQL driver from the drop-down menu.
                  
                  URL: Enter the connection URL, for example, jdbc: mysql://localhost:3306/guids.
                  
                  Username: Enter the MySQL username, such as root.
                  
                  Password: Enter the password associated with the MySQL user.
                  
•	Click "OK" to save the connection profile.

# Step 2: Create Database and Table

•	Database creation 
CREATE DATABASE guids;

•	Table creation
            CREATE TABLE guids.metadata (
            guid VARCHAR(32) PRIMARY KEY,
            expire INT,
            user VARCHAR(255));

•	Verify that the guids database and the metadata table have been created successfully.

# Step 3: Run the Python Code

•	Open an editor and paste the provided Python code into a new file (e.g., filename.py).

• Make sure you have the necessary Python dependencies installed.

•	Save the Python file.

•	Open a workbench terminal and navigate to the directory where the Python file is saved.

•	Run the Python script using the command python filename.py.

•	The Tornado application will start running and listening for requests on port 8000.

# Step 4: Test the Application with Postman

•	Open Postman or any other HTTP client tool.

•	Create a new request with the desired HTTP method (e.g., GET, POST, PUT, DELETE) and specify the URL based on the available routes in the Tornado application.

•	For example, to retrieve metadata for a specific GUID, use a GET request with a URL like http://localhost:8000/guid/1234567890ABCDEF, where 1234567890ABCDEF is a valid GUID.

•	To create a new metadata entry, use a POST request with the URL http://localhost:8000/guid and provide the required data in the request body as JSON.

•	Similarly, you can test the PUT and DELETE methods by providing the appropriate GUID in the URL and the required data in the request body.

•	Send the request and observe the response in Postman.

By following these steps, you can implement the provided code in SQL Workbench and test the functionality using Postman. You can create, retrieve, update, and delete metadata entries in the MySQL database and interact with the Tornado application via the defined route

