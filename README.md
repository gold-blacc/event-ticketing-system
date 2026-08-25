# 🏛️ GODMANOR — Cloud & AI Infrastructure Event Ticketing System

An event-driven, serverless event ticketing and notification system built on AWS using **Terraform (IaC)**, **API Gateway**, **AWS Lambda**, **DynamoDB Streams**, and **Amazon SNS**.

This portal demonstrates production-grade cloud architecture, real-time database streaming, automated notifications, and secure API integrations tailored for modern cloud support and AI cloud operations.

**Live Demo:** [https://d686wc2aajlxo.cloudfront.net/](https://d686wc2aajlxo.cloudfront.net/)

---

## 📐 Architecture Overview

```
[ Frontend (HTML/JS) ]
        │
        ▼ (HTTP POST /register)
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
```

Static assets (HTML/CSS/JS) are served via **Amazon S3 + CloudFront**, giving the portal global low-latency delivery with no server management.

---

## ✨ Key Technical Features

* **Infrastructure as Code (IaC):** Provisioned entirely via **Terraform** for repeatable, trackable infrastructure deployments.
* **Serverless API Layer:** RESTful API endpoints managed by **Amazon API Gateway** with integrated CORS handling and request validation.
* **Event-Driven Microservices:** Built with **AWS Lambda (Python 3.x)** to handle registration payloads and asynchronous notifications.
* **Real-Time Data Streaming:** Leveraged **DynamoDB Streams** to capture table insert events instantly without polling.
* **Automated Alerting Pipeline:** Integrated **Amazon SNS** to push VIP access confirmations directly to attendees upon DynamoDB stream invocation.
* **Global Static Hosting:** Frontend served via **S3 + CloudFront** for fast, cached delivery worldwide.
* **Modern Web Portal:** Custom glassmorphism UI styled in rich burgundy and gold (`#2B0410` / `#D4AF37`) for a high-end user experience.

---

## 🛠️ Tech Stack & Skills Demonstrated

| Domain | Tools & Technologies |
| :--- | :--- |
| **Cloud Provider** | Amazon Web Services (AWS) |
| **Compute & API** | AWS Lambda, Amazon API Gateway |
| **Database & Streaming** | Amazon DynamoDB, DynamoDB Streams |
| **Messaging & Notifications**| Amazon SNS |
| **Content Delivery** | Amazon S3, Amazon CloudFront |
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
   git clone https://github.com/gold-blacc/event-ticketing-system.git
   cd event-ticketing-system
   ```

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

4. **Confirm SNS Subscription:**
   Check the administrator email address specified in your Terraform configuration and click **Confirm Subscription** in the AWS email.

5. **Deploy Frontend to S3 + CloudFront:**
   ```bash
   aws s3 cp frontend/index.html s3://<your-bucket-name>/index.html
   aws cloudfront create-invalidation --distribution-id <your-distribution-id> --paths "/*"
   ```

---

## 🔍 Troubleshooting & Cloud Support Scenarios

![Flowchart on a black background showing a vertical sequence of five diagnostic stages connected by arrows and labeled Browser form submit, API Gateway /register, Lambda: registerForEvent, DynamoDB write, DynamoDB Streams trigger, and SNS confirmation email. Each box includes a short subtitle describing the step, and the final bottom line reads Full trace verified end to end using AWS CLI and browser dev tools. The overall tone is technical, clean, and support-focused.](assets/troubleshoot.png)

As part of operating and maintaining this system, the following real-world cloud support and diagnostic issues were identified and resolved end-to-end:

* **CORS Access Control:** Resolved cross-origin browser restriction errors by configuring explicit `Access-Control-Allow-Origin` headers on both API Gateway resources and Lambda return payloads.

* **Stream Trigger Diagnosing:** Verified DynamoDB stream view type configurations (`NEW_IMAGE`) to ensure full item attributes are passed payload-intact to downstream Lambda triggers.

* **IAM Least Privilege:** Configured targeted IAM policies granting Lambda functions restricted execution permissions specifically for `dynamodb:DescribeStream`, `dynamodb:GetRecords`, and `sns:Publish`.

* **Silent Frontend Integration Failure:** Diagnosed a production issue where form submissions appeared successful in the UI but never reached the backend. Root cause was isolated by systematically working through the full request path:
  1. Inspected browser console for client-side errors
  2. Verified live API Gateway resources and methods via AWS CLI (`aws apigateway get-resources`)
  3. Traced the full data flow (Frontend → API Gateway → Lambda → DynamoDB → DynamoDB Streams → SNS)
  4. Identified a duplicated event handler block silently breaking form submission JavaScript
  5. Isolated and removed the duplicate, redeployed, and confirmed the fix via a live DynamoDB scan and successful SNS email delivery

* **Cache Invalidation Verification:** Used `aws cloudfront create-invalidation` and `aws s3 ls` to confirm deployed frontend changes were both uploaded correctly and actually served past CloudFront's edge cache — distinguishing browser-cache issues from genuine deployment failures.

---

## 👤 Author

<img src="assets/profile.jpeg" width="120" height="120" style="border-radius: 50%;" alt="Sandra Oteng Abrokwah"/>

**Sandra Oteng Abrokwah**
*Junior Cloud/Support Engineer*
* **LinkedIn:** [linkedin.com/in/sandraotengabrokwah](https://linkedin.com)
* **Certification:** AWS Simulearn AI / Cloud Practitioner