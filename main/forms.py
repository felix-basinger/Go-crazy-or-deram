from django import forms


class UkraineDeliveryForm(forms.Form):
    first_name = forms.CharField(label="Ім'я", max_length=100)
    last_name = forms.CharField(label="Прізвище", max_length=100)
    phone = forms.CharField(label="Номер телефону", max_length=15)
    address = forms.CharField(label="Адреса доставки", widget=forms.Textarea)
    email = forms.EmailField(label="Email")


class WorldDeliveryForm(forms.Form):
    first_name = forms.CharField(label="Ім'я латиницею", max_length=100)
    last_name = forms.CharField(label="Прізвище латиницею", max_length=100)
    country = forms.CharField(label="Країна", max_length=100)
    city = forms.CharField(label="Місто", max_length=100)
    postal_code = forms.CharField(label="Поштовий індекс", max_length=10)
    address = forms.CharField(label="Адреса (вулиця, будинок, квартира)", widget=forms.Textarea)
    phone = forms.CharField(label="Номер телефону", max_length=15)
    email = forms.EmailField(label="Email")
    additional_info = forms.CharField(label="Додаткова інформація", required=False, widget=forms.Textarea)
