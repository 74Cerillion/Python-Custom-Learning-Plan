"""HTTP Request/Response Model
Defines a communication pattern where a client sends a request to a server, and the server responds
    appropriately.
PHASES:
1. Client sends request
    client initiates communication by sending HTTP request to URL or endpoint
    Request includes HTTP method (GET, POST, PUT, DELETE) indicating desired action
2. Server parses request
3. Server processes request
4. Server sends response
5. Client parses response and uses it
"""

"""HTTP Methods
Indicate desired action to be performed got a given resource
Sent by client in request
1: GET
    Purpose - Retrieves representation of specfiied resource
    Retrieves data, does not contain request body
    Safe, idempotent, and cachable
2: POST
    Submits data to a resource, often triggering state changes or creating records
    Neither safe nore idempotent
3: PUT
    Replaces an entire target resource or creates it if missing;
    idempotent but not safe
4: PATCH
    Applies partial updates to a resource;
    Neither safe nor idempotent
5: DELETE
    Removes specified resource
    inherently idempotent, but not safe
* Safe defined as methodic alterations to server state *
"""

"""URL Endpoints
An API endpoint is an specific URL where an application or server receives requests
    to access or change a digital resource

A specific URL where an API receives requests and sends responses.

When a client makes an API call, this is what happens:
    1. Client sends a request with the endpoint URL
    2. Request routes to server, who matched the URL path to handler
    3. Server processes request by validating input and applying business logic
    4. Response is generated and returned to the client with data or confirmation

Key Parts:
Base URL(https://api.example.com)
The resource you want to modify or its location (/users)
HTTP Method: The action you want to perform (GET or POST)
Parameters: Extra data added as filters, ID variables in the path, or a JSON payload body
GET https://api.example.com/v1/users/123?include=posts
GET- HTTP Method
https://api.example.com- Base URL
v1- Version
Endpoint Path- users
123?-Path parameter(user ID)
include=posts- Query parameter

Request:

GET /api/users/12345 HTTP/1.1
Host: api.example.com
Authorization: Bearer your_token_here
Accept: application/json

Response:

HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "12345",
  "name": "Perry Ostman",
  "email": "p.ostman@example.com",
  "role": "Developer"
}
"""

"""Requests Headers

"""

"""Response Headers

"""

"""HTTP Status codes and status-code families

"""