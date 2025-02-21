import os
import base64
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from django.http import HttpResponse

# Kirish sahifasi
def index_view(request):
    return render(request, "cryptoapp/index.html")

# Shifrlash funksiyasi
def encrypt_view(request):
    if request.method == "POST":
        text = request.POST.get("text")  # Kiruvchi matn
        key = request.POST.get("key")  # AES kaliti

        # AES kalit uzunligi 16, 24 yoki 32 bo'lishi kerak
        if len(key) not in [16, 24, 32]:
            return render(request, "encrypt.html", {"error": "Kalit uzunligi noto'g'ri! (16, 24 yoki 32 bayt kiriting)"})

        key = key.encode()  # UTF-8 kodlash
        cipher = AES.new(key, AES.MODE_CBC)  # AES CBC rejimi
        iv = cipher.iv  # Tasodifiy IV generatsiya qilish
        ciphertext = cipher.encrypt(pad(text.encode(), AES.block_size))  # Shifrlash

        encrypted_data = base64.b64encode(iv + ciphertext).decode()  # IV + shifrlangan ma'lumot

        # Faylni yaratish va saqlash
        file_name = "encrypted_data.txt"
        file_path = default_storage.save(file_name, ContentFile(encrypted_data))

        return render(request, "cryptoapp/encrypt.html", {"file_url": default_storage.url(file_path)})

    return render(request, "cryptoapp/encrypt.html")

# Deshifrlash funksiyasi
def decrypt_view(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")  # Foydalanuvchi yuklagan fayl
        key = request.POST.get("key")  # AES kaliti

        # AES kalit uzunligi tekshiriladi
        if len(key) not in [16, 24, 32]:
            return render(request, "decrypt.html", {"error": "Kalit uzunligi noto'g'ri! (16, 24 yoki 32 bayt kiriting)"})

        key = key.encode()

        # Faylni o‘qish
        encrypted_data = uploaded_file.read()
        encrypted_data = base64.b64decode(encrypted_data)

        iv = encrypted_data[:16]  # IV ni olish
        ciphertext = encrypted_data[16:]  # Asosiy shifrlangan ma'lumot

        cipher = AES.new(key, AES.MODE_CBC, iv)  # AES CBC
        try:
            decrypted_text = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
        except:
            return render(request, "cryptoapp/decrypt.html", {"error": "Noto‘g‘ri kalit yoki fayl!"})

        # Deshifrlangan ma'lumotni yangi fayl sifatida saqlash
        decrypted_file_name = "decrypted_data.txt"
        file_path = default_storage.save(decrypted_file_name, ContentFile(decrypted_text))

        # Foydalanuvchi yuklab olishi uchun URL
        download_url = default_storage.url(file_path)

        return render(request, "cryptoapp/decrypt.html", {"decrypted_text": decrypted_text, "download_url": download_url})

    return render(request, "cryptoapp/decrypt.html")

# Faylni yuklab olish funksiyasi
def download_decrypted_file(request, file_name):
    """Deshifrlangan faylni foydalanuvchiga yuklab berish."""
    file_path = os.path.join(default_storage.location, file_name)

    if default_storage.exists(file_path):
        with default_storage.open(file_path, "rb") as f:
            response = HttpResponse(f.read(), content_type="text/plain")
            response["Content-Disposition"] = f'attachment; filename="{file_name}"'
            return response
    return HttpResponse("Fayl topilmadi!", status=404)
