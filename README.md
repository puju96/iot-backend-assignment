# IoT Data Ingestion & Streaming Service

## Overview

This project implements a generic IoT data ingestion and streaming service using FastAPI, MongoDB, and WebSockets.

Due to system restrictions on my office laptop, I was unable to execute the project locally. However, the implementation follows standard async backend architecture and is designed to run in any standard Python environment.

---

## Features

* JWT-based Authentication
* User Management APIs
* IoT Data Ingestion with validation
* Historical & Latest Data Fetch APIs
* Real-time updates using WebSocket subscriptions

---

## Tech Stack

* FastAPI (async framework)
* MongoDB (Motor driver)
* WebSocket for real-time streaming
* JWT Authentication

---

## API Endpoints

### Auth

* POST /auth/login

### User APIs

* POST /users
* GET /users/{user_id}

### IoT Data

* POST /iot/data
* GET /users/{user_id}/iot/latest
* GET /users/{user_id}/iot/history

---

## WebSocket

### Subscribe

/ws/subscribe?user_id=U1001&token=JWT_TOKEN

Behavior:

* Client subscribes to user data stream
* Receives real-time updates on new data ingestion

---

## Validation Rules

* metric_1: 0–100
* metric_2: 0–200
* timestamp cannot be in future
* user must exist and be active

---

## Architecture

* Async FastAPI application
* MongoDB for data persistence
* Connection manager for WebSocket broadcasting

---

## Design Decisions

* Used async framework for scalability
* Separated concerns (auth, models, db, websocket)
* Implemented real-time streaming using WebSockets

---

## Future Improvements

* Redis Pub/Sub for horizontal scaling
* Docker containerization
* Rate limiting
* Unit testing with pytest
