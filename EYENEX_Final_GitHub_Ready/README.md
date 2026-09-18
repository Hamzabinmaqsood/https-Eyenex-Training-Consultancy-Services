# EYENEX Trainings & Consultancy

Production website: **https://eyenextrainingconsultancy.services**

Django 5.2 website for EYENEX Trainings & Consultancy, including course catalogue, admissions, course appointments, admin-controlled appointment fees, EasyPaisa payment proof, financial-aid requests, FAQs, gallery, and responsive UI/UX.

## Current public contact details

- Phone / WhatsApp: +92 310 0987891
- Email: eyenextrainingsandconsultancy@gmail.com
- Address: Burj-e-Noor Plaza, First Floor, Shamsabad, Rawalpindi, Pakistan

## Local setup (Windows PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

For local development, `DJANGO_DEBUG` defaults to `True`. Production must set `DJANGO_DEBUG=False` and a private `DJANGO_SECRET_KEY` in the hosting environment.

## Production / Namecheap

See `NAMECHEAP_DEPLOYMENT.md`.

## Security and repository hygiene

This repository intentionally does **not** contain:

- `db.sqlite3`
- student applications or appointment records
- payment screenshots / private media
- production `.env` files
- production secret keys

Only curated public course artwork under `media/courses/` is versioned. Never commit student data, payment screenshots, passwords, API keys, or production secrets.
