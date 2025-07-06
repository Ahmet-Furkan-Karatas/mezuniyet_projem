#bot.py
import discord
from discord.ext import commands
from logic import CareerBotDB
from config import BOT_TOKEN, COMMAND_PREFIX, client
from discord.ui import View, Button, Select
from discord import Interaction
from datetime import datetime

class CareerOptionView(View):
    def __init__(self, career_title, ai_text):
        super().__init__(timeout=120)
        self.career_title = career_title
        self.ai_text = ai_text

        self.add_item(CareerSelect(title=career_title))
        self.add_item(InterestedButton(title=career_title, ai_text=ai_text))

class InterestedButton(Button):
    def __init__(self, title, ai_text):
        super().__init__(label="👍 İlgimi çekti", style=discord.ButtonStyle.success)
        self.title = title
        self.ai_text = ai_text

    async def callback(self, interaction: discord.Interaction):
        db.save_liked_career(interaction.user.id, self.title, self.ai_text)
        await interaction.response.send_message(
            f"`{self.title}` ilgini çekti olarak kaydedildi. 🎯",
            ephemeral=True
        )

class CareerSelect(Select):
    def __init__(self, title):
        options = [
            discord.SelectOption(label="Gereken beceriler", value="skills"),
            discord.SelectOption(label="Maaş aralığı", value="salary"),
            discord.SelectOption(label="Nasıl başlanır?", value="start"),
        ]
        super().__init__(placeholder="Bu meslekle ilgili ne öğrenmek istersin?", options=options)
        self.title = title

    async def callback(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        question_map = {
            "skills": "Gereken beceriler nelerdir?",
            "salary": "Maaş aralığı nedir?",
            "start": "Bu mesleğe nasıl başlanır?",
        }
        prompt = (
            f"Kariyer: {self.title}\n"
            f"Soru: {question_map[self.values[0]]}\n"
            "Kısa ve öz, tek cümle cevap ver."
        )
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            answer = response.text.strip()
        except Exception as e:
            print("Gemini API hatası:", e)
            answer = "Bilgi alınamadı."

        await interaction.followup.send(
            f"**{self.title}** hakkında:\n{answer}", ephemeral=True
        )

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)
db = CareerBotDB()

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı!')

@bot.command()
async def info(ctx):
    mesaj = (
        "**Kariyer Danışman Botu Komutları:**\n\n"
        "`!tanıtım` → Botun tanıtımını yapar\n" 
        "`!info` → Komut listesini gösterir\n"
        "`!kayıt [yaş] [ilgi]` → Kayıt olmanızı sağlar\n"
        "`!öneri` → İlgi alanlarınıza göre kariyer önerisi verir\n"
        "`!profil` → Kayıtlı bilgilerinizi gösterir (embed)\n"
        "`!güncelle [yaş] [ilgi]` → Yaş ve ilgi alanlarınızı günceller\n"
        "`!sıfırla` → Bilgilerinizi tamamen siler\n"
        "`!beğendiklerim` → Beğendiğiniz kariyer önerilerini listeler"
        "\n\n**Not:** Botu kullanabilmek için önce `!kayıt` komutunu kullanarak kendinizi tanıtmanız gerekiyor."
    )
    await ctx.send(mesaj)

@bot.command()
async def kayıt(ctx, yaş: int, *, ilgi: str):
    db.add_user(ctx.author.id, ctx.author.name, yaş, ilgi)
    await ctx.send(f"{ctx.author.name}, başarıyla kaydedildiniz!")

@bot.command()
async def profil(ctx):
    profil = db.get_user_profile(ctx.author.id)
    if profil:
        username, age, interests = profil
        embed = discord.Embed(title="👤 Kullanıcı Profilin", color=discord.Color.blue())
        embed.add_field(name="Kullanıcı", value=username, inline=False)
        embed.add_field(name="Yaş", value=str(age), inline=True)
        embed.add_field(name="İlgi Alanları", value=interests, inline=True)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Henüz kayıtlı değilsiniz. `!kayıt` komutunu kullanın.")

@bot.command()
async def güncelle(ctx, yaş: int, *, ilgi: str):
    profil = db.get_user_profile(ctx.author.id)
    if profil:
        db.update_user(ctx.author.id, yaş, ilgi)
        await ctx.send("Bilgileriniz başarıyla güncellendi.")
    else:
        await ctx.send("Kayıt bulunamadı. Önce `!kayıt` komutunu kullanın.")

import re

@bot.command()
async def öneri(ctx):
    profil = db.get_user_profile(ctx.author.id)
    if not profil:
        await ctx.send("Lütfen önce `!kayıt yaş ilgi` komutuyla kayıt olun.")
        return

    username, _, interests = profil
    ai_response = db.generate_detailed_ai_suggestions(interests, username)
    if not ai_response:
        await ctx.send("AI önerisi alınamadı.")
        return

    # Öneri içindeki başlığı ve açıklamayı daha sağlam ayır
    # Örneğin, metin şu formatta varsayalım:
    # **Başlık**\nAçıklama (birden fazla satır olabilir)

    pattern = r"\*\*(.+?)\*\*\s*([\s\S]+)"  # Başlık: **...**, Açıklama: sonrası her şey
    match = re.search(pattern, ai_response)

    if match:
        title = match.group(1).strip()
        desc = match.group(2).strip()

        if len(title) > 256:
            title = title[:253] + "..."

        embed = discord.Embed(title=title, description=desc, color=discord.Color.purple())
        view = CareerOptionView(title, desc)
        await ctx.send(embed=embed, view=view)
    else:
        # Eğer pattern yakalayamazsa, tüm metni açıklama yap
        embed = discord.Embed(title="Kariyer Önerisi", description=ai_response, color=discord.Color.purple())
        view = CareerOptionView("Kariyer Önerisi", ai_response)
        await ctx.send(embed=embed, view=view)

@bot.command()
async def sıfırla(ctx):
    db.delete_user(ctx.author.id)
    await ctx.send("Kayıt bilgileriniz silindi.")

@bot.command()
async def beğendiklerim(ctx):
    entries = db.get_liked_careers(ctx.author.id)
    if not entries:
        await ctx.send("Henüz beğendiğiniz bir öneri yok.")
        return

    for title, liked_at, ai_text in entries:
        embed = discord.Embed(title=f"❤️ {title}", description=ai_text, color=discord.Color.red())
        embed.set_footer(text=f"Beğenme Tarihi: {liked_at}")
        await ctx.send(embed=embed)

@bot.command()
async def tanıtım(ctx):
    embed = discord.Embed(
        title="🤖 Kariyer Danışman Botu - Tanıtım",
        description=(
            "Merhaba! Ben Kariyer Danışman Botu, gençlerin ve kariyerine yön vermek isteyenlerin "
            "hayallerine ulaşmaları için yapay zeka destekli rehberlik sunuyorum.\n\n"
            "🎯 İlgi alanlarınıza göre size özel kariyer önerileri sağlıyor, "
            "seçtiğiniz mesleklerle ilgili gerekli beceriler, maaş aralıkları ve başlangıç yolları hakkında bilgi veriyorum.\n\n"
            "💡 Ayrıca beğendiğiniz kariyerleri kaydedip daha sonra kolayca inceleyebilirsiniz.\n\n"
            "🚀 Hadi başlayalım! `!kayıt [yaş] [ilgi alanları]` komutuyla kendinizi tanıtın ve kariyer yolculuğunuzu benimle keşfedin."
        ),
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

bot.run(BOT_TOKEN)
