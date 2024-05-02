# Project Name
    
    ChatBot-Gpt
      
## Description

    This is a test project, designed in Django, and created to show certain skills as a backend developer. It is an artificial intelligence chat, connected to the external OpenAI API that manages to generate the chat experience with said technology. It has a Postgres database to save users and their conversation histories, that is, it saves all the messages that you send. The project also incorporates Celery to execute the asynchronous task of eliminating users that exceed 24 hours of creation and that relies on Redis as a message broker. In addition, all these services are executed and orchestrated within Docker and Docker-compose.

## Installation

    1. Ensure Docker and Docker-compose are installed on your machine.

    2. Create a Project directory

    3. Create and activate Virtual Enviroment

    4. Clone the repository to your local machine.

    5. Run the following command to build and start the Docker containers:

        docker-compose up --build -d

## Usage
    After running the Docker containers, you can access the chatbot at http://localhost:8000.


## Project Structure
    The project is structured as follows:

    chat/: Contains the Django application for the chatbot.
    core/: Contains the core Django settings and configurations.
    static/: Contains static files like CSS.
    templates/: Contains HTML templates for the chatbot.
    Dockerfile: Defines the Docker image for the Django application.
    docker-compose.yml: Defines the services that make up the application.
    entrypoint.sh: A script that is run when the Docker container is started.
    manage.py: A command-line utility for administrative tasks.
    requirements.txt: Contains the Python dependencies for the project.

## Contributing
Any contribution you want to make is welcome to improve this project. Please follow the standard Fork & Pull Request process if you want to contribute.

## License

    Information about the project's license and any additional terms or conditions.

## Contact

    email: ansagu88@gmail.com
    github: ansagu88