import threading
import uuid
from datetime import timedelta

from django.core.cache import cache
from django.db import transaction, IntegrityError
from liqpay import LiqPay

import stripe
from cloudipsp import Api, Checkout
from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .forms import UkraineDeliveryForm, WorldDeliveryForm
from .models import ProcessedToken, Order
import hashlib


def index(request):
    return render(request, 'main/btsbook_ua.html')


def index_en(request):
    return render(request, 'main/btsbook_en.html')


def validate_and_process_token(token):
    print(f"Проверка токена: {token}")
    try:
        with transaction.atomic():
            token_entry, created = ProcessedToken.objects.get_or_create(
                token=token, defaults={'is_processed': True, 'email_sent': False}
            )
            if token_entry.email_sent:
                print(f"[INFO] Письмо уже отправлено для токена: {token}")
                return False  # Предотвращаем повторную отправку
            print(f"Токен успешно обработан: {token}")
            return True
    except IntegrityError:
        print(f"Дублирующий запрос для токена: {token}")
        return False


def async_send_emails(order_data, context):
    email = order_data['email']
    subject_user = "Order Confirmation - Book Purchase" if context[
                                                               'language'] == 'en' else "Підтвердження замовлення книги"
    user_email_template = 'main/email_template_en.html' if context[
                                                               'language'] == 'en' else 'main/email_template_ua.html'

    # Отправка письма пользователю
    email_content = render_to_string(user_email_template, context)
    user_message = EmailMessage(subject=subject_user, body=email_content, from_email="ваш_почтовый_адрес@gmail.com",
                                to=[email])
    user_message.content_subtype = "html"
    user_message.send()

    # Отправка письма админу
    admin_message = (
        f"Нове замовлення книги:\n\n"
        f"Iм'я: {context['first_name']}\n"
        f"Прізвище: {context['last_name']}\n"
        f"Країна: {context['country']}\n"
        f"Місто: {context['city']}\n"
        f"Почтовий індекс: {context['postal_code']}\n"
        f"Адреса доставки: {context['address']}\n"
        f"Телефон клієнта: {context['phone']}\n"
        f"Додаткова інформація: {context['additional_info']}\n"
        f"Email клієнта: {email}\n"
        f"Тип доставки: {'Україна' if context['delivery_type'] == 'ukraine' else 'Світ'}\n"
        f"Ціна: {context['price']} €\n"
    )
    send_mail(subject="New Book Order Received", message=admin_message, from_email="ваш_почтовый_адрес@gmail.com",
              recipient_list=["basingerfelix17@gmail.com"])

    # Обновляем флаг, чтобы предотвратить дублирование писем
    ProcessedToken.objects.filter(token=order_data['token']).update(email_sent=True)
    print("Письма отправлены успешно.")


def submit_ukraine_form(request):
    if request.method == "POST":
        form = UkraineDeliveryForm(request.POST)
        if form.is_valid():
            # Сохраняем данные в сессию для дальнейшего использования после успешной оплаты
            request.session['delivery_data'] = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'phone': form.cleaned_data['phone'],
                'address': form.cleaned_data['address'],
                'email': form.cleaned_data['email'],
                'delivery_type': 'ukraine'
            }
            return JsonResponse({"success": True, "message": "Дані форми збережені успішно."})
        else:
            return JsonResponse({"success": False, "errors": form.errors})


def submit_world_form(request):
    if request.method == "POST":
        form = WorldDeliveryForm(request.POST)
        if form.is_valid():
            # Сохраняем данные в сессию для дальнейшего использования после успешной оплаты
            request.session['delivery_data'] = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'country': form.cleaned_data['country'],
                'city': form.cleaned_data['city'],
                'postal_code': form.cleaned_data['postal_code'],
                'address': form.cleaned_data['address'],
                'phone': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'additional_info': form.cleaned_data.get('additional_info', ''),
                'delivery_type': 'world'
            }
            return JsonResponse({"success": True, "message": "Дані форми збережені успішно."})
        else:
            return JsonResponse({"success": False, "errors": form.errors})


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request):
    token = str(uuid.uuid4())
    request.session['checkout_token'] = token

    # Получение данных из запроса
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    country = request.POST.get('country', '')
    city = request.POST.get('city', '')
    postal_code = request.POST.get('postal_code', '')
    address = request.POST.get('address')
    phone = request.POST.get('phone')
    additional_info = request.POST.get('additional_info', '')
    email = request.POST.get('email')
    delivery_type = request.POST.get('delivery_type')
    language = request.POST.get('lang', 'ua')
    book_language = request.POST.get('book_language', 'Українська')

    # Проверка корректности типа доставки
    if delivery_type not in ['ukraine', 'world']:
        return JsonResponse({"error": "Некорректный тип доставки."})

    # Установка цены в зависимости от типа доставки
    price = 25 if delivery_type == "ukraine" else 48

    # Сохраняем данные о заказе в сессию
    request.session['order_data'] = {
        'token': token,
        'first_name': first_name,
        'last_name': last_name,
        'country': country,
        'city': city,
        'postal_code': postal_code,
        'address': address,
        'phone': phone,
        'additional_info': additional_info,
        'email': email,
        'delivery_type': delivery_type,
        'price': price,
        'book_language': book_language,
    }

    # Сохраняем заказ в базу данных
    Order.objects.create(
        order_id=token,
        first_name=first_name,
        last_name=last_name,
        country=country,
        city=city,
        postal_code=postal_code,
        address=address,
        phone=phone,
        additional_info=additional_info,
        email=email,
        delivery_type=delivery_type,
        price=price,
        book_language=book_language,
        language=language,
        payment_status='pending'
    )

    # Формирование URL-адресов
    success_url = f"{request.build_absolute_uri(reverse('payment_success'))}?lang={language}"
    cancel_url = f"{request.build_absolute_uri(reverse('payment_cancel'))}?lang={language}"

    # Создание платежной сессии LiqPay
    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    params = {
        'action': 'pay',
        'amount': price,
        'currency': 'EUR',
        'description': 'Оплата книги',
        'order_id': token,
        'version': '3',
        'sandbox': 0,
        'server_url': request.build_absolute_uri(reverse('pay_callback')),
        'result_url': success_url,
        'cancel_url': cancel_url
    }
    signature = liqpay.cnb_signature(params)
    data = liqpay.cnb_data(params)

    return JsonResponse({
        "data": data,
        "signature": signature
    })



@csrf_exempt
def check_payment_status(request):
    order_id = request.GET.get('order_id')
    lang = request.GET.get('lang', 'ua')

    # Здесь предполагается, что статус платежа хранится в базе данных.
    try:
        order = Order.objects.get(order_id=order_id)
        if order.payment_status == 'success':
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failure'})
    except Order.DoesNotExist:
        return JsonResponse({'status': 'failure'})


@csrf_exempt
def pay_callback(request):
    if request.method == "POST":
        try:
            print("Получен POST-запрос от LiqPay:", request.POST)

            liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
            data = request.POST.get('data')
            signature = request.POST.get('signature')

            if not data or not signature:
                return JsonResponse({"error": "Некорректные данные обратного вызова."}, status=400)

            expected_signature = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
            if signature != expected_signature:
                return JsonResponse({"error": "Неверная подпись данных LiqPay."}, status=400)

            decoded_data = liqpay.decode_data_from_str(data)
            status = decoded_data.get('status')
            order_id = decoded_data.get('order_id')

            if not order_id:
                return JsonResponse({"error": "Отсутствует идентификатор заказа."}, status=400)

            print(f"Статус платежа: {status}, Order ID: {order_id}")

            # Получаем заказ из базы
            order = Order.objects.filter(order_id=order_id).first()
            if not order:
                print(f"Ошибка: Заказ с ID {order_id} не найден.")
                return JsonResponse({"error": "Заказ не найден."}, status=400)

            # Обновляем статус заказа в зависимости от результата платежа
            if status in ['success', 'sandbox']:
                order.payment_status = 'success'
                order.save()

                # Формируем контекст для отправки писем
                context = {
                    'first_name': order.first_name,
                    'last_name': order.last_name,
                    'country': order.country,
                    'city': order.city,
                    'postal_code': order.postal_code,
                    'address': order.address,
                    'phone': order.phone,
                    'email': order.email,
                    'delivery_type': order.delivery_type,
                    'price': order.price,
                    'language': order.language,
                    'book_language': order.book_language,
                    'additional_info': order.additional_info
                }

                # Асинхронная отправка писем
                threading.Thread(target=async_send_emails, args=(context, context)).start()

                return JsonResponse({"status": "success", "message": "Платеж подтвержден."}, status=200)
            else:
                order.payment_status = 'failure'
                order.save()
                print(f"Ошибка или отмена платежа: {decoded_data.get('err_description', 'Причина неизвестна')}")
                return JsonResponse({"status": "failure"}, status=200)

        except Exception as e:
            print(f"Ошибка при обработке LiqPay callback: {e}")
            return JsonResponse({"error": "Внутренняя ошибка сервера."}, status=500)
    else:
        return JsonResponse({"error": "Неверный метод запроса."}, status=405)





def payment_success(request):
    token = request.session.get('checkout_token')
    if not token:
        print("Отсутствует токен в сессии.")
        return redirect('payment_cancel_en' if request.GET.get('lang', 'en') == 'en' else 'payment_cancel_ua')

    # Проверка статуса платежа по токену
    order = Order.objects.filter(order_id=token).first()
    if not order:
        print(f"Ошибка: Заказ с токеном {token} не найден.")
        return redirect('payment_cancel_en' if request.GET.get('lang', 'en') == 'en' else 'payment_cancel_ua')

    # Проверяем, что платеж успешен
    if order.payment_status not in ['success', 'sandbox']:
        print(f"Ошибка: Платеж для заказа {token} не был успешным.")
        return redirect('payment_cancel_en' if request.GET.get('lang', 'en') == 'en' else 'payment_cancel_ua')

    # Удаляем данные из сессии, если платеж успешен
    request.session.pop('checkout_token', None)
    request.session.pop('order_data', None)

    # Формируем контекст для отображения успешной страницы
    context = {
        'first_name': order.first_name,
        'last_name': order.last_name,
        'phone': order.phone,
        'email': order.email,
        'address': order.address,
        'book_language': order.book_language,
        'delivery_type': "Доставка по Україні" if order.delivery_type == "ukraine" else "Доставка по світу",
        'price': order.price,
        'country': order.country,
        'city': order.city,
        'postal_code': order.postal_code,
        'additional_info': order.additional_info,
        'language': request.GET.get('lang', 'uk')
    }

    # Перенаправляем на страницу успешной оплаты
    return redirect('payment_success_en' if context['language'] == 'en' else 'payment_success_ua')


def clear_old_tokens():
    ProcessedToken.objects.filter(created_at__lt=now() - timedelta(days=1)).delete()


def payment_success_ua(request):
    return render(request, 'main/payment_success_ua.html')


def payment_success_en(request):
    return render(request, 'main/payment_success_en.html')


def payment_cancel(request):
    print("Отмена платежа")
    print(f"GET параметры: {request.GET}")
    language = request.GET.get('lang', 'uk')
    return redirect('payment_cancel_en' if language == 'en' else 'payment_cancel_ua')


def payment_cancel_ua(request):
    return render(request, 'main/payment_cancel_ua.html')


def payment_cancel_en(request):
    return render(request, 'main/payment_cancel_en.html')