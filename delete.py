import datetime

import telebot
from bot.models import Search, TgUser, UserCart
from bot.system import *
from botconfig.models import (Avto, AvtoKub, Category, Paket, PodCategory,
                              StartNarx, Tuman, Viloyat, AvtoPod)
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import F, Q, QuerySet
from django.utils import timezone
from telebot import types


def search_avto_save(message, bot):
    user = TgUser.objects.get(tg_id=message.chat.id)
    lan = user.lan

    search_false = Search.objects.filter(user__tg_id=message.from_user.id, status_check=False, status=False)
    search_true = Search.objects.filter(user__tg_id=message.from_user.id, status=False, status_check=True)

    if search_false.exists():
        search_false.delete()

    if search_true.exists():
        search_true.update(status=True)

    avto_button = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    if lan == 'oz':
        category = Category.objects.filter(oz=message.text).first()
        search = Search.objects.create(
            user=user,
            category=category
        )
        btn = []
        if search.category.cat == '4':
            btn = [avto.oz for avto in Avto.objects.filter(is_special=True)]
        else:
            btn = [a.oz for a in Avto.objects.filter(is_special=False)]

        avto_button.add(*btn)

    if lan == 'uz':
        category = Category.objects.get(uz=message.text)
        search = Search.objects.create(
            user=user,
            category=category
        )
        if search.category.cat == '4':
            btn = [avto.uz for avto in Avto.objects.filter(is_special=True)]
        else:
            btn = [avto.uz for avto in Avto.objects.filter(is_special=False)]

        avto_button.add(*btn)

    if lan == 'ru':
        category = Category.objects.get(ru=message.text)
        search = Search.objects.create(
            user=user,
            category=category
        )
        if search.category.cat == '4':
            btn = [avto.ru for avto in Avto.objects.filter(is_special=True)]
        else:
            btn = [avto.ru for avto in Avto.objects.filter(is_special=False)]

        avto_button.add(*btn)


    category = Search.objects.filter(user__tg_id=message.from_user.id, status_check=False,
                             status=False).first().category

    if category.cat == '3':

        if user.province:
            Search.objects.filter(user__tg_id=message.from_user.id, status_check=False, status=False).update(province=user.province)

            district_button = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

            if lan == 'oz':
                district_button.add(*[LAN[lan]['all_district']])
                district_button.add(*[d.oz for d in Tuman.objects.filter(viloyat=Viloyat.objects.get(oz=user.province.oz))])
                # district_button.add(*[LAN[user.lan]['share_location']])

            elif lan == 'uz':
                district_button.add(*[LAN[lan]['all_district']])
                district_button.add(*[d.uz for d in Tuman.objects.filter(viloyat=Viloyat.objects.get(uz=user.province.uz))])

            elif lan == 'ru':
                district_button.add(*[LAN[lan]['all_district']])
                district_button.add(*[d.ru for d in Tuman.objects.filter(viloyat=Viloyat.objects.get(ru=user.province.ru))])

            district_button.add(types.KeyboardButton(text=LAN[lan]['change_province']))
            district_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])

            bot.send_message(message.from_user.id, LAN[lan]['search_tuman1'], reply_markup=district_button,
                             parse_mode='html')

            set_user_step(user.tg_id, USER_STEP['SEARCH_TUMAN_'])


        else:
            province_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

            if lan == 'oz':
                province_button.add(*[i.oz for i in Viloyat.objects.all().filter(status=True).order_by('sort')])

            elif lan == 'uz':
                province_button.add(*[i.uz for i in Viloyat.objects.all().filter(status=True).order_by('sort')])

            elif lan == 'ru':
                province_button.add(*[i.ru for i in Viloyat.objects.all().filter(status=True).order_by('sort')])

            province_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])

            bot.send_message(message.from_user.id, LAN[user.lan]['search_viloyat1'], reply_markup=province_button,
                             parse_mode='html')

            set_user_step(user.tg_id, USER_STEP['SEARCH_VILOYAT_'])


    else:
        avto_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])

        bot.send_message(message.from_user.id, LAN[lan]['search_avto'], reply_markup=avto_button,
                         parse_mode='html')
        if category.cat == '4':
            set_user_step(message.from_user.id, USER_STEP['SEARCH_AVTO_POD'])
        else:
            set_user_step(user.tg_id, USER_STEP['SEARCH_AVTO'])


def search_avto_pod(message, bot):
    user = TgUser.objects.get(tg_id=message.chat.id)
    lan = user.lan
    if message.text == LAN[lan]['orqa']:
        search_false = Search.objects.filter(user__tg_id=message.from_user.id, status_check=False, status=False)
        search_true = Search.objects.filter(user__tg_id=message.from_user.id, status=False, status_check=True)

        if search_false.exists():
            search_false.delete()

        if search_true.exists():
            search_true.update(status=True)

        category_button = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        if lan == 'oz':
            category_button.add(*[cat.oz for cat in Category.objects.all().order_by('sort')])
        if lan == 'uz':
            category_button.add(*[cat.uz for cat in Category.objects.all().order_by('sort')])
        if lan == 'ru':
            category_button.add(*[cat.ru for cat in Category.objects.all().order_by('sort')])

        category_button.add(*[LAN[user.lan]['home']])

        bot.send_message(message.from_user.id, LAN[lan]['search_what1'], reply_markup=category_button,
                         parse_mode='html')

        set_user_step(message.from_user.id, USER_STEP['SEARCH_CATEGORY'])

    else:
        avto_pod_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn = []
        avto = None
        if lan == 'oz':
            avto = Avto.objects.get(oz=message.text)
            if avto.avto_pod.all():
                for i in avto.avto_pod.all():
                    btn.append(types.KeyboardButton(text=i.oz))

        if lan == 'uz':
            avto = Avto.objects.get(uz=message.text)
            if avto.avto_pod.all():
                for i in avto.avto_pod.all():
                    btn.append(types.KeyboardButton(text=i.uz))


        if lan == 'ru':
            avto = Avto.objects.get(ru=message.text)
            if avto.avto_pod.all():
                for i in avto.avto_pod.all():
                    btn.append(types.KeyboardButton(text=i.ru))

        Search.objects.filter(user__tg_id=message.chat.id, status_check=False).update(
            avto=avto
        )

        avto_pod_button.add(*btn)
        avto_pod_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])
        bot.send_message(message.from_user.id, LAN[lan]['search_avto_pod'], reply_markup=avto_pod_button,
                         parse_mode='html')

        set_user_step(message.from_user.id, USER_STEP['SEARCH_AVTO_KUB'])


def search_avto_kub(message, bot):
    user = TgUser.objects.get(tg_id=message.chat.id)
    lan = user.lan
    if message.text == LAN[lan]['orqa']:
        user = TgUser.objects.get(tg_id=message.chat.id)
        lan = user.lan

        search = Search.objects.filter(user__tg_id=message.from_user.id, status_check=False, status=False).first()
        avto_button = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        if lan == 'oz':
            if search.category.cat == '4':
                btn = [avto.oz for avto in Avto.objects.filter(is_special=True)]
            else:
                btn = [avto.oz for avto in Avto.objects.filter(is_special=False)]

            avto_button.add(*btn)

        if lan == 'uz':
            if search.category.cat == '4':
                btn = [avto.uz for avto in Avto.objects.filter(is_special=True)]
            else:
                btn = [avto.uz for avto in Avto.objects.filter(is_special=False)]

            avto_button.add(*btn)

        if lan == 'ru':
            if search.category.cat == '4':
                btn = [avto.ru for avto in Avto.objects.filter(is_special=True)]
            else:
                btn = [avto.ru for avto in Avto.objects.filter(is_special=False)]

            avto_button.add(*btn)

        avto_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])

        bot.send_message(message.from_user.id, LAN[lan]['search_avto'], reply_markup=avto_button,
                         parse_mode='html')

        if search.category.cat == '4':
            set_user_step(message.from_user.id, USER_STEP['SEARCH_AVTO_POD'])
        else:
            set_user_step(message.from_user.id, USER_STEP['SEARCH_AVTO'])

    else:
        btn = []
        kub_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        avto_pod = None
        if lan == 'oz':
            avto_pod = AvtoPod.objects.filter(oz=message.text).first()
        if lan == 'uz':
            avto_pod = AvtoPod.objects.filter(uz=message.text).first()
        if lan == 'ru':
            avto_pod = AvtoPod.objects.filter(ru=message.text).first()

        Search.objects.filter(user__tg_id=message.chat.id, status_check=False).update(avto_pod=avto_pod)

        avto = Search.objects.filter(user__tg_id=message.chat.id, status_check=False).first().avto

        if avto.kub.exists():
            for j in avto.kub.all():
                btn.append(types.KeyboardButton(text=str(j)))

            kub_button.add(*btn)
            kub_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])
            bot.send_message(message.from_user.id, LAN[lan]['search_avto_kub'], reply_markup=kub_button, parse_mode='html')

            set_user_step(message.from_user.id, USER_STEP['SEARCH_AVTO'])
        else:
            search = Search.objects.filter(user__tg_id=message.chat.id, status_check=False).first()

            if user.province:
                district_button = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                district_button.add(*[LAN[lan]['all_district']])

                search.province = user.province
                search.save()
                if lan == 'oz':
                    district_button.add(
                        *[d.oz for d in Tuman.objects.filter(viloyat=Viloyat.objects.get(oz=user.province.oz))]
                    )

                elif lan == 'uz':

                    district_button.add(
                        *[d.uz for d in Tuman.objects.filter(viloyat=Viloyat.objects.get(uz=user.province.uz))]
                    )

                elif lan == 'ru':
                    district_button.add(
                        *[d.ru for d in Tuman.objects.filter(viloyat=Viloyat.objects.get(ru=user.province.ru))]
                    )

                district_button.add(types.KeyboardButton(text=LAN[lan]['change_province']))

                district_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])

                bot.send_message(message.from_user.id, LAN[lan]['search_tuman1'], reply_markup=district_button,
                                 parse_mode='html')

                set_user_step(message.from_user.id, USER_STEP['SEARCH_TUMAN_'])

            else:

                province_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                if lan == 'oz':
                    province_button.add(*[i.oz for i in Viloyat.objects.all().filter(status=True).order_by('sort')])

                elif lan == 'uz':
                    province_button.add(*[i.uz for i in Viloyat.objects.all().filter(status=True).order_by('sort')])

                elif lan == 'ru':
                    province_button.add(*[i.ru for i in Viloyat.objects.all().filter(status=True).order_by('sort')])

                province_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])
                bot.send_message(message.from_user.id, LAN[user.lan]['search_viloyat1'],
                                 reply_markup=province_button,
                                 parse_mode='html')
                set_user_step(message.from_user.id, USER_STEP['SEARCH_VILOYAT_'])



def search_category_save(message, bot):

    user = TgUser.objects.get(tg_id=message.chat.id)
    lan = user.lan
    if message.text == LAN[lan]['orqa']:
        search = Search.objects.filter(user__tg_id=message.from_user.id, status_check=False, status=False).first()
        if search.category.cat == '4':
            avto = search.avto
            avto_pod_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            btn = []
            if lan == 'oz':
                if avto.avto_pod.all():
                    for i in avto.avto_pod.all():
                        btn.append(types.KeyboardButton(text=i.oz))

            if lan == 'uz':
                if avto.avto_pod.all():
                    for i in avto.avto_pod.all():
                        btn.append(types.KeyboardButton(text=i.uz))

            if lan == 'ru':
                if avto.avto_pod.all():
                    for i in avto.avto_pod.all():
                        btn.append(types.KeyboardButton(text=i.ru))

            avto_pod_button.add(*btn)
            avto_pod_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])
            bot.send_message(message.from_user.id, LAN[lan]['search_avto_pod'], reply_markup=avto_pod_button,
                             parse_mode='html')

            set_user_step(message.from_user.id, USER_STEP['SEARCH_AVTO_KUB'])

        else:

            search_false = Search.objects.filter(user__tg_id=message.from_user.id, status_check=False, status=False)
            search_true = Search.objects.filter(user__tg_id=message.from_user.id, status=False, status_check=True)

            if search_false.exists():
                search_false.delete()

            if search_true.exists():
                search_true.update(status=True)

            category_button = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

            if lan == 'oz':
                category_button.add(*[cat.oz for cat in Category.objects.all().order_by('sort')])
            if lan == 'uz':
                category_button.add(*[cat.uz for cat in Category.objects.all().order_by('sort')])
            if lan == 'ru':
                category_button.add(*[cat.ru for cat in Category.objects.all().order_by('sort')])

            category_button.add(*[LAN[user.lan]['home']])

            bot.send_message(message.from_user.id, LAN[lan]['search_what1'], reply_markup=category_button,
                             parse_mode='html')
            set_user_step(message.from_user.id, USER_STEP['SEARCH_CATEGORY'])

    else:
        search = Search.objects.filter(user__tg_id=message.chat.id, status_check=False).first()

        if user.province:
            district_button = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            district_button.add(*[LAN[lan]['all_district']])

            if lan == 'oz':
                if search.category.cat == '4':
                    kub, unit = message.text.split(' ')
                    avto_kub = AvtoKub.objects.filter(Q(unit=unit) & Q(kub=kub)).first()
                    search.avto_kub = avto_kub
                else:
                    avto = Avto.objects.get(oz=message.text)
                    search.avto = avto

                search.province = user.province
                search.save()

                district_button.add(*[d.oz for d in Tuman.objects.filter(viloyat=Viloyat.objects.get(oz=user.province.oz))])

            elif lan == 'uz':
                if search.category.cat == '4':
                    kub, unit = message.text.split(' ')
                    avto_kub = AvtoKub.objects.filter(Q(unit=unit) & Q(kub=kub)).first()
                    search.avto_kub = avto_kub
                else:
                    avto = Avto.objects.get(uz=message.text)
                    search.avto = avto

                search.province = user.province
                search.save()

                district_button.add(*[d.uz for d in Tuman.objects.filter(viloyat=Viloyat.objects.get(uz=user.province.uz))])

            elif lan == 'ru':
                if search.category.cat == '4':
                    kub, unit = message.text.split(' ')
                    avto_kub = AvtoKub.objects.filter(Q(unit=unit) & Q(kub=kub)).first()
                    search.avto_kub = avto_kub
                else:
                    avto = Avto.objects.get(ru=message.text)
                    search.avto = avto

                search.province = user.province
                search.save()

                district_button.add(*[d.ru for d in Tuman.objects.filter(viloyat=Viloyat.objects.get(ru=user.province.ru))])

            district_button.add(types.KeyboardButton(text=LAN[lan]['change_province']))
            district_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])
            bot.send_message(message.from_user.id, LAN[lan]['search_tuman1'], reply_markup=district_button,
                             parse_mode='html')
            set_user_step(message.from_user.id, USER_STEP['SEARCH_TUMAN_'])

        else:
            if lan == 'oz':
                if search.category.cat == '4':
                    kub, unit = message.text.split(' ')
                    avto_kub = AvtoKub.objects.filter(Q(unit=unit) & Q(kub=kub)).first()
                    search.avto_kub = avto_kub
                else:
                    avto = Avto.objects.get(oz=message.text)
                    search.avto = avto

                search.save()

                province_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

                province_button.add(*[i.oz for i in Viloyat.objects.all().filter(status=True).order_by('sort')])
                province_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])
                bot.send_message(message.from_user.id, LAN[user.lan]['search_viloyat1'], reply_markup=province_button,
                                 parse_mode='html')
                set_user_step(message.from_user.id, USER_STEP['SEARCH_VILOYAT_'])
            elif lan == 'uz':
                if search.category.cat == '4':
                    kub, unit = message.text.split(' ')
                    avto_kub = AvtoKub.objects.filter(Q(unit=unit) & Q(kub=kub)).first()
                    search.avto_kub = avto_kub
                else:
                    avto = Avto.objects.get(uz=message.text)
                    search.avto = avto

                search.save()
                province_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                # province_button.add(*[LAN[lan]['change_province']])
                province_button.add(*[i.uz for i in Viloyat.objects.all().filter(status=True).order_by('sort')])
                # province_button.add(*[LAN[user.lan]['share_location']])
                province_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])
                bot.send_message(message.from_user.id, LAN[user.lan]['search_viloyat1'], reply_markup=province_button,
                                 parse_mode='html')
                set_user_step(message.from_user.id, USER_STEP['SEARCH_VILOYAT_'])
            elif lan == 'ru':
                if search.category.cat == '4':
                    kub, unit = message.text.split(' ')
                    avto_kub = AvtoKub.objects.filter(Q(unit=unit) & Q(kub=kub)).first()
                    search.avto_kub = avto_kub
                else:
                    avto = Avto.objects.get(ru=message.text)
                    search.avto = avto

                search.save()
                province_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                # province_button.add(*[LAN[lan]['change_province']])
                province_button.add(*[i.ru for i in Viloyat.objects.all().filter(status=True).order_by('sort')])
                # province_button.add(*[LAN[user.lan]['share_location']])
                province_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])
                bot.send_message(message.from_user.id, LAN[user.lan]['search_viloyat1'], reply_markup=province_button,
                                 parse_mode='html')
                set_user_step(message.from_user.id, USER_STEP['SEARCH_VILOYAT_'])


def search_province_save(message, bot):
    user = TgUser.objects.get(tg_id = message.chat.id)
    lan = user.lan
    if message.text == LAN[lan]['orqa']:
        category = Search.objects.filter(user__tg_id=message.from_user.id, status_check=False,
                                         status=False).first().category

        if category.cat == '4':
            btn = []
            kub_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            avto = Search.objects.filter(user__tg_id=message.chat.id, status_check=False).first().avto

            if avto.kub.exists():
                for j in avto.kub.all():
                    btn.append(types.KeyboardButton(text=str(j)))

                kub_button.add(*btn)
                kub_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])
                bot.send_message(message.from_user.id, LAN[lan]['search_avto_kub'], reply_markup=kub_button,
                                 parse_mode='html')

                set_user_step(message.from_user.id, USER_STEP['SEARCH_AVTO'])

            else:

                search = Search.objects.filter(user__tg_id=message.from_user.id, status_check=False, status=False).first()

                if search.category.cat == '4':

                    avto = search.avto

                    avto_pod_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

                    btn = []

                    if lan == 'oz':

                        if avto.avto_pod.all():

                            for i in avto.avto_pod.all():
                                btn.append(types.KeyboardButton(text=i.oz))

                    if lan == 'uz':
                        if avto.avto_pod.all():

                            for i in avto.avto_pod.all():
                                btn.append(types.KeyboardButton(text=i.uz))
                    if lan == 'ru':
                        if avto.avto_pod.all():

                            for i in avto.avto_pod.all():
                                btn.append(types.KeyboardButton(text=i.ru))

                    avto_pod_button.add(*btn)
                    avto_pod_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])
                    bot.send_message(message.from_user.id, LAN[lan]['search_avto_pod'], reply_markup=avto_pod_button,

                                     parse_mode='html')
                    set_user_step(message.from_user.id, USER_STEP['SEARCH_AVTO_KUB'])
                else:

                    search_false = Search.objects.filter(user__tg_id=message.from_user.id, status_check=False, status=False)

                    search_true = Search.objects.filter(user__tg_id=message.from_user.id, status=False, status_check=True)

                    if search_false.exists():
                        search_false.delete()

                    if search_true.exists():
                        search_true.update(status=True)

                    category_button = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

                    if lan == 'oz':
                        category_button.add(*[cat.oz for cat in Category.objects.all().order_by('sort')])

                    if lan == 'uz':
                        category_button.add(*[cat.uz for cat in Category.objects.all().order_by('sort')])

                    if lan == 'ru':
                        category_button.add(*[cat.ru for cat in Category.objects.all().order_by('sort')])

                    category_button.add(*[LAN[user.lan]['home']])

                    bot.send_message(message.from_user.id, LAN[lan]['search_what1'], reply_markup=category_button,

                                     parse_mode='html')

                    set_user_step(message.from_user.id, USER_STEP['SEARCH_CATEGORY'])

        else:
            search_false = Search.objects.filter(user__tg_id=message.from_user.id, status_check=False, status=False)
            # search_true = Search.objects.filter(user__tg_id=message.from_user.id, status=False, status_check=True)

            if search_false.exists():
                search_false.delete()

            # if search_true.exists():
            #     search_true.update(status=True)

            if category.cat == '3':
                search_false = Search.objects.filter(user__tg_id=message.from_user.id, status_check=False, status=False)
                search_true = Search.objects.filter(user__tg_id=message.from_user.id, status=False, status_check=True)

                if search_false.exists():
                    search_false.delete()

                if search_true.exists():
                    search_true.update(status=True)

                category_button = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

                if lan == 'oz':
                    category_button.add(*[cat.oz for cat in Category.objects.all().order_by('sort')])
                if lan == 'uz':
                    category_button.add(*[cat.uz for cat in Category.objects.all().order_by('sort')])
                if lan == 'ru':
                    category_button.add(*[cat.ru for cat in Category.objects.all().order_by('sort')])

                category_button.add(*[LAN[user.lan]['home']])

                bot.send_message(message.from_user.id, LAN[lan]['search_what1'], reply_markup=category_button,
                                 parse_mode='html')
                set_user_step(message.from_user.id, USER_STEP['SEARCH_CATEGORY'])
            else:

                Search.objects.create(
                    user=user,
                    category=category
                )

                avto_button = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

                if lan == 'oz':
                    if category.cat == '4':
                        btn = [avto.oz for avto in Avto.objects.filter(is_special=True)]
                    else:
                        btn = [a.oz for a in Avto.objects.filter(is_special=False)]

                    avto_button.add(*btn)

                if lan == 'uz':
                    if category.cat == '4':
                        btn = [avto.uz for avto in Avto.objects.filter(is_special=True)]
                    else:
                        btn = [a.uz for a in Avto.objects.filter(is_special=False)]

                    avto_button.add(*btn)

                if lan == 'ru':
                    if category.cat == '4':
                        btn = [avto.ru for avto in Avto.objects.filter(is_special=True)]
                    else:
                        btn = [a.ru for a in Avto.objects.filter(is_special=False)]

                    avto_button.add(*btn)

                avto_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])

                bot.send_message(message.from_user.id, LAN[lan]['search_avto'], reply_markup=avto_button,
                                 parse_mode='html')
                set_user_step(message.from_user.id, USER_STEP['SEARCH_AVTO'])

    else:
        district_button = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        district_button.add(*[LAN[lan]['all_district']])
        if lan == 'oz':
            province = Viloyat.objects.get(oz=message.text)
            if Viloyat.objects.filter(oz = message.text).exists():
                search = Search.objects.filter(
                    user__tg_id=message.chat.id,
                    status_check=False
                ).update(
                    province=province
                )

            district_button.add(*[d.oz for d in Tuman.objects.filter(viloyat=province)])

        elif lan == 'uz':
            province = Viloyat.objects.get(uz = message.text)
            user = TgUser.objects.get(tg_id=message.chat.id)
            if Viloyat.objects.filter(uz = message.text).exists():
                Search.objects.filter(
                    user__tg_id = message.chat.id,
                    status_check = False
                ).update(
                    province=province
                )

            district_button.add(*[d.uz for d in Tuman.objects.filter(viloyat=province)])

        elif lan == 'ru':
            province = Viloyat.objects.get(ru = message.text)
            user = TgUser.objects.get(tg_id=message.chat.id)

            if Viloyat.objects.filter(ru=message.text).exists():
                Search.objects.filter(
                    user__tg_id = message.chat.id,
                    status_check = False
                ).update(
                    province = province
                )

            district_button.add(*[d.ru for d in Tuman.objects.filter(viloyat=province)])

        district_button.add(types.KeyboardButton(text=LAN[lan]['change_province']))
        district_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])
        bot.send_message(message.from_user.id, LAN[lan]['search_tuman1'], reply_markup=district_button, parse_mode='html')
        user = TgUser.objects.filter(tg_id=message.chat.id).update(province=province)
        set_user_step(message.from_user.id, USER_STEP['SEARCH_TUMAN_'])


def search_district_save(message, bot):
    user = TgUser.objects.get(tg_id = message.chat.id)
    lan = user.lan
    if message.text == LAN[lan]['orqa']:
        # if Search.objects.filter(user__tg_id=message.chat.id, status_check=True).exists():
        #     Search.objects.filter(user__tg_id=message.chat.id, status_check=True).update(status_check=False)
        Search.objects.filter(
            user__tg_id=message.chat.id,
            status_check=False
        ).first().province = None
        if lan == 'oz':
            province_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            province_button.add(*[i.oz for i in Viloyat.objects.all().filter(status=True).order_by('sort')])
            province_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])
            bot.send_message(message.from_user.id, LAN[user.lan]['search_viloyat1'], reply_markup=province_button, parse_mode = 'html')
            set_user_step(message.from_user.id, USER_STEP['SEARCH_VILOYAT_'])
        elif lan == 'uz':
            province_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            province_button.add(*[i.uz for i in Viloyat.objects.all().filter(status=True).order_by('sort')])
            province_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])
            bot.send_message(message.from_user.id, LAN[user.lan]['search_viloyat1'], reply_markup=province_button, parse_mode = 'html')
            set_user_step(message.from_user.id, USER_STEP['SEARCH_VILOYAT_'])
        elif lan == 'ru':
            province_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            province_button.add(*[i.ru for i in Viloyat.objects.all().filter(status=True).order_by('sort')])
            province_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])
            bot.send_message(message.from_user.id, LAN[user.lan]['search_viloyat1'], reply_markup=province_button, parse_mode = 'html')
            set_user_step(message.from_user.id, USER_STEP['SEARCH_VILOYAT_'])

    elif message.text == LAN[lan]['change_province']:
        user = TgUser.objects.filter(tg_id=message.chat.id).first()
        user.province = None
        user.save()
        province_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        if lan == 'oz':
            province_button.add(*[i.oz for i in Viloyat.objects.all().filter(status=True).order_by('sort')])

        elif lan == 'uz':
            province_button.add(*[i.uz for i in Viloyat.objects.all().filter(status=True).order_by('sort')])

        elif lan == 'ru':
            province_button.add(*[i.ru for i in Viloyat.objects.all().filter(status=True).order_by('sort')])

        province_button.add(*[LAN[lan]['orqa'], LAN[lan]['home']])
        bot.send_message(message.from_user.id, LAN[user.lan]['change_province'], reply_markup=province_button,
                         parse_mode='html')
        bot.send_message(message.from_user.id, LAN[user.lan]['search_viloyat1'], reply_markup=province_button,
                         parse_mode='html')
        set_user_step(message.from_user.id, USER_STEP['SEARCH_VILOYAT_'])

    else:
        if lan == 'oz':
            if Tuman.objects.filter(oz=message.text).exists():
                if Search.objects.filter(user__tg_id = message.chat.id, status_check = False).exists():
                    Search.objects.filter(
                        user__tg_id = message.chat.id,
                        status_check = False
                    ).update(
                        status_check = True,
                        district=Tuman.objects.get(oz=message.text)
                    )
                else:
                    Search.objects.filter(
                        user__tg_id=message.chat.id,
                        status_check=True
                    ).update(
                        district=Tuman.objects.get(oz=message.text)
                    )
            else:
                Search.objects.filter(
                    user__tg_id=message.chat.id,
                    status_check=False
                ).update(
                    status_check=True
                )

            search = Search.objects.filter(user__tg_id = message.chat.id, status_check = True, status = False).first()
            if search.category.cat == '3':
                search_obj = UserCart.objects.filter(
                    category__oz=search.category.oz,
                    status=1,
                ).order_by('-date_sort')
            elif search.category.cat == '4':
                search_obj = UserCart.objects.filter(
                    category__oz=search.category.oz,
                    avto__oz=search.avto.oz,
                    avto_pod__oz=search.avto_pod.oz,
                    kub=search.avto_kub,
                    status=1
                ).order_by('-date_sort')
            else:
                returned_autos = UserCart.objects.filter(
                    Q(category__oz=search.category.oz,
                    avto__oz=search.avto.oz,
                    status=1)
                ).order_by('-date_sort')

                returned_filter_by_district = []
                if search.district:
                    returned_filter_by_district = returned_autos.filter(
                        tuman__oz=search.district.oz
                    )
                    returned_filter_by_district = list(set(returned_filter_by_district) - set(returned_autos))


                other_autos = UserCart.objects.filter(
                    category__oz=search.category.oz,
                    viloyat__oz=search.province.oz,
                    status=1
                ).order_by('-date_sort')

                other_autos = list(set(other_autos) - set(returned_autos))

                # search_obj = returned_autos.union(other_autos) if returned_autos else other_autos
                search_obj = list(returned_autos) + list(returned_filter_by_district) + list(other_autos) or UserCart.objects.none() #returned_autos.union(returned_filter_by_district, all=False).union(other_autos, all=False) or UserCart.objects.none()

            try:
                if isinstance(search_obj, QuerySet):
                    if search.district:
                        if search_obj.filter(category_id__in=(3, 4)):
                            districts_ads = search_obj.filter(
                                tuman__oz=search.district.oz
                            ).order_by('-date_sort')

                            other_districts_ads = search_obj.filter(
                                viloyat__oz=search.province.oz,
                            ).exclude(
                                Q(tuman__oz=search.district.oz) | Q(tuman=None)
                            ).order_by('-date_sort')

                            search_obj = list(districts_ads) + list(other_districts_ads)

                    else:
                        search_obj = search_obj.filter(
                            viloyat__oz=search.province.oz,
                            status=1
                        )

                    if search_obj:
                        pass
                    else:
                        if search.category.cat == '3':
                            search_obj = UserCart.objects.filter(
                                category__oz=search.category.oz,
                                status=1,
                            ).order_by('-date_sort')

                        elif search.category.cat == '4':
                            search_obj = UserCart.objects.filter(
                                category__oz=search.category.oz,
                                avto__oz=search.avto.oz,
                                avto_pod__oz=search.avto_pod.oz,
                                kub=search.avto_kub,
                                status=1
                            ).order_by('-date_sort')

                        else:
                            returned_autos = UserCart.objects.filter(
                                category__oz=search.category.oz,
                                avto__oz=search.avto.oz,
                                status=1
                            ).order_by('-date_sort')

                            other_autos = UserCart.objects.filter(
                                category__oz=search.category.oz,
                                viloyat__oz=search.province.oz,
                                status=1
                            ).exclude(returned_autos).order_by('-date_sort')

                            search_obj = other_autos if not(returned_autos) else returned_autos.union(returned_autos, all=False)
                            # search_obj = returned_autos.union(other_autos)

                        search_obj = search_obj.filter(
                            viloyat__oz=search.province.oz,
                            status=1,
                        ).order_by('-date_sort')
            except Exception as e:
                print(e)

            paginator = Paginator(search_obj, Service.get_count(Config.objects.all()))
            search_object = paginator.get_page(1)
            district_button = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            district_button.add(*[LAN[lan]['all_district']])
            district_button.add(*[d.oz for d in Tuman.objects.filter(viloyat=Viloyat.objects.get(uz=user.province.uz))])
            # district_button.add(*[LAN[user.lan]['orqa']])
            district_button.add(*[LAN[user.lan]['home']])

            if search_object:
                for i in search_object:
                    sendtextoz = ''
                    UserCart.objects.filter(id=i.id).update(date_sort=timezone.now())
                    if i.podcategory:
                        pcat = i.podcategory.oz
                    else:
                        pcat = ''
                    if i.avto:
                        avto = i.avto.oz
                    else:
                        avto = '---'
                    if i.kub:
                        kub = f'{i.kub.kub} {i.kub.unit}'
                    else:
                        kub = '---'
                    if i.username:
                        usern = '@'+i.username
                    else:
                        usern = '<a href="tg://user?id={0}">{1}</a>'.format(i.user.tg_id, i.user)

                    sendtextoz += "\n"
                    sendtextoz += LAN[lan]['category'] + f"{i.category.oz}, "
                    sendtextoz += f"{pcat}\n"
                    if i.category.cat != '3':
                        sendtextoz += LAN[lan]['avto'] + f"{avto}, {kub}"
                    sendtextoz += '\n'+LAN[lan]['province'] + f"{i.viloyat.oz}\n"
                    sendtextoz += LAN[lan]['district'] + f"{i.tuman.oz}\n\n"
                    sendtextoz += f"✏️ {usern}\n\n"
                    sendtextoz += f"☎️ {i.telefon}\n\n"
                    if i.img_id:
                        img_id = i.img_id
                    else:
                        img_id = i.category.image_id
                    if img_id.endswith('jpg') or img_id.endswith('png') or img_id.endswith('jpeg') or img_id.endswith('svg'):
                        img_id = open(img_id, 'rb')
                    bot.send_photo(
                        message.chat.id,
                        img_id,
                        sendtextoz,
                        parse_mode = 'html',
                        reply_markup = district_button
                    )
                if (paginator.count) > int(Service.get_count(Config.objects.all())):
                    btnsearch = types.InlineKeyboardMarkup()
                    btnsearch.row(types.InlineKeyboardButton(text=LAN[lan]['more'], callback_data=f'search_{search_object.next_page_number()}'))
                    bot.send_message(message.chat.id, LAN[lan]['more_text'], parse_mode="HTML", reply_markup=btnsearch)
            else:
                bot.send_message(message.chat.id, LAN[lan]['search_not_found'], parse_mode = 'html', reply_markup=district_button)


        if lan == 'uz':
            if Tuman.objects.filter(uz=message.text).exists():
                if Search.objects.filter(user__tg_id=message.chat.id, status_check=False).exists():
                    Search.objects.filter(
                        user__tg_id=message.chat.id,
                        status_check=False
                    ).update(
                        status_check=True,
                        district=Tuman.objects.get(uz=message.text)
                    )
                else:
                    Search.objects.filter(
                        user__tg_id=message.chat.id,
                        status_check=True
                    ).update(
                        district=Tuman.objects.get(uz=message.text)
                    )
            else:
                Search.objects.filter(
                    user__tg_id=message.chat.id,
                    status_check=False
                ).update(
                    status_check=True
                )

            # if Tuman.objects.filter(uz = message.text).exists():
            #     Search.objects.filter(
            #         user__tg_id = message.chat.id,
            #         status_check = False
            #     ).update(
            #         district = Tuman.objects.get(uz = message.text)
            #     )

            search = Search.objects.filter(user__tg_id=message.chat.id, status_check=True, status=False).first()
            if search.category.cat == '3':
                search_obj = UserCart.objects.filter(
                    category__uz=search.category.uz,
                    status=1,
                ).order_by('-date_sort')

            elif search.category.cat == '4':
                search_obj = UserCart.objects.filter(
                    category__uz=search.category.uz,
                    avto__uz=search.avto.uz,
                    avto_pod__uz=search.avto_pod.uz,
                    kub=search.avto_kub,
                    status=1
                ).order_by('-date_sort')

            else:
                returned_autos = UserCart.objects.filter(
                    Q(category__uz=search.category.uz,
                      avto__uz=search.avto.uz,
                      status=1)
                ).order_by('-date_sort')

                returned_filter_by_district = []
                if search.district:
                    returned_filter_by_district = returned_autos.filter(
                        tuman__uz=search.district.uz
                    )
                    returned_filter_by_district = list(set(returned_filter_by_district) - set(returned_autos))



                other_autos = UserCart.objects.filter(
                    category__uz=search.category.uz,
                    viloyat__uz=search.province.uz,
                    status=1
                ).order_by('-date_sort')

                other_autos = list(set(other_autos) - set(returned_autos))

                # search_obj = returned_autos.union(other_autos) if returned_autos else other_autos
                search_obj = list(returned_autos) + list(returned_filter_by_district) + list(
                    other_autos) or UserCart.objects.none()  # returned_autos.union(returned_filter_by_district, all=False).union(other_autos, all=False) or UserCart.objects.none()

            if isinstance(search_obj, QuerySet):
                if search.district:
                    if search_obj.filter(category_id__in=(3, 4)):
                        districts_ads = search_obj.filter(
                            tuman__uz=search.district.uz
                        ).order_by('-date_sort')

                        other_districts_ads = search_obj.filter(
                            viloyat__uz=search.province.uz,
                        ).exclude(
                            Q(tuman__uz=search.district.uz) | Q(tuman=None)
                        ).order_by('-date_sort')

                        search_obj = list(districts_ads) + list(other_districts_ads)

                else:
                    search_obj = search_obj.filter(
                        viloyat__uz=search.province.uz,
                        status=1
                    )

            if search_obj:
                pass
            else:
                if search.category.cat == '3':
                    search_obj = UserCart.objects.filter(
                        category__uz=search.category.uz,
                        status=1,
                    ).order_by('-date_sort')

                elif search.category.cat == '4':
                    search_obj = UserCart.objects.filter(
                        category__uz=search.category.uz,
                        avto__uz=search.avto.uz,
                        avto_pod__uz=search.avto_pod.uz,
                        kub=search.avto_kub,
                        status=1
                    ).order_by('-date_sort')

                else:
                    search_obj = UserCart.objects.filter(
                        category__uz=search.category.uz,
                        avto__uz=search.avto.uz,
                        status=1,
                    ).order_by('-date_sort')

                search_obj = search_obj.filter(
                    viloyat=Viloyat.objects.get(
                        uz=search.province.uz
                    ),
                    status=1,
                ).order_by('-date_sort')

            paginator = Paginator(search_obj, Service.get_count(Config.objects.all()))
            search_object = paginator.get_page(1)
            district_button = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            district_button.add(*[LAN[lan]['all_district']])
            district_button.add(*[d.uz for d in Tuman.objects.filter(viloyat=Viloyat.objects.get(uz=user.province.uz))])
            # district_button.add(*[LAN[user.lan]['orqa']])
            district_button.add(*[LAN[user.lan]['home']])

            if search_object:
                for i in search_object:
                    sendtextuz = ''
                    UserCart.objects.filter(id=i.id).update(date_sort=timezone.now())
                    if i.podcategory:
                        pcat = i.podcategory.uz
                    else:
                        pcat = ''
                    if i.avto:
                        avto = i.avto.uz
                    else:
                        avto = '---'
                    if i.kub:
                        kub = f'{i.kub.kub} {i.kub.unit}'
                    else:
                        kub = '---'
                    if i.username:
                        usern = '@' + i.username
                    else:
                        usern = '<a href="tg://user?id={0}">{1}</a>'.format(i.user.tg_id, i.user)

                    sendtextuz += "\n"
                    sendtextuz += LAN[lan]['category'] + f"{i.category.uz}, "
                    sendtextuz += f"{pcat}\n"
                    if i.category.cat != '3':
                        sendtextuz += LAN[lan]['avto'] + f"{avto}, {kub}"
                    sendtextuz += '\n' + LAN[lan]['province'] + f"{i.viloyat.uz}\n"
                    sendtextuz += LAN[lan]['district'] + f"{i.tuman.uz}\n\n"
                    sendtextuz += f"✏️ {usern}\n\n"
                    sendtextuz += f"☎️ {i.telefon}\n\n"
                    if i.img_id:
                        img_id = i.img_id
                    else:
                        img_id = i.category.image_id

                    if img_id.endswith('jpg') or img_id.endswith('png') or img_id.endswith('jpeg') or img_id.endswith('svg'):
                        img_id = open(img_id, 'rb')

                    bot.send_photo(
                        message.chat.id,
                        img_id,
                        sendtextuz,
                        parse_mode='html',
                        reply_markup=district_button
                    )
                if (paginator.count) > int(Service.get_count(Config.objects.all())):
                    btnsearch = types.InlineKeyboardMarkup()
                    btnsearch.row(types.InlineKeyboardButton(text=LAN[lan]['more'],
                                                             callback_data=f'search_{search_object.next_page_number()}'))
                    bot.send_message(message.chat.id, LAN[lan]['more_text'], parse_mode="HTML", reply_markup=btnsearch)
            else:
                bot.send_message(message.chat.id, LAN[lan]['search_not_found'], parse_mode='html',
                                 reply_markup=district_button)

        if lan == 'ru':
            if Tuman.objects.filter(ru=message.text).exists():
                if Search.objects.filter(user__tg_id=message.chat.id, status_check=False).exists():
                    Search.objects.filter(
                        user__tg_id=message.chat.id,
                        status_check=False
                    ).update(
                        status_check=True,
                        district=Tuman.objects.get(ru=message.text)
                    )
                else:
                    Search.objects.filter(
                        user__tg_id=message.chat.id,
                        status_check=True
                    ).update(
                        district=Tuman.objects.get(ru=message.text)
                    )
            else:
                Search.objects.filter(
                    user__tg_id=message.chat.id,
                    status_check=False
                ).update(
                    status_check=True
                )

            search = Search.objects.filter(user__tg_id=message.chat.id, status_check=True, status=False).first()
            if search.category.cat == '3':
                search_obj = UserCart.objects.filter(
                    category__ru=search.category.ru,
                    status=1,
                ).order_by('-date_sort')

            elif search.category.cat == '4':
                search_obj = UserCart.objects.filter(
                    category__ru=search.category.ru,
                    avto__ru=search.avto.ru,
                    avto_pod__ru=search.avto_pod.ru,
                    kub=search.avto_kub,
                    status=1
                ).order_by('-date_sort')

            else:
                returned_autos = UserCart.objects.filter(
                    Q(category__ru=search.category.ru,
                      avto__ru=search.avto.ru,
                      status=1)
                ).order_by('-date_sort')

                returned_filter_by_district = []
                if search.district:
                    returned_filter_by_district = returned_autos.filter(
                        tuman__ru=search.district.ru
                    )
                    returned_filter_by_district = list(set(returned_filter_by_district) - set(returned_autos))

                other_autos = UserCart.objects.filter(
                    category__ru=search.category.ru,
                    viloyat__ru=search.province.ru,
                    status=1
                ).order_by('-date_sort')

                other_autos = list(set(other_autos) - set(returned_autos))

                # search_obj = returned_autos.union(other_autos) if returned_autos else other_autos
                search_obj = list(returned_autos) + list(returned_filter_by_district) + list(
                    other_autos) or UserCart.objects.none()  # returned_autos.union(returned_filter_by_district, all=False).union(other_autos, all=False) or UserCart.objects.none()

            if isinstance(search_obj, QuerySet):
                if search.district:
                    if search_obj.filter(category_id__in=(3, 4)):
                        districts_ads = search_obj.filter(
                            tuman__ru=search.district.ru
                        ).order_by('-date_sort')

                        other_districts_ads = search_obj.filter(
                            viloyat__ru=search.province.ru,
                        ).exclude(
                            Q(tuman__ru=search.district.ru) | Q(tuman=None)
                        ).order_by('-date_sort')

                        search_obj = list(districts_ads) + list(other_districts_ads)

                else:
                    search_obj = search_obj.filter(
                        viloyat__ru=search.province.ru,
                        status=1
                    )
            if search_obj:
                pass
            else:
                if search.category.cat == '3':
                    search_obj = UserCart.objects.filter(
                        category__ru=search.category.ru,
                        status=1,
                    ).order_by('-date_sort')

                elif search.category.cat == '4':
                    search_obj = UserCart.objects.filter(
                        category__ru=search.category.ru,
                        avto__ru=search.avto.ru,
                        avto_pod__ru=search.avto_pod.ru,
                        kub=search.avto_kub,
                        status=1
                    ).order_by('-date_sort')

                else:
                    search_obj = UserCart.objects.filter(
                        category__ru=search.category.ru,
                        avto__ru=search.avto.ru,
                        status=1,
                    ).order_by('-date_sort')

                search_obj = search_obj.filter(
                    viloyat=Viloyat.objects.get(
                        ru=search.province.ru
                    ),
                    status=1,
                ).order_by('-date_sort')

            paginator = Paginator(search_obj, Service.get_count(Config.objects.all()))
            search_object = paginator.get_page(1)
            district_button = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            district_button.add(*[LAN[lan]['all_district']])
            district_button.add(*[d.ru for d in Tuman.objects.filter(viloyat=Viloyat.objects.get(uz=user.province.uz))])
            # district_button.add(*[LAN[user.lan]['orqa']])
            district_button.add(*[LAN[user.lan]['home']])

            if search_object:
                for i in search_object:
                    sendtextru = ''
                    UserCart.objects.filter(id=i.id).update(date_sort=timezone.now())
                    if i.podcategory:
                        pcat = i.podcategory.ru
                    else:
                        pcat = ''
                    if i.avto:
                        avto = i.avto.ru
                    else:
                        avto = '---'
                    if i.kub:
                        kub = f'{i.kub.kub} {i.kub.unit}'
                    else:
                        kub = '---'
                    if i.username:
                        usern = '@' + i.username
                    else:
                        usern = '<a href="tg://user?id={0}">{1}</a>'.format(i.user.tg_id, i.user)

                    sendtextru += "\n"
                    sendtextru += LAN[lan]['category'] + f"{i.category.ru}, "
                    sendtextru += f"{pcat}\n"
                    if i.category.cat != '3':
                        sendtextru += LAN[lan]['avto'] + f"{avto}, {kub}"
                    sendtextru += '\n' + LAN[lan]['province'] + f"{i.viloyat.ru}\n"
                    sendtextru += LAN[lan]['district'] + f"{i.tuman.ru}\n\n"
                    sendtextru += f"✏️ {usern}\n\n"
                    sendtextru += f"☎️ {i.telefon}\n\n"
                    if i.img_id:
                        img_id = i.img_id
                    else:
                        img_id = i.category.image_id

                    if img_id.endswith('jpg') or img_id.endswith('png') or img_id.endswith('jpeg') or img_id.endswith('svg'):
                        img_id = open(img_id, 'rb')

                    bot.send_photo(
                        message.chat.id,
                        img_id,
                        sendtextru,
                        parse_mode='html',
                        reply_markup=district_button
                    )
                if (paginator.count) > int(Service.get_count(Config.objects.all())):
                    btnsearch = types.InlineKeyboardMarkup()
                    btnsearch.row(types.InlineKeyboardButton(text=LAN[lan]['more'],
                                                             callback_data=f'search_{search_object.next_page_number()}'))
                    bot.send_message(message.chat.id, LAN[lan]['more_text'], parse_mode="HTML", reply_markup=btnsearch)
            else:
                bot.send_message(message.chat.id, LAN[lan]['search_not_found'], parse_mode='html',
                                 reply_markup=district_button)

