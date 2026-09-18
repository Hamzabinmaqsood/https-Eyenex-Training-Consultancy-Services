from django.conf import settings


def site_info(request):
    return {
        'site_name': 'EYENEX Trainings & Consultancy',
        'site_short_name': 'EYENEX',
        'site_tagline': 'Empowering Professionals. Building Safer Futures.',
        'site_phone': '+92 310 0987891',
        'site_whatsapp_number': '923100987891',
        'site_whatsapp_url': 'https://wa.me/923100987891',
        'site_email': 'eyenextrainingsandconsultancy@gmail.com',
        'site_address': 'Burj-e-Noor Plaza, First Floor, Shamsabad, Rawalpindi, Pakistan.',
        'site_domain': 'eyenextrainingconsultancy.services',
        'easypaisa_number': settings.EASYPAISA_NUMBER,
        'easypaisa_account_name': settings.EASYPAISA_ACCOUNT_NAME,
    }

