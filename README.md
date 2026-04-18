# Online Store

This repository contains a Python Django backend and a Next.js frontend for a mini Amazon-style e-commerce platform.

## Backend

Path: `backend`

### Setup

1. Create a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Copy `.env.example` to `backend/.env` and fill in your database and Paymob credentials.
4. Run migrations:
   ```bash
   python backend/manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python backend/manage.py createsuperuser
   ```
6. Run development server:
   ```bash
   python backend/manage.py runserver
   ```

## Frontend

Path: `frontend`

### Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Run dev server:
   ```bash
   npm run dev
   ```

## Deployment

### GitHub

1. Initialize git in the repository if needed:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```
2. Create a new GitHub repository and push:
   ```bash
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git branch -M main
   git push -u origin main
   ```

### Vercel

This repo uses Vercel multi-service deployment for frontend and backend.

1. Sign in to Vercel and choose "Import Project".
2. Connect the GitHub repository `Felosameh97/online-store`.
3. Set the Root Directory to `./` (important — do not choose `frontend`).
4. Vercel will read `vercel.json` from the repo root and deploy two services:
   - `frontend` from `frontend/` using Next.js
   - `backend` from `backend/` using Django
5. Add environment variables in Vercel for backend and frontend as needed.
6. Deploy and monitor logs in Vercel.

If Vercel asks for a framework or build settings, use the defaults from the `vercel.json` configuration.

> If you already created a project with `frontend` as root, delete it and recreate it using root `./` so Vercel loads the multi-service config correctly.

## Notes

- Backend checkout and Paymob integration are available in `backend/shop/paymob.py`.
- Admin and automation endpoints are in `backend/shop/views.py`.
- The frontend is a minimal Next.js + Tailwind app in `frontend`.
