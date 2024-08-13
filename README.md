# La Patisserie Du Coeur

La Patisserie Du Coeur is an e-commerce bakery website that allows users to conveniently order bakery goods online. The website is built using Django REST API on the backend and ReactJS, Docker, and TailwindCSS on the frontend.
![image](https://github.com/SeaBebop/La-Patisserie-Du-Coeur/assets/54507045/eab797dd-fef7-4b25-8b71-99455a2d704a)

# Deployed Demo (Currently AWS implimented! Previously was gcloud deployed )
- https://lacoeurbakery.xyz

# Table of Contents

- [La Patisserie Du Coeur](#la-patisserie-du-coeur)
  - [Structure](#structure)
  - [Features](#features)
  - [Setup](#setup)
    - [Clone the repository](#clone-the-repository)
    - [Build and Run Docker Container](#build-and-run-docker-container)
  - [Setting Up Emails (Optional)](#setting-up-emails-optional)
  - [Setting Up Stripe Test Payments (Optional)](#setting-up-stripe-test-payments-optional)
  - [Dependencies](#dependencies)
## Structure 
### AWS
![image](https://github.com/user-attachments/assets/1694e660-5e43-4808-b04d-b476d0aa2c1d)
### GCP
![image](https://github.com/user-attachments/assets/da113263-cb72-4327-a0a6-cfc8a90b5d4c)

## Features

  <img align="left" width="250" src="https://github.com/SeaBebop/La-Patisserie-Du-Coeur/assets/54507045/d69f5060-ce1c-48a3-a0e0-ab490b449c6b" alt="Image" width="200"/>


- **User-friendly Interface**: Users can easily browse through a variety of bakery goods and conveniently add them to their cart.
- **Inventory Management**: Celery task and beat efficiently manage the product inventory, ensuring accurate stock levels.
- **Persistent Sessions**: Anonymous users are registered with a persistent session, enabling them to access their cart and purchase history across sessions.
- **User Accounts**: Registered users can enjoy the benefits of having an account, including JWT cookie authentication for secure login and the ability to persistently log in.
- **Cart Transfer**: Anonymous users can seamlessly transfer their old session carts to their newly created accounts.
- **Payment Processing**: Purchases are securely processed using a test mode version of Stripe webhook.

<br>

[(Back to Top)](#table-of-contents)

<br>
<br>
<br>
<br>
<br>
<br>


## Setup

### Clone the repository:

```bash
git clone https://github.com/<your-username>/La-Patisserie-Du-Coeur.git

```
### Build and Run Docker Container:
``` bash
docker compose  -f "docker-compose-dev.yml" up -d --build rabbitmq celery-worker celery-beat db frontend web nginx
```
## Alternative only FrontEnd Setup:
```bash
cd frontend && npm start
```
[(Back to Top)](#table-of-contents)
## Setting Up Emails (Optional):
![image](https://github.com/SeaBebop/La-Patisserie-Du-Coeur/assets/54507045/0c07bcdf-712a-4923-a9ed-5548a5abddba)

- **Create a SendGrid Account:** Visit SendGrid's website to create your own account.
- **Generate API Key:** Generate a full access API key from your SendGrid account settings.
- **Update Environment Variables:** Update DOCKER_DEFAULT_FROM_EMAIL with your email and DOCKER_EMAIL_HOST_PASSWORD with your API key in env_backend_dev.env.
[(Back to Top)](#table-of-contents)
## Setting Up Stripe Test Payments (Optional):
![image](https://github.com/SeaBebop/La-Patisserie-Du-Coeur/assets/54507045/2d97c294-b7ce-497c-9bf2-abc68f8e5051)

- **Create a Stripe Account:** Sign up for a Stripe account on their website.
- **Locate Secret Key:** Find your secret key in your Stripe account settings and copy it to DOCKER_STRIPE in env_backend_dev.
- **Configure Webhooks:** Follow the instructions provided at Stripe Dashboard and adjust step 2 to $ stripe listen --forward-to localhost/api/v1/checkout/webhook/stripe/.
- **Retrieve Endpoint Secret:** After following the CLI instructions, you will receive a whsec_... key. Copy this to DOCKER_ENDPOINT_SK in env_backend_dev.env.
[(Back to Top)](#table-of-contents)
## Dependencies
- Docker 20.10.5
- Python 3.8
- Django 3.2
- Django REST Framework 3.12
- ReactJS 17.0
[(Back to Top)](#table-of-contents)
