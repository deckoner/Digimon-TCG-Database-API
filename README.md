# Digimon TCG Database API
This project is an **API built with FastAPI** that allows interaction with a complete Digimon TCG card database. It enables users to manage their collection, build decks, and retrieve detailed card information programmatically.

---

## 🚀 What does this API do?
- 📦 Manage your **card collection**: add, remove, and update cards.
- 🧩 Create and organize **decks**: add/remove cards, update quantities, retrieve deck content.
- 🔍 Query the database for detailed card info (via endpoints).
- 🧪 Designed for integration with a frontend or external tools.

---

## ⚙️ .env configuration
Before running the API, you need to create an `.env` file in the root directory with the following content:
```env
DB_HOST=your_host
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_database_name
API_KEY=your_api_key
```
This config is used to connect the API to your MySQL database.

---

## ▶️ How to run the API
Once the environment is configured, you can launch the API using:
```bash
uvicorn main:app --reload
```
---

## 🧪 Example endpoints
Here are some of the available routes:
- `GET /collection/` — Get paginated user collection  
- `POST /collection/add` — Add a card to your collection  
- `DELETE /collection/delete/{card_number}` — Remove a card from your collection  
- `POST /decks/add` — Create a new deck  
- `GET /decks/{deck_id}/cards` — Get all cards in a deck  
- `POST /decks/{deck_id}/cards/add` — Add cards to a deck  
- `PUT /decks/{deck_id}/cards/update/{card_number}` — Update card quantity in a deck  
- `DELETE /decks/{deck_id}/cards/delete/{card_number}` — Remove a card from a deck  

All endpoints require an API token via the `Authorization` header.

---

## Card insertion vs quantity update
The API handles card quantities based on whether a card already exists in a collection or deck:

- **Adding a new card**  
  - Endpoint: `POST /collection/add` or `POST /decks/{deck_id}/cards/add`  
  - If the card does **not exist** in the collection or deck, it will be inserted as a new record with the specified quantity.

- **Incrementing quantity**  
  - Endpoint: `POST /collection/add`  
  - If the card **already exists**, the specified quantity is added to the current quantity.  
  - Example: adding `BT1-001` with quantity `1` then adding `2` more results in a total quantity of `3`.

- **Updating quantity explicitly**  
  - Endpoint: `PUT /decks/{deck_id}/cards/update/{card_number}`  
  - Use this to set a card to a specific quantity in a deck.  
  - Setting the quantity to `0` will **remove the card** entirely from the deck.

- **Deleting a card**  
  - Endpoints: `DELETE /collection/delete/{card_number}` or `DELETE /decks/{deck_id}/cards/delete/{card_number}`  
  - Removes the card completely from the collection or deck, regardless of its current quantity.

These rules ensure duplicate entries are avoided and quantity management is consistent.

---

## ⚠️ Warnings and limitations
- This API assumes the database has already been filled with valid Digimon TCG data.
- The quality of the data depends on the source — if there are issues in the scraped database, they will reflect in the API responses.
- This is a backend project only — no frontend or user interface is included (yet).

---

## 📌 License and Rights
This project is for **personal and educational use only**.
All rights to Digimon TCG belong to **Bandai**.  
This API is an **unofficial project** and has no affiliation with Bandai or the creators of Digimon TCG.

---

## 🛠️ Coming soon
Work in progress:
- 🖥️ A **web frontend** to manage your collection and decks visually.
- 🔄 Enhanced search and filter options for card queries.
