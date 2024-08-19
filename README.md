
# Collaborative Story Creator API

This is a basic backend API for the **Collaborative and Fun Story Creator** web application. It supports user authentication and collaborative storytelling, where users can create stories and contribute to existing ones.

## Features

1. **User Authentication Endpoints**:
   - User Registration
   - User Login
   - Get Current User Information

2. **Story Endpoints** (Protected):
   - Create a New Story
   - Get the List of Stories
   - Get a Specific Story
   - Add a Contribution to a Story

## Tech Stack

- **Backend**: Django (Python)
- **Authentication**: JWT (JSON Web Token)
- **Database**: SQLite
- **Storage**: Images are stored on the server in the `media/stories` folder.
- **Logging**: Errors are logged to log/error.log.

## Requirements

- Python 3.12 or above
- Django 5.1
- Django REST Framework
- Django SimpleJWT for authentication

## Setup Instructions

 - Clone the repository:
```
git clone https://github.com/username/story-creator-api.git
```

 - Create a virtual environment and activate it:
```
python3 -m venv env
source env/bin/activate
```
 - Install dependencies:
```
pip install -r requirements.txt
```
 - Run migrations:
```
python manage.py migrate
```
 - Run the development server:
```
python manage.py runserver
```
API Endpoints
 - **User Authentication**:
 -  User Registration (Mock Authentication)
	   -  Endpoint: /signup/
	   -  Method: POST
	   -  Payload:
	      ```
          {
              "username": "user2",
              "password": "test@123"
          }
 -  User Login
	   -  Endpoint: /login/
	   -  Method: POST
	   - Payload:
        ```
         {
           "username": "user1",
           "password": "password123"
          }
        ```
		- Response: Returns an access token on successful login.

- Get Current User Info
	 - Endpoint: /user/
	 - Method: GET
	 - Headers:
	 - Auth: Bearer Token: <access_token>
2. Story Endpoints (Protected)
  - Create a New Story
	  - Endpoint: /story/
	  - Method: POST
	  - Headers:
	  - Auth: Bearer Token: <access_token>
	  - Payload: form-data
	  ```
    {
      "title": "The Adventures of Django",
      "content": "Once upon a time...",
      "image": "<image_file>"
    }
	  ```
  - Get List of Stories
	  - Endpoint: /story/
	  - Method: GET
	  - Headers:
	  - Auth: Bearer Token: <access_token>
	  
- Get a Specific Story
	- Endpoint: /story/?pk=<story_id>
	- Method: GET
	- Headers:
	- Authorization: Bearer <access_token>
	
 -  Add a Contribution to a Story
	 - Endpoint: /story/
	 - Method: PATCH
	 - Headers:
	 - Auth: Bearer Token: <access_token>
	 - Payload:
	    ```
	    {
	      "id": <story_id>,
	      "content": "And they lived happily ever after..."
	    }
	    ```

**Image Upload**

Images can be uploaded with the story. They will be stored with the format: story_<story_id>_<datetime>.ext. The API allows images up to 5MB and only accepts .jpg, .jpeg, and .png formats.
To access the image from the frontend, you can use the path provided in the response, typically under the image field.




