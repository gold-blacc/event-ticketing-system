# 🏛️ GODMANOR — Cloud & AI Infrastructure Event Ticketing System

An event-driven, serverless event ticketing and notification system built on AWS using **Terraform (IaC)**, **API Gateway**, **AWS Lambda**, **DynamoDB Streams**, and **Amazon SNS**. 

This portal demonstrates production-grade cloud architecture, real-time database streaming, automated notifications, and secure API integrations tailored for modern cloud support and AI cloud operations.

---

## 📐 Architecture Overview

[ Frontend (HTML/JS) ]
│
▼ (HTTP POST)
[ Amazon API Gateway ]
│
▼
[ AWS Lambda: registerForEvent ]
│
▼ (PutItem)
[ Amazon DynamoDB ] ──(DynamoDB Streams)──► [ AWS Lambda: sendTicketNotification ]
│
▼
[ Amazon SNS Topic ]
│
▼ (Email Notification)
[ End User Inbox ]


---

## ✨ Key Technical Features

* **Infrastructure as Code (IaC):** Provisioned entirely via **Terraform** for repeatable, trackable infrastructure deployments.
* **Serverless API Layer:** RESTful API endpoints managed by **Amazon API Gateway** with integrated CORS handling and request validation.
* **Event-Driven Microservices:** Built with **AWS Lambda (Python 3.x)** to handle registration payloads and asynchronous notifications.
* **Real-Time Data Streaming:** Leveraged **DynamoDB Streams** to capture table insert events instantly without polling.
* **Automated Alerting Pipeline:** Integrated **Amazon SNS** to push VIP access confirmations directly to attendees upon DynamoDB stream invocation.
* **Modern Web Portal:** Custom glassmorphism UI styled in rich burgundy and gold (`#2B0410` / `#D4AF37`) for high-end user experience.

---

## 🛠️ Tech Stack & Skills Demonstrated

| Domain | Tools & Technologies |
| :--- | :--- |
| **Cloud Provider** | Amazon Web Services (AWS) |
| **Compute & API** | AWS Lambda, Amazon API Gateway |
| **Database & Streaming** | Amazon DynamoDB, DynamoDB Streams |
| **Messaging & Notifications**| Amazon SNS |
| **Infrastructure as Code** | Terraform |
| **Languages & Scripting** | Python (Boto3), JavaScript (ES6+), HTML5, CSS3 |
| **Version Control** | Git, GitHub |

---

## 🚀 Deployment & Operations

### Prerequisites
* AWS CLI configured with appropriate IAM permissions
* Terraform installed locally

### Step-by-Step Provisioning

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/gold-blacc/event-ticketing-system.git](https://www.linkedin.com/in/sandra-oteng-abrokwah)
   cd event-ticketing-system

   2. **Package the Notification Function:**
```bash
cd terraform
zip -j notification_payload.zip ../functions/sendTicketNotification/lambda_function.py
```
3. **Deploy Infrastructure via Terraform:**
```bash
terraform init
terraform apply
```
*Type `yes` when prompted to confirm deployment.*
4. **Confirm SNS Subscription:**
Check the administrator email address specified in your Terraform configuration and click **Confirm
Subscription** in the AWS email.
---
## �� Troubleshooting &amp; Cloud Support Scenarios
As part of operating this system, the following cloud support &amp; network diagnostic steps were
implemented and verified:
* **CORS Access Control:** Resolved cross-origin browser restriction errors by configuring explicit
`Access-Control-Allow-Origin` headers on both API Gateway resources and Lambda return payloads.
* **Stream Trigger Diagnosing:** Verified DynamoDB stream view type configurations (`NEW_IMAGE`)
to ensure full item attributes are passed payload-intact to downstream Lambda triggers.
* **IAM Least Privilege:** Configured targeted IAM policies granting Lambda functions restricted
execution permissions specifically for `dynamodb:DescribeStream`, `dynamodb:GetRecords`, and
`sns:Publish`.
---
## �� Author
**Sandra Oteng Abrokwah**

*Cloud Support &amp; AI Infrastructure Engineer*
* **LinkedIn:** [linkedin.com/in/sandraotengabrokwah](https://linkedin.com)
* **Certification:** AWS Simulearn AI/ Cloud Practictioner