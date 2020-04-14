Simple API that stores category tree to database and returns category
parents, children and siblings by category id.


**API documentation**
-

Service API works on HTTP protocol and accepts GET and POST method only.

All responses are JSON structures.

To receive response send request  to 'http://localhost:8000'

**Endpoints**

- POST /categories
- GET /categories/\<id\>

**POST /categories**
Create and save category tree to database

**Query parameters**:

- name (str, field is required, should be unique)
- children (list, field is not required)


**Request body example**:

`{
    "name": "Category 1",
    "children": [
        {
            "name": "Category 1.1",
                "children": [
                    {
                        "name": "Category 1.1.1",
                        "children": [
                        {
                            "name": "Category 1.1.1.1"
                        },
                        {
                            "name": "Category 1.1.1.2"
                         },
                    }
            ]
            "name": "Category 1.2",
        }
    ]
 }`


**Response parameters**:

- detail
    
**Response code**:

`201` for success

`400` for error
                                                 
**Response body example**:

`{ "detail": "Category tree created." }`

**Error body example**:

`{ "detail": "Category name 'Category 1.1.2' is not unique." }`

**GET /categories/\<id\>**
Retrieves category with its parents, children and siblings by id.

**Request parameters**:

- id (int)

**Request example**:

`curl --header 'Content-Type: application/json' http://localhost:8000/categories/1`

**Response parameters**:

- id
- name
- parents
- children
- siblings
    
**Response code**:

`200` for success

`404` for error
                                                 
**Response body example**:

`{
     "id": 2,
     "name": "Category 1.1",
     "parents": [
         {
             "id": 1,
             "name": "Category 1"
         }
     ],
     "children": [
         {
             "id": 3,
             "name": "Category 1.1.1"
         },
         {
             "id": 7,
             "name": "Category 1.1.2"
         }
     ],
     "siblings": [ 
         {
             "id": 11,
             "name": "Category 1.2"
         }
     ]
}
`


**Error body example**:

`{ "detail": "Not found" }`


**Error codes and description**:

400 Incorrect Category Tree Data

400 Category name %name% is not unique

405 Method Not Allowed

404 Not Found
