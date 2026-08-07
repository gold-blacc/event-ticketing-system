# Serverless Event Ticketing System

A scalable, serverless Event Ticketing API built on AWS using Lambda, DynamoDB, and API Gateway, with automated CI/CD deployments via GitHub Actions.

## Architecture

* **API Gateway**: REST API managing endpoints and routing.
* **AWS Lambda (Python 3.15)**: Serverless compute functions handling business logic, data validation, and atomic database operations.
* **AWS DynamoDB**: NoSQL database hosting `EventsTable` and `RegistrationsTable`.
* **GitHub Actions**: Continuous integration and deployment pipeline updating Lambda functions on `main` branch pushes.

---

## API Documentation

### Base URL
`https://adqrmc34qb.execute-api.us-east-1.amazonaws.com/prod`

### Endpoints

#### 1. List All Events
* **HTTP Method**: `GET`
* **Path**: `/events`
* **Success Response (200 OK)**:
  ```json
  [
    {
      "eventId": "evt001",
      "eventName": "AWS Workshop Accra 2026",
      "capacity": 100,
      "date": "2026-05-15",
      "registered": 2,
      "status": "Available"
    }
  ]