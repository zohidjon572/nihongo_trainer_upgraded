from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from trainer.models import Scenario, ConversationStep, AnswerChoice


class Command(BaseCommand):
    help = "Nihongo Talk Trainer uchun demo mashqlarni yaratadi."

    def handle(self, *args, **kwargs):

        # ==============================
        # ADMIN USER
        # ==============================
        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "is_staff": True,
                "is_superuser": True,
            },
        )

        if created:
            admin.set_password("admin12345")
            admin.save()

        # ==============================
        # DEMO SCENARIYLAR
        # ==============================
        demos = [

            # 1
            {
                "emoji": "☕",
                "title": "Kafeda buyurtma berish",
                "description": "Kafeda yaponcha ichimlik va taom buyurtma qilishni mashq qiling.",
                "category": "restaurant",
                "level": "beginner",
                "minutes": 5,
                "steps": [
                    {
                        "jp": "いらっしゃいませ！何になさいますか？",
                        "romaji": "Irasshaimase! Nani ni nasaimasu ka?",
                        "translation": "Xush kelibsiz! Nima buyurasiz?",
                        "choices": [
                            ("コーヒーをお願いします。", True),
                            ("駅はどこですか？", False),
                            ("おやすみなさい。", False),
                        ],
                    },
                    {
                        "jp": "お飲み物は何にしますか？",
                        "romaji": "Onomimono wa nani ni shimasu ka?",
                        "translation": "Ichimlik sifatida nima olasiz?",
                        "choices": [
                            ("コーヒーをお願いします。", True),
                            ("先生です。", False),
                            ("明日です。", False),
                        ],
                    },
                    {
                        "jp": "サイズはいかがなさいますか？",
                        "romaji": "Saizu wa ikaga nasaimasu ka?",
                        "translation": "O‘lchami qanday bo‘ladi?",
                        "choices": [
                            ("大きいサイズでお願いします。", True),
                            ("駅に行きます。", False),
                            ("学生です。", False),
                        ],
                    },
                    {
                        "jp": "店内でお召し上がりですか？",
                        "romaji": "Tennai de omeshiagari desu ka?",
                        "translation": "Shu yerda yeysizmi?",
                        "choices": [
                            ("はい、お願いします。", True),
                            ("いい天気です。", False),
                            ("東京です。", False),
                        ],
                    },
                ],
            },

            # 2
            {
                "emoji": "🚉",
                "title": "Poyezd bekatida",
                "description": "Yaponiyada bekat, chipta va yo‘nalish haqida gaplashishni o‘rganing.",
                "category": "travel",
                "level": "beginner",
                "minutes": 6,
                "steps": [
                    {
                        "jp": "東京駅はどこですか？",
                        "romaji": "Tokyo eki wa doko desu ka?",
                        "translation": "Tokyo vokzali qayerda?",
                        "choices": [
                            ("あそこです。", True),
                            ("おいしいです。", False),
                            ("学生です。", False),
                        ],
                    },
                    {
                        "jp": "切符を一枚お願いします。",
                        "romaji": "Kippu o ichimai onegaishimasu.",
                        "translation": "Bitta chipta, iltimos.",
                        "choices": [
                            ("はい、どうぞ。", True),
                            ("いただきます。", False),
                            ("また明日。", False),
                        ],
                    },
                    {
                        "jp": "新宿までいくらですか？",
                        "romaji": "Shinjuku made ikura desu ka?",
                        "translation": "Shinjukugacha qancha turadi?",
                        "choices": [
                            ("500円です。", True),
                            ("学生です。", False),
                            ("おはようございます。", False),
                        ],
                    },
                    {
                        "jp": "この電車は新宿に行きますか？",
                        "romaji": "Kono densha wa Shinjuku ni ikimasu ka?",
                        "translation": "Bu poyezd Shinjukuga boradimi?",
                        "choices": [
                            ("はい、行きます。", True),
                            ("コーヒーです。", False),
                            ("先生です。", False),
                        ],
                    },
                ],
            },

            # 3
            {
                "emoji": "🎓",
                "title": "Universitetda tanishuv",
                "description": "Yangi yapon kursdoshingiz bilan tanishish va o‘zingiz haqingizda gapirishni mashq qiling.",
                "category": "school",
                "level": "beginner",
                "minutes": 6,
                "steps": [
                    {
                        "jp": "はじめまして。お名前は何ですか？",
                        "romaji": "Hajimemashite. Onamae wa nan desu ka?",
                        "translation": "Tanishganimdan xursandman. Ismingiz nima?",
                        "choices": [
                            ("ゾヒドです。よろしくお願いします。", True),
                            ("いただきます。", False),
                            ("駅はどこですか？", False),
                        ],
                    },
                    {
                        "jp": "どこから来ましたか？",
                        "romaji": "Doko kara kimashita ka?",
                        "translation": "Qayerdan kelgansiz?",
                        "choices": [
                            ("ウズベキスタンから来ました。", True),
                            ("コーヒーをください。", False),
                            ("明日です。", False),
                        ],
                    },
                    {
                        "jp": "日本語を勉強していますか？",
                        "romaji": "Nihongo o benkyou shiteimasu ka?",
                        "translation": "Yapon tilini o‘rganyapsizmi?",
                        "choices": [
                            ("はい、勉強しています。", True),
                            ("いいえ、食べます。", False),
                            ("東京です。", False),
                        ],
                    },
                    {
                        "jp": "趣味は何ですか？",
                        "romaji": "Shumi wa nan desu ka?",
                        "translation": "Hobbiyingiz nima?",
                        "choices": [
                            ("音楽を聞くことです。", True),
                            ("駅に行きます。", False),
                            ("500円です。", False),
                        ],
                    },
                ],
            },

            # 4
            {
                "emoji": "🛍️",
                "title": "Do‘konda xarid qilish",
                "description": "Do‘konda narx so‘rash va mahsulot tanlashni mashq qiling.",
                "category": "shopping",
                "level": "beginner",
                "minutes": 6,
                "steps": [
                    {
                        "jp": "これはいくらですか？",
                        "romaji": "Kore wa ikura desu ka?",
                        "translation": "Bu qancha turadi?",
                        "choices": [
                            ("3,000円です。", True),
                            ("学生です。", False),
                            ("駅です。", False),
                        ],
                    },
                    {
                        "jp": "このシャツを見せてください。",
                        "romaji": "Kono shatsu o misete kudasai.",
                        "translation": "Bu ko‘ylakni ko‘rsating, iltimos.",
                        "choices": [
                            ("はい、どうぞ。", True),
                            ("おやすみなさい。", False),
                            ("明日です。", False),
                        ],
                    },
                    {
                        "jp": "試着してもいいですか？",
                        "romaji": "Shichaku shite mo ii desu ka?",
                        "translation": "Kiyib ko‘rsam bo‘ladimi?",
                        "choices": [
                            ("はい、どうぞ。", True),
                            ("東京に行きます。", False),
                            ("コーヒーです。", False),
                        ],
                    },
                    {
                        "jp": "これをください。",
                        "romaji": "Kore o kudasai.",
                        "translation": "Shuni olaman.",
                        "choices": [
                            ("ありがとうございます。", True),
                            ("どこですか？", False),
                            ("学生です。", False),
                        ],
                    },
                ],
            },

            # 5
            {
                "emoji": "🏨",
                "title": "Mehmonxonada",
                "description": "Mehmonxonada ro‘yxatdan o‘tish va xona haqida savol berishni mashq qiling.",
                "category": "travel",
                "level": "beginner",
                "minutes": 7,
                "steps": [
                    {
                        "jp": "チェックインをお願いします。",
                        "romaji": "Chekkuin o onegaishimasu.",
                        "translation": "Ro‘yxatdan o‘tmoqchiman.",
                        "choices": [
                            ("はい、お名前をお願いします。", True),
                            ("コーヒーください。", False),
                            ("駅はどこですか？", False),
                        ],
                    },
                    {
                        "jp": "予約していますか？",
                        "romaji": "Yoyaku shiteimasu ka?",
                        "translation": "Bron qilganmisiz?",
                        "choices": [
                            ("はい、予約しています。", True),
                            ("学生です。", False),
                            ("おいしいです。", False),
                        ],
                    },
                    {
                        "jp": "朝食は何時からですか？",
                        "romaji": "Choushoku wa nanji kara desu ka?",
                        "translation": "Nonushta soat nechadan?",
                        "choices": [
                            ("7時からです。", True),
                            ("東京からです。", False),
                            ("500円です。", False),
                        ],
                    },
                ],
            },

            # 6
            {
                "emoji": "💼",
                "title": "Ishxonada suhbat",
                "description": "Ish joyida salomlashish, uchrashuv va kundalik muloqotni mashq qiling.",
                "category": "work",
                "level": "intermediate",
                "minutes": 8,
                "steps": [
                    {
                        "jp": "おはようございます。",
                        "romaji": "Ohayou gozaimasu.",
                        "translation": "Xayrli tong.",
                        "choices": [
                            ("おはようございます。", True),
                            ("おやすみなさい。", False),
                            ("いただきます。", False),
                        ],
                    },
                    {
                        "jp": "今日の会議は何時ですか？",
                        "romaji": "Kyou no kaigi wa nanji desu ka?",
                        "translation": "Bugungi yig‘ilish soat nechada?",
                        "choices": [
                            ("10時です。", True),
                            ("学生です。", False),
                            ("東京です。", False),
                        ],
                    },
                    {
                        "jp": "この資料を確認してください。",
                        "romaji": "Kono shiryou o kakunin shite kudasai.",
                        "translation": "Iltimos, bu hujjatni tekshiring.",
                        "choices": [
                            ("はい、確認します。", True),
                            ("コーヒーを飲みます。", False),
                            ("駅に行きます。", False),
                        ],
                    },
                    {
                        "jp": "お疲れ様でした。",
                        "romaji": "Otsukaresama deshita.",
                        "translation": "Mehnatingiz uchun rahmat / Bugun yaxshi ishladingiz.",
                        "choices": [
                            ("お疲れ様でした。", True),
                            ("いただきます。", False),
                            ("いくらですか？", False),
                        ],
                    },
                ],
            },

            # 7
            {
                "emoji": "🏥",
                "title": "Kasalxonada",
                "description": "Kasalxonada oddiy savollar va javoblarni yapon tilida mashq qiling.",
                "category": "other",
                "level": "intermediate",
                "minutes": 8,
                "steps": [
                    {
                        "jp": "どうしましたか？",
                        "romaji": "Dou shimashita ka?",
                        "translation": "Nima bo‘ldi?",
                        "choices": [
                            ("頭が痛いです。", True),
                            ("学生です。", False),
                            ("駅に行きます。", False),
                        ],
                    },
                    {
                        "jp": "いつから痛いですか？",
                        "romaji": "Itsu kara itai desu ka?",
                        "translation": "Qachondan beri og‘riyapti?",
                        "choices": [
                            ("昨日からです。", True),
                            ("東京です。", False),
                            ("500円です。", False),
                        ],
                    },
                    {
                        "jp": "この薬を一日三回飲んでください。",
                        "romaji": "Kono kusuri o ichinichi sankai nonde kudasai.",
                        "translation": "Bu dorini kuniga uch marta iching.",
                        "choices": [
                            ("はい、わかりました。", True),
                            ("おいしいです。", False),
                            ("どこですか？", False),
                        ],
                    },
                ],
            },

            # 8
            {
                "emoji": "🏠",
                "title": "Kundalik hayot",
                "description": "Uyda va kundalik hayotda ishlatiladigan oddiy yaponcha gaplarni mashq qiling.",
                "category": "daily",
                "level": "beginner",
                "minutes": 5,
                "steps": [
                    {
                        "jp": "今日は何をしますか？",
                        "romaji": "Kyou wa nani o shimasu ka?",
                        "translation": "Bugun nima qilasiz?",
                        "choices": [
                            ("映画を見ます。", True),
                            ("学生です。", False),
                            ("500円です。", False),
                        ],
                    },
                    {
                        "jp": "何時に起きますか？",
                        "romaji": "Nanji ni okimasu ka?",
                        "translation": "Soat nechada turasiz?",
                        "choices": [
                            ("7時に起きます。", True),
                            ("東京です。", False),
                            ("コーヒーです。", False),
                        ],
                    },
                    {
                        "jp": "週末は何をしましたか？",
                        "romaji": "Shuumatsu wa nani o shimashita ka?",
                        "translation": "Dam olish kunlari nima qildingiz?",
                        "choices": [
                            ("友達と映画を見ました。", True),
                            ("学生です。", False),
                            ("駅はどこですか？", False),
                        ],
                    },
                ],
            },

            # 9
            {
                "emoji": "🗺️",
                "title": "Yo‘l so‘rash",
                "description": "Yaponiyada yo‘l so‘rash va manzilni tushuntirishni mashq qiling.",
                "category": "travel",
                "level": "beginner",
                "minutes": 6,
                "steps": [
                    {
                        "jp": "すみません。駅はどこですか？",
                        "romaji": "Sumimasen. Eki wa doko desu ka?",
                        "translation": "Kechirasiz. Bekat qayerda?",
                        "choices": [
                            ("まっすぐ行ってください。", True),
                            ("コーヒーください。", False),
                            ("学生です。", False),
                        ],
                    },
                    {
                        "jp": "右に曲がってください。",
                        "romaji": "Migi ni magatte kudasai.",
                        "translation": "O‘ngga buriling.",
                        "choices": [
                            ("はい、ありがとうございます。", True),
                            ("500円です。", False),
                            ("おやすみなさい。", False),
                        ],
                    },
                    {
                        "jp": "駅までどのくらいかかりますか？",
                        "romaji": "Eki made dono kurai kakarimasu ka?",
                        "translation": "Bekatgacha qancha vaqt ketadi?",
                        "choices": [
                            ("10分ぐらいです。", True),
                            ("学生です。", False),
                            ("コーヒーです。", False),
                        ],
                    },
                ],
            },

            # 10
            {
                "emoji": "🍣",
                "title": "Restoranda",
                "description": "Restoranda stol, menyu va taom buyurtma qilishni mashq qiling.",
                "category": "restaurant",
                "level": "beginner",
                "minutes": 7,
                "steps": [
                    {
                        "jp": "二人です。",
                        "romaji": "Futari desu.",
                        "translation": "Ikki kishimiz.",
                        "choices": [
                            ("こちらへどうぞ。", True),
                            ("駅です。", False),
                            ("学生です。", False),
                        ],
                    },
                    {
                        "jp": "メニューをお願いします。",
                        "romaji": "Menyuu o onegaishimasu.",
                        "translation": "Menyuni bering, iltimos.",
                        "choices": [
                            ("はい、どうぞ。", True),
                            ("おやすみなさい。", False),
                            ("東京です。", False),
                        ],
                    },
                    {
                        "jp": "おすすめは何ですか？",
                        "romaji": "Osusume wa nan desu ka?",
                        "translation": "Tavsiya qiladigan taomingiz qaysi?",
                        "choices": [
                            ("こちらがおすすめです。", True),
                            ("500円です。", False),
                            ("学生です。", False),
                        ],
                    },
                    {
                        "jp": "お会計をお願いします。",
                        "romaji": "Okaikei o onegaishimasu.",
                        "translation": "Hisobni bering, iltimos.",
                        "choices": [
                            ("はい、ありがとうございます。", True),
                            ("駅はどこですか？", False),
                            ("明日です。", False),
                        ],
                    },
                ],
            },
        ]

        # ==============================
        # DATABASE GA YOZISH
        # ==============================

        for demo in demos:

            scenario, _ = Scenario.objects.update_or_create(
                title=demo["title"],
                defaults={
                    "description": demo["description"],
                    "category": demo["category"],
                    "level": demo["level"],
                    "emoji": demo["emoji"],
                    "estimated_minutes": demo["minutes"],
                    "created_by": admin,
                    "is_active": True,
                },
            )

            for order, step_data in enumerate(demo["steps"], start=1):

                step, _ = ConversationStep.objects.update_or_create(
                    scenario=scenario,
                    order=order,
                    defaults={
                        "speaker": "AI Sensei",
                        "japanese_text": step_data["jp"],
                        "romaji": step_data["romaji"],
                        "translation": step_data["translation"],
                        "answer_type": "choice",
                    },
                )

                # Eski variantlarni tozalaymiz
                step.choices.all().delete()

                # Yangi variantlarni qo‘shamiz
                for text, is_correct in step_data["choices"]:
                    AnswerChoice.objects.create(
                        step=step,
                        text=text,
                        is_correct=is_correct,
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ {len(demos)} ta yaponcha mashq muvaffaqiyatli yaratildi!"
            )
        )