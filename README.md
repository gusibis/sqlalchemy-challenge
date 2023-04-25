# sqlalchemy-challenge
Analyze and Explore the Climate Data

Reflecting tables into SQLAlchemy ORM is creating classes that correspond to the tables in the database.
So we can use these classes to access the database using Python code instead of writing SQL queries.
The automap_base() function in SQLAlchemy can be used to reflect tables into classes. 
Once the tables are reflected, we can save use variables for each table to access them with python. 

In this project I used the reflection, creating a sqlalchemy and using automap_base(), Did not use classes as it was more complicated to make the queries. 
The challenge mentions globals and constants which I did see the need to use. 

I learned in class that it is a good practice to open and close the session in each function of the API setup that makes sense, however the template provided had
the session outside of the functions which I followed. 

Very challenging using the ORM model with sqlalchemy, will need lots of practice, however the reflection is more intuitive. 
I understand the ORM model would be much faster so it must be considered for a production environment. 

In the first part of the project I had the challenge to adjust the x-axis tickers to match the image provided in the assingment, which I could not emuate. 

See plots saved in the Resources folder. 