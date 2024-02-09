# API Usage Documentation

## 1. Obtain Token

To obtain a token, send a POST request to `localhost:8000/api/token/` with the following JSON payload:

```json
{
  "username": "arvindrk",
  "password": "password"
}
```

It will generate the token, and the response will be:

```
{
  "token": "ac3018c4992c2daa823231cb87befc22ac12b4dc"
}

```

## 2. POST Request

For a POST request, add the following key-value pairs to the headers:

```
Content Type: application/json
Authorization: Token ac3018c4992c2daa823231cb87befc22ac12b4dc
```

Then, go to the endpoint localhost:8000/api/todos and send the following JSON payload:

```
{
  "title": "New Tasks 2",
  "description": "New tasks will be added",
  "user": 9
}

```

The user key will increment the last value. The response will be:

```
{
  "id": 4,
  "title": "New Tasks 2",
  "description": "New tasks will be added",
  "completed": false,
  "created_at": "2024-02-09T05:56:25.016486Z",
  "updated_at": "2024-02-09T05:56:25.017484Z",
  "user": 10
}
```

## 3. GET Request

For a GET request, go to the endpoint localhost:8000/api/todos/. It will display the response of all the todos created by the user:

```
[
  {
    "id": 4,
    "title": "New Tasks 2",
    "description": "New tasks will be added",
    "completed": false,
    "created_at": "2024-02-09T05:56:25.016486Z",
    "updated_at": "2024-02-09T05:56:25.017484Z",
    "user": 10
  },
  {
    "id": 5,
    "title": "New Tasks 3",
    "description": "New tasks will be added",
    "completed": false,
    "created_at": "2024-02-09T05:59:26.193270Z",
    "updated_at": "2024-02-09T05:59:26.195823Z",
    "user": 10
  },
  {
    "id": 6,
    "title": "New Tasks 4",
    "description": "New tasks will be added",
    "completed": false,
    "created_at": "2024-02-09T05:59:33.359063Z",
    "updated_at": "2024-02-09T05:59:33.359063Z",
    "user": 10
  }
]

```

To get a particular todo by ID, use the endpoint localhost:8000/api/todos/<pk>, for example, localhost:8000/api/todos/5/, and the response will be:

```
{
  "id": 5,
  "title": "New Tasks 3",
  "description": "New tasks will be added",
  "completed": false,
  "created_at": "2024-02-09T05:59:26.193270Z",
  "updated_at": "2024-02-09T05:59:26.195823Z",
  "user": 10
}


```

## 4. PUT Request

For a PUT request, use the endpoint localhost:8000/api/todos/pk. Example PUT request:

```
{
  "title": "New Tasks 4",
  "description": "New tasks will be added",
  "user": 9
}

```

The response will be

```
{
  "id": 5,
  "title": "New Tasks 4",
  "description": "New tasks will be added",
  "completed": false,
  "created_at": "2024-02-09T05:59:26.193270Z",
  "updated_at": "2024-02-09T05:59:26.195823Z",
  "user": 9
}


```

## 5. DELETE Request

To delete a particular todo, send a DELETE request to localhost:8000/api/todos/pk. Example:

```
localhost:8000/api/todos/5
```

It will delete the specified todo, and the response will be the updated list of todos:

```
[
  {
    "id": 4,
    "title": "New Tasks 2",
    "description": "New tasks will be added",
    "completed": false,
    "created_at": "2024-02-09T05:56:25.016486Z",
    "updated_at": "2024-02-09T05:56:25.017484Z",
    "user": 10
  },
  {
    "id": 6,
    "title": "New Tasks 4",
    "description": "New tasks will be added",
    "completed": false,
    "created_at": "2024-02-09T05:59:33.359063Z",
    "updated_at": "2024-02-09T05:59:33.359063Z",
    "user": 10
  }
]


```
# Bonus

Added the pagination in the settings max try as 5

sorting also done by the methods in views.py


Note the localhost:8000/api/login/ 
