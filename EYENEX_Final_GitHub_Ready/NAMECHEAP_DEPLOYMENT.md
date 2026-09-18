# EYENEX Namecheap Deployment

Production domain: `eyenextrainingconsultancy.services`

## Python App

- Python: 3.12
- Application root: `eyenex_app`
- Application URL: `eyenextrainingconsultancy.services`
- Startup file: `passenger_wsgi.py`
- Entry point: `application`

## Production environment variables

Configure these in cPanel > Setup Python App rather than committing them to Git:

- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS=eyenextrainingconsultancy.services,www.eyenextrainingconsultancy.services`
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://eyenextrainingconsultancy.services,https://www.eyenextrainingconsultancy.services`
- `DJANGO_SECRET_KEY=<private-random-production-secret>`
- `EYENEX_EASYPAISA_NUMBER=03408186889`
- `EYENEX_EASYPAISA_ACCOUNT_NAME=Raja Khizar Hayat`
- `DJANGO_STATIC_ROOT=/home/<CPANEL_USERNAME>/public_html/static`
- `DJANGO_MEDIA_ROOT=/home/<CPANEL_USERNAME>/public_html/media`
- `DJANGO_PRIVATE_MEDIA_ROOT=/home/<CPANEL_USERNAME>/eyenex_private_media`
- `DJANGO_SECURE_SSL_REDIRECT=True` after SSL is active

## Update commands

After uploading/pulling updated code, activate the cPanel virtual environment and run:

```bash
cd ~/eyenex_app
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check
```

Restart the Python application in cPanel afterward.

## Media privacy

- Public course/gallery images belong under the configured public `MEDIA_ROOT`.
- Appointment payment screenshots must stay under `DJANGO_PRIVATE_MEDIA_ROOT`, outside `public_html`.
- Payment screenshots are served only through the authenticated staff endpoint.

Do not push the live SQLite database, private uploads, `.env`, or any production secret to a public GitHub repository.
