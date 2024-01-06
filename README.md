# AH Receipt Parser (or something like that)

## Requirements

- Python 3 (I tested it only on 3.10)
- Postgres 14

## How to

This application is using the API for the mobile AH app. Thanks to Rutgerdj for getting me started on the undocumented API, otherwise I'd have to do it with OCR...

- Install dependencies with `pip install -r requirements.txt`
- Rename the `config-template.yml` file to `config.yml`. The only thing that is required is `api.code`, which needs to be fetched as follows:
  - Visit https://login.ah.nl/secure/oauth/authorize?client_id=appie&redirect_uri=appie://login-exit&response_type=code
  - Open the dev tools and go to the network tab
  - Enter your credentials on the website and login. The page might not change at all but new requests in the network tab will appear.
  - Look for the GET request https://login.ah.nl/login/_next/data/blabla/nl/ingelogd.json with the `ingelogd.json` file
  - In the response body of the request, look for the key `__N_REDIRECT` in the `pageProps` object. The value that comes after `appie://login-exit?code=` is the code that needs to be put into `api.code`
- `cd` into `src`
- Run `main.py`, for example `python main.py`

### Docker compose
If you're using Docker, you can start everything with `docker compose up`. It's spinning up a postgres and a pgadmin instance as well, such that you can look at your data. All that is needed is the `docker-compose.yml` file and the `config.yml`, which should be placed in the same directory.

```yml
version: "3.8"

services:
  grocitrack:
    image: ghcr.io/funnypocketbook/receipt-scanner:master
    container_name: grocitrack
    volumes:
      - ./config.yml:/app/config.yml
    networks:
      - grocitrack
    depends_on:
      - postgres
  postgres:
    image: postgres:14
    container_name: postgres-grocitrack
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: admin
      POSTGRES_DB: grocitrack
    ports:
      - "5432:5432"
    networks:
      - grocitrack

  pgadmin:
    container_name: pgadmin4_container
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: root
    ports:
      - "5050:80"
    networks:
      - grocitrack

networks:
  grocitrack:
```


### Functionalities
Basically, what works now already is that all receipts and the groceries from the receipt are stored in a database. I want to add at least the categories (including translating them) to the database and include proper logging before I startsta the frontend.

- [x] Authorization
- [x] Database integration (sqlite, mysql, postgresql)
- [x] Receipt parsing
- [x] Product parsing
  - [x] Product categories

### Todo
- [x] Add product categories
- [ ] Proper logging
- [ ] ~~Handle missing category~~ Shouldn't occur, since all categories are fetched weekly
  - [ ] ~~If category not found, fetch it, add it to database, continue~~
- [x] Handle product not found
  - [x] Match by "previously bought item"
  - [ ] Extend the search by matching on all categories and not just the subcategory
  - [ ] Extend the search by `LIKE %name%` and weighing those results higher
  - [x] Create new table to store all unmatched products/all potential matches
  - [ ] ~~Split name into tokens and search for each token~~
  - [ ] ~~If no results, use LLM (LLama) to find out what the name was meant to be~~
- [ ] Create superclass for DbAHProducts DbPreviousProducts
- [ ] Refactor Product._set_details()
- [ ] Discount not bound to any products
- [ ] Frontend in Vue.js
- [ ] Show average percentage saved (per category and total)

### ER Diagram
Not quite up to date but close enough.
![ER Diagram](ER_diagram.png)
