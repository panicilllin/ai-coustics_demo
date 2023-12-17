# Readme file for this project

--------

## Project Requitement

Development of a Containerized Audio Processing API Using Python Objective:

To develop a user-facing, containerized API for audio file processing with features for uploading, downloading, and volume adjustment. 
The API should be defined according to the OpenAPI 2.0 standard, including an authentication scheme using an API key.

### Requirements:

1. API Development:
Develop a RESTful API in Python for audio file processing.
Implement functionalities for uploading and downloading audio files.
Provide an endpoint for adjusting the volume of audio files in decibels Full Scale (dBFS).

2. OpenAPI 2.0 Specification with Authentication:
Define the API using the OpenAPI 2.0 specification.
Include a well-defined authentication scheme using API keys.
Ensure comprehensive documentation of all endpoints, including authentication procedures.

3. Docker Containerization:
Containerize the API using Docker for easy deployment and scalability.
Provide a Dockerfile and detailed instructions for building and running the Docker container.

4. Audio Processing:
Develop functionality for audio volume adjustment while maintaining audio integrity. Support common audio file formats.

5. Testing and Validation:
Write unit tests for all functionalities, including authentication and audio processing. 
Validate the correct functioning of file uploads, downloads, and volume adjustments.

6. Error Handling and Security:
Implement robust error handling for common scenarios.
Ensure the API securely handles and stores API keys and audio files. 

7. Code Quality and Documentation:
Adhere to best coding practices, ensuring clean and maintainable code. Provide clear comments and documentation for code and API usage.

### Deliverables:

Source code for the API.

OpenAPI 2.0 specification document including the authentication scheme. Dockerfile and deployment instructions.

Unit tests for the API.

A README file with setup, running instructions, and API usage guidelines.

### Evaluation Criteria:

Functionality: Does the API meet the functional and technical requirements?

Code Quality: Is the code well-structured, readable, and maintainable?

Compliance with OpenAPI 2.0 and Security: Does the API follow OpenAPI standards with secure authentication? Containerization: Is the Docker setup correctly configured for easy deployment?

Documentation: Is the documentation thorough for understanding API usage and deployment?

### Submission Instructions:

Submit a Git repository link containing all deliverables.

Ensure the repository includes the Dockerfile, API code, OpenAPI specification, tests, and README.


-------

## Guide from author

### Structure
ai-coustics

  - api/                     
    - audio.py          ::  api route for audio upload/download/list/adjust volume
    - user.py           ::  api route for user create/login

  - model/
    - database.py       ::  method for database connection and tools related to database
    - models.py         ::  sqlalchemy models
    - schemas.py        ::  pydantic models, not in use
  
  - utils/
    - audio_utils.py    ::  method for audio volume adjust and tools related to audio
    - user_utils.py     ::  method for about encrypt and token
    - general_utils.py  ::  other method

  - test/               ::  thst file for this project
  - logs/               ::  logs folder, empty while not running
  - temp/               ::  path for temp file, should be empty all time
  - storage/            ::  audio file storage path, you can put this path out of container

  - main.py             ::  entrance of this project
  - config.py           ::  config file of this project
  - requirements.txt
  - Dockerfile
  

### Deployment

```bash
cd ai-coustics
mkdir storage
docker build -t audio_backend:v1 -f ./Dockerfile .
docker run -itd --name backend -p 8000:8000 -v ./storage:/backend/storage audio_backend:v1
```

### Use

open browser, typing:
http://127.0.0.1:8000/docs#

- /api/user/create      create user
- /api/user/login       login and get a fake token for other request
- /api/audio/upload     use token upload a audio file 
- /api/audio/list       all audio file for one user, can get the request_id of each file
- /api/audio/download   audio file by given request_id of the audio file
- /api/audio/volume     adjust audio volume and download by given request_id volume, volume could be positive and negetive
- /ping                 health check

### TODO

- test case fillup
- response code fillup
- fake token into real token
