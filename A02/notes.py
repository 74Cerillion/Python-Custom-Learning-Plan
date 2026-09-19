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

"""Request and Response Headers
    Metadata fields that accompany HTTP requests, providing additional context
        providing additional context about the communication between clients and servers.
    They contain key-value pairs that define content types, auth credentials, chaching behavior
        handling instructions, and its contents.
Headers define how every API communicates
Simple Format:
    Header-Name: Header-Value
Types of Headers;
    1. Request Headers: sent from client to server. containing info about req,
        client's capabililities, and what client expects in return
    2. Response Headers: Sent from server to client, providing metadata about response, including 
        how client should handle returned data
    3. Representation Headers: Describe the encoding, format, and other characteristics of the message
        body in both requests and responses
    4. Payload headers: Contain information about the payload data, including content length, encoding, and
        range information for partial content delivery
"""

"""HTTP Status codes and status-code families
    3-digit numbers returned by a server to a client that communicate the outcome of an HTTP request.
    Organized into 5 distinct families determined by their first digit:
1xx = informal
    request recieved, server continuing to process
2xx = success 
    action successfully received, understood, and accepted
3xx = Redirection
    Further action needs to be taken by the client to complete the request
4xx = Client Error
    Request contains bad syntax or cannot be fulfilled due to a client-side issue
5xx = Server Error
    Server failed to fulfill an apparently valid request due to an internal error

Key status code to know:
200 OK
201 Created
204 No Content
301 Moved Permanently
302 Found - resource temporarily located at new URL
304 Not Modified
400 Bad Request
401 Unauthorized - Server does not know who you are
403 Forbidden - Server knows who you are, but you do not have proper permissions to perform action
404 Not Found
408 Request Timeout
429 Too Many Requests (Rate limiting)
"""

"""How does an HTTP Library expose response status/body/JSON
By returning a unified response object that provides properties for the status code, raw text or binary
    body, and parsed JSON methods
https://www.youtube.com/playlist?list=PLMtN5CLH3nnTANATvkTFsl_M-BZJ3XONy
"""