# Serverless Event Ticketing System

An end-to-end, event-driven ticketing platform built on AWS, deployed automatically via GitHub Actions CI/CD pipelines, and provisioned using Terraform Infrastructure as Code (IaC).

---

## 🏛️ System Architecture & Tech Stack

* **Compute:** AWS Lambda (Python 3.x) handling event lookups, registrations, and error handling.
* **API Layer:** Amazon API Gateway REST endpoints with CORS enabled for web frontends.
* **Database:** Amazon DynamoDB NoSQL tables for atomic capacity updates and guest registrations.
* **Infrastructure as Code:** Terraform for declarative cloud resource management.
* **CI/CD Pipeline:** GitHub Actions automated workflows testing and deploying Lambda functions on push.
* **Frontend Portal:** Responsive glassmorphic UI hosted on S3 integrating live backend endpoints.

---

## 🛠️ Key Technical Challenges Solved

1. **DynamoDB Decimal Serialization:** Designed custom Python JSON encoders to handle DynamoDB numerical types seamlessly over HTTP.
2. **Atomic Counter Updates:** Used DynamoDB `UpdateExpression` logic to prevent race conditions during concurrent booking spikes.
3. **Resilient Error Handling:** Implemented structured 400 Bad Request and 404 Not Found payloads for invalid payloads and missing event records.

---

## 🚀 Live API Endpoints

* **`GET /events`** - Fetch all active events and seating capacities
* **`GET /events/{eventId}`** - Fetch single event details
* **`POST /register`** - Register a guest for an event

```json
// Example POST /register payload
{
  "eventId": "evt001",
  "userName": "Sandra Oteng Abrokwah"
}