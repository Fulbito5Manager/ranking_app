# Ranking Service
The application was made with Flask framework connecting with the other services through Kafka consumer. Uses MVC simple architecture and, as said before, has a kafka consumer which constantly checks for new updates on the main services. Additionally, it requests information pharalel to the kafka consumer loop to the respective endpoints of the main services.

## Purpose
The current service will serve as a ranking system that will communicate with the main services(partido_service, jugador_service, equipo_service, etc.). It will provide a personal ranking profile for each individual player. Improving the experience of its users so they can enjoy a more competitive aspect of match making!

## Tests
The application counts with at least a 80% test coverage over `tests/` folder. It also provide examples for edge cases and common possible errors in every service. 

### **Setup Instructions**

There is a Docker file available to run the app locally, follow these steps. You can notice the loop will start running due to the logs:

![docker-test-ranking-app](https://dl.dropboxusercontent.com/scl/fi/7x7b2uzxwn6jm8vdjikd6/docker-fucntioning-example.png?rlkey=2uodwg4wo8o0u690zzayzkypn&st=3d98z3jn&dl=1)

1.  **Build and Start the Containers**:
    
    docker-compose build
    docker-compose up -d

### **Future improvements**
Any time soon, we will be working on deploying most of the services as an all-together-app. 

--------------------------------------------
## Techs

• Kafka
• Python
• Docker
• Sqlite
• Flask
