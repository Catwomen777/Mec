 Mechanic Shop Service Ticket API

This is a full REST API for managing customers, mechanics, service tickets, and inventory for a mechanic shop.  
The API supports authentication (JWT), caching, rate limiting, relationship handling, and Swagger documentation.

---

 Features

- Customer registration, login & JWT authentication
- CRUD for Customers, Mechanics, Service Tickets, and Inventory Items
- Assign / Remove Mechanics from Service Tickets (Many-to-Many relationship)
- Rate limiting with **Flask-Limiter**
- Response caching with **Flask-Caching**
- API documentation using **Swagger UI**
- Fully tested with `unittest`

---

 Tech Stack

| Component | Library |
|---------|--------|
| Backend Framework | Flask |
| ORM | SQLAlchemy |
| Serialization | Marshmallow |
| Auth | JWT Tokens |
| DB (local) | SQLite |
| API Docs | Swagger UI |
| Testing | unittest |

---

 Setup Instructions

 1. Clone the Repository

git clone <your-repository-url>
cd Mec
