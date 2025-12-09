# Udemy Demo Backend

Demo amaçlı FastAPI backend projesi. Kullanıcı, eğitmen ve admin rolleri ile mini Udemy ve Uber benzeri sistemleri simüle eder.

## Proje Hakkında

Bu proje, kullanıcı, eğitmen ve admin rolleri ile mini Udemy akışı ve canlı ders eşleştirme (mini Uber mantığı) simülasyonu sunar. Başlıca özellikler:

- Eğitim listesi ve satın alma simülasyonu
- Ödeme akışı threading ile simüle edilmiştir
- Canlı ders talebi ve eğitmen-öğrenci eşleştirme
- Mock veri tabanı (JSON) kullanımı ile hızlı test

## Kurulum

1. Repo klonlanır:
   git clone https://github.com/edamerveatalay/udemy-demo-backend.git

2. Sanal ortam oluşturulur ve aktif edilir:
   python -m venv .venv
   source .venv/bin/activate # macOS / Linux
   ..venv\Scripts\activate # Windows

3. Gereksinimler yüklenir:
   pip install -r requirements.txt

4. Sunucu çalıştırılır:
   uvicorn app.main:app --reload

## Kullanım

- `/auth/login` ile giriş yapılabilir
- `/courses/` ile kurs listesi görüntülenebilir
- `/purchase/` ile kurs satın alma işlemi yapılabilir
- `/payment/` ile ödeme simülasyonu yapılır
- `/live/request` ile canlı ders talebi oluşturulur
- `/admin/` endpointleri ile admin paneline erişim sağlanır

## Kullanılan Teknolojiler

- **FastAPI**: Hızlı ve modern backend framework
- **Pydantic**: Veri doğrulama ve modelleme
- **Uvicorn**: ASGI server
- **Threading**: Arka planda ödeme otomasyonu için

## Ödeme ve Eşleştirme Akışı

- **Ödeme Akışı:** `/payment/create` endpoint’i ile ödeme pending olarak kaydedilir; threading ile success durumuna güncellenir. Kurs kullanıcıya atanır. Geliştirme ve test için `/payment/confirm` endpoint’i ile manuel onay da mümkündür.
- **Eşleştirme Mantığı:** `/live/request` endpoint’i ile canlı ders talebi oluşturulur. Sistem, mock veri tabanından ilk uygun eğitmeni seçer ve eğitmene bildirim simülasyonu gönderir. Kullanıcı tarafında talep “assigned” statüsü ile kaydedilir.

## Proje Yapısı

- `app/` - FastAPI uygulama kodları
  - `models/` - Veri modelleri
  - `routers/` - Endpoint yönlendirmeleri
  - `controllers/` - İş mantığı ve simülasyon
  - `schemas/` - Pydantic veri şemaları
  - `utils/` - Yardımcı fonksiyonlar ve araçlar
  - `mock_db.json` - Mock veri tabanı
- `requirements.txt` - Python bağımlılıkları
- `README.md` - Proje dokümanı

## API

| Endpoint                          | Metod | Açıklama                                                                                 |
| --------------------------------- | ----- | ---------------------------------------------------------------------------------------- |
| `/auth/login`                     | POST  | Kullanıcı, eğitmen veya admin giriş yapar ve JWT token döner                             |
| `/courses/`                       | GET   | Mevcut kurs listesini görüntüler                                                         |
| `/courses/{course_id}`            | GET   | Belirli bir kursun detaylarını getirir                                                   |
| `/purchase/`                      | POST  | Seçilen kurs için satın alma isteği oluşturur; ödeme `/payment/create` ile simüle edilir |
| `/payment/create`                 | POST  | Ödeme simülasyonu başlatır (pending → success)                                           |
| `/payment/confirm`                | POST  | Ödemeyi manuel olarak onaylar (test/geliştirme amaçlı)                                   |
| `/live/request`                   | POST  | Canlı ders talebi oluşturur, uygun eğitmeni atar ve bildirim simülasyonu yapar           |
| `/users/me`                       | GET   | Mevcut kullanıcının profil bilgilerini getirir                                           |
| `/users/me/courses`               | GET   | Kullanıcının satın aldığı kursları getirir                                               |
| `/instructor/notifications`       | GET   | Eğitmenin bildirim listesini getirir                                                     |
| `/instructor/notifications/clear` | POST  | Eğitmenin bildirimlerini temizler                                                        |
| `/admin/users`                    | GET   | Tüm kullanıcıları listeler (admin yetkisi)                                               |
| `/admin/courses`                  | GET   | Tüm kursları listeler (admin yetkisi)                                                    |
| `/admin/purchases`                | GET   | Tüm satın almaları listeler (admin yetkisi)                                              |
| `/admin/payments`                 | GET   | Tüm ödemeleri listeler (admin yetkisi)                                                   |
| `/admin/live-requests`            | GET   | Tüm canlı ders taleplerini listeler (admin yetkisi)                                      |
