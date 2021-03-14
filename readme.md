# Hack the North 2021 Backend Challenge

## Introduction
This repository holds a basic REST API server that stores and works with a hackathon's participant data. The server takes the data in hacker-data-2021.json and creates two tables to store the data, following a one-to-many relationship. The first database, **hackers**, stores each user's name, picture, company, email, and phone number. Through a foreign-key relationship, referencing **hackers'** rowid, it connects to the second database which stores **skills**, containing the names and ratings for each skill. The rowid is SQLite's default one, starting at 1 and autoincrementing. This is the ID that identifies each hacker and their associated skills.

## Getting Started
1. Clone this repository to your local directory
2. Run `export FLASK_APP=main.py` and then `flask run` 
3. The server will be running on port http://127.0.0.1:5000/

## API Usage 

#### All Users Endpoint
`GET localhost:5000/users/` will return all data, from both the **hackers** and **skills** tables, using an INNER JOIN.

#### User Information Endpoint
`GET localhost:5000/users/<id>` will return both hacker data and skill data for the hacker with the specified integer ID, using an INNER JOIN. 

#### Updating User Data Endpoint
`PUT localhost:5000/users/<id>`, given data in a JSON format, will return the updated user data as the response. This supports partial updating through first getting the original data and setting it as the default - any new information will replace its associated default information. 

#### Skills Endpoints


## Built With
Flask & SQLite, using REST principles. 

## Challenges & Takeaways 

When getting hacker data, each INNER JOIN only combines one hacker and one skill - that means if a hacker has two skills, the hacker data will be returned twice, once with each skill.

In updates, I am unsure if that is truly partial updating, because you are still sending back information for each of the sections, regardless of whether or not it was actually updated. Next steps would be to investigate this area and look for a more efficient approach. 
