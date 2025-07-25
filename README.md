# 🚀 Kariyer Danışman Discord Botu

Gençlerin ve iş hayatında yönünü bulmak isteyenlerin kariyer yolculuğu için öneriler veren yapay zeka destekli Discord botu! 🤖✨

---

## 🌟 Özellikler

* 👥 Kişisel yaş ve ilgi alanlarına göre özel kariyer önerileri sunar.
* 🤖 Yapay zeka destekli kısa ve öz kariyer bilgileri sağlar (gerekli beceriler, maaş aralığı, nasıl başlanır gibi).
* 💾 Beğenilen kariyer önerilerini kayıt eder ve kullanıcıya liste halinde sunar.
* 📝 Kullanıcı profili oluşturma, güncelleme ve sıfırlama komutları.
* 🎛️ Kolay kullanım için sezgisel komut yapısı ve etkileşimli butonlar/menüler.
* 🎨 Discord UI elemanlarıyla şık ve kullanıcı dostu deneyim.

---

## ⚙️ Kurulum

1. Projeyi klonlayın:

   ```bash
   git clone <repo_url>
   cd <repo_klasoru>
   ```

2. [Gemini API anahtarı alın](https://aistudio.google.com/app/apikey) 🗝️ — Gemini API tokeninizi buradan edinin.

3. Eğer halihazırda bir discord botunuz yoksa [bu](https://discord.com/developers/applications) linke tıklayarak bir discord botu oluşturun ardından kullanmak istediğiniz sunucuya ekleyin.

4. Gerekli paketleri yükleyin:

   ```bash
   pip install -r requirements.txt
   ```

5. `config.py` dosyasını oluşturup Discord bot tokeninizi, komut prefixinizi ve yapay zeka istemcisi tokenininizi ekleyin:

   ```python
   from google import genai

   BOT_TOKEN = "your-discord-bot-token"
   COMMAND_PREFIX = "!"
   client = genai.Client(api_key="your-api-token")
   DATABASE = "database.db"
   ```

6. Önce logic.py dosyasını çalıştırıp veritabanı dosyanızı oluşturun ardından da bot.py dosyasını çalıştırarak da botu kullanmaya başlayın.

---

## 🚀 Kullanım

| Komut                    | Açıklama                                                       |
| ------------------------ | -------------------------------------------------------------- |
| `!kayıt [yaş] [ilgi]`    | Kullanıcı profilini oluşturur.                                 |
| `!öneri`                 | İlgi alanlarına göre yapay zeka destekli kariyer önerisi alır. |
| `!profil`                | Kayıtlı kullanıcı bilgilerini embed olarak gösterir.           |
| `!güncelle [yaş] [ilgi]` | Profil bilgilerini günceller.                                  |
| `!sıfırla`               | Profil ve kayıt bilgilerini siler.                             |
| `!beğendiklerim`         | Daha önce beğenilen kariyer önerilerini listeler.              |
| `!tanıtım`               | Botun kendini tanıttığı şık mesajı gösterir.                   |

---

## 🛠️ Teknik Detaylar

* **Dil:** Python 3.11+ 🐍
* **Discord Kütüphanesi:** discord.py 🎮
* **Veritabanı:** SQLite3 (hafif ve dosya tabanlı) 💾
* **Yapay Zeka API:** Google Gemini (gelişmiş dil modeli ile içerik üretimi) 🤖

---

## 🤝 Katkıda Bulunma

Proje açık kaynak ve gelişime açık.
İstersen sorun bildir, yeni özellik öner veya direkt katkı yap!
Pull request ve issue’larınızı bekliyoruz. 💡✨

---

## 📫 İletişim

* Geliştirici: Ahmet Furkan
* GitHub: [github.com/Ahmet-Furkan-Karatas](https://github.com/Ahmet-Furkan-Karatas)
* E-posta: [ahmet\_karatas44@hotmail.com](mailto:ahmet_karatas44@hotmail.com)

---

*Teşekkürler! Başarılar dilerim.* 🚀💙
