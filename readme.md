# Hack the North 2021 Backend Challenge

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#introduction">Introduction</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
    <li>
        <a href="#API-usage">API Usage</a>
        <ul>
            <li><a href="#all-users-endpoint">All Users Endpoint</a></li>
            <li><a href="#user-information-endpoint">User Information Endpoint</a></li>
            <li><a href="#updating-user-data-endpoint">Updating User Data Endpoint</a></li>
            <li><a href="#skills-endpoint">Skills Endpoint</a></li>
        </ul> 
    </li>
    <li><a href="#challenges-and-takeaways">Challenges and Takeaways</a></li>
  </ol>
</details>

## Introduction
This repository holds a basic REST API server that stores and works with a hackathon's participant data. 

The server takes the data in hacker-data-2021.json and creates two tables to store the data, following a one-to-many relationship. The first database, **hackers**, stores each user's name, picture, company, email, and phone number. Through a foreign-key relationship, referencing **hackers'** rowid, it connects to the second database which stores **skills**, containing the names and ratings for each skill. The rowid is SQLite's default one, starting at 1 and autoincrementing. This is the ID that identifies each hacker and their associated skills.

The two tables are structured as follow:

```sql
CREATE TABLE hackers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    picture TEXT, 
    company TEXT,
    email TEXT,
    phone TEXT 
)
```

```sql
CREATE TABLE skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hacker_id INTEGER,
    name TEXT,
    rating INTEGER,
    FOREIGN KEY (hacker_id) REFERENCES hackers (id)
)
```

#### Built With
1. Flask 
2. SQLite
3. Python json package

Designed with REST principles. 
Used standard documentation & articles as references; used Postman to test requests.  

## Getting Started
1. Clone this repository to your local directory
2. Run `python main.py` 
3. The server will be running on port http://127.0.0.1:5000/




## API Usage 

#### All Users Endpoint
`GET http://127.0.0.1:5000/users/` will return all data, from both the **hackers** and **skills** tables, using an inner join.

#### User Information Endpoint
`GET http://127.0.0.1:5000/users/<id>` will return both hacker data and skill data for the hacker with the specified integer ***id***, using an inner join. 

#### Updating User Data Endpoint
`PUT http://127.0.0.1:5000/users/<id>`, given data in a JSON format, will return the updated hacker data as the response. The data's format will be as follows:

```json
{
  "name": <string>,
  "picture": <string>,
  "company": <string>,
  "email": <string>,
  "phone": <string>,
  "skills": [
    {
      "name": <string>,
      "rating": <int>
    }
  ]
}
```

where there can be 0+ skills, and not all pieces of information must be entered. To support this partial updating, the code implementation is split into two parts:

1. For hacker data, first get the original data and set it as the default - any new information will replace its associated default information. 
2. For skills data, loop through any new skills provided, and check if it already exists. If it exists, the skill is updated with its new rating. If it does not, the skill is inserted into the **skills** table as a new entry, with the current user ***id*** as the foreign key. Note: this was implemented taking into account that skills do not update often, and that realistically, there is not a significant number of skills per user, since it utilises a linear search through the current skills.

#### Skills Endpoints
`GET http://127.0.0.1:5000/skills` will return a list of all skills and each of their frequencies.
Querying, as shown below will return list of all skills that are greater than the minimum frequency ***min*** and/or less than the maximum frequency ***max***. 

- `GET http://127.0.0.1:5000/skills/?min_frequency=<min>` 
- `GET http://127.0.0.1:5000/skills/?max_frequency=<max>` 
- `GET http://127.0.0.1:5000/skills/?min_frequency=<min>&max_frequency=<max>` 

## Challenges and Takeaways 

I found this challenge to be very rewarding! It was my first time designing an API and using SQLite (or any SQL-based technology). Thus, the initial hours were spent understanding how SQLite and Flask connect and basic SQL documentation. While learning SQL was straight forward, there were often a lot of small syntactical and ordering errors that bottlenecked the process. I found this project to not be code-intensive, but design-focused, which was new and something I really enjoyed exploring.

I strived for best practices within my code, but there are a couple areas of uncertainty that I'd like to acknowledge and would pursue in the future:

1. When getting hacker data, each INNER JOIN only combines one hacker and one skill - that means if a hacker has two skills, the hacker data will be returned twice, once with each skill.
2. In updates, I am unsure if that is truly partial updating, because the program is still sending back a full row of information, regardless of whether or not every column was updated. My implementation was largely intuition based - I believe there exists a better approach and this would be a next step to investigate.
