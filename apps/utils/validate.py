from django.utils.translation.trans_null import gettext_lazy as _

from apps.models import User


def validate_phone_number(phone_number):
    phone_number = phone_number.replace(' ', '')
    if phone_number and phone_number[0] != '+':
        phone_number = '+' + phone_number
    if not phone_number:
        return {'message': _('This is empty.'), 'status': 400}
    c = 0
    for i in phone_number:
        if i.isdigit():
            c += 1
    if c != 12:
        return {'message': _('Enter correct phone number.'), 'status': 400}
    user = User.objects.filter(phone_number=phone_number).first()
    return {'message': 'success', 'user': user, 'status': 200}
