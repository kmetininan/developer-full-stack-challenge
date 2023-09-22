# Library Application

This project uses the following packages:

- Nuxt 2.x
    - BootstrapVue
    - [VueTreeselect](https://vue-treeselect.js.org/)
- FastAPI
    - Pydantic
    - SQLAlchemy

Sqlite file with dummy data is attached to the repository

## Setup

### Backend

```bash
cd api
python3 -m venv .
source bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

This code uses node:16.16. If you are using nvm to switch node version, use `nvm use v16.16.0`

```bash
cd dashboard
npm i
npm run dev
```

## User Credentials

```bash
username: 'foo@bar.com'
password: 'foobar'
```
