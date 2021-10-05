# Car Service Application with MongoEngine

This application is a simple program that demonstrates the power and capability of the [MongoEngine](http://mongoengine.org/) library for Python.

Run the test program, based on [TalkPython's MongoDB for Developers](https://training.talkpython.fm/courses/explore_mongodb_for_python_developers_course/mongodb-for-python-for-developers-featuring-orm-odm-mongoengine) Python Course, in this simple text-based Car Service Application.

## Setup

*Setup instructions for demoing application*

### Install MongoDB and Mongo Engine

Follow the [instructions](https://docs.mongodb.com/manual/administration/install-community/) from MongoDB's site.

Next, install MongoEngine

```bash
pip install -r requirements.txt
```

### Run Application

There are two driving applications:

- [Q&A](./q_and_a.py) - This automated program prints the time it takes to query mongo, use [this database](https://github.com/mikeckennedy/mongodb-for-python-developers/blob/master/data/dealership_db_250k.zip) to test this program
  - Unzip the file first
  - Next, restore the database: `mongorestore --drop --db dealership_example ./path/to/dealship`
  - Run `q_and_a.py` app
- [Service App](./service_app.py) - This is a menu-based system that allows you to perform CRUD operations on a mongo database
  - This prints reports based on selections
  - You can create cars, service them, find and list cars, and more... 

### Things to Try

- Try removing the indexes from the [data models](./data/models) objects and see how it affects performance in with the q_and_a.py file.
- Feel free to add onto the car_service.py file to experiment, there is a create_owner function that doesn't do anything, good place to write custom code to test your skills
