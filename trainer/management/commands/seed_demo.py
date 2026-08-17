from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from trainer.models import Scenario, ConversationStep, AnswerChoice


class Command(BaseCommand):
    help = "Demo admin va namunaviy yaponcha dialoglarni yaratadi."

    def handle(self, *args, **kwargs):
        admin, created = User.objects.get_or_create(username="admin", defaults={"is_staff": True, "is_superuser": True})
        if created: admin.set_password("admin12345"); admin.save()
        demos = [
            ("☕","Kafeda buyurtma berish","Restoranda odobli buyurtma qilishni mashq qiling.","restaurant","beginner",5,
             [("いらっしゃいませ！何になさいますか？","Irasshaimase! Nani ni nasaimasu ka?","Xush kelibsiz! Nima buyurasiz?",[("コーヒーをお願いします。",True),("さようなら。",False),("駅はどこですか？",False)]),
              ("サイズはいかがなさいますか？","Saizu wa ikaga nasaimasu ka?","O'lchami qanday bo'ladi?",[("大きいサイズでお願いします。",True),("ありがとうございます。",False),("すみません。",False)])]),
            ("🚉","Poyezd bekatida","Bekat va yo'nalish haqida savol berishni o'rganing.","travel","beginner",5,
             [("東京駅はどこですか？","Tokyo eki wa doko desu ka?","Tokyo vokzali qayerda?",[("あそこです。",True),("いただきます。",False),("おやすみなさい。",False)]),
              ("切符を一枚お願いします。","Kippu o ichimai onegaishimasu.","Bitta chipta, iltimos.",[("はい、どうぞ。",True),("おいしいです。",False),("また明日。",False)])]),
            ("🎓","Universitetda tanishuv","Yangi yapon kursdoshingiz bilan tabiiy tanishing.","school","beginner",6,
             [("はじめまして。お名前は何ですか？","Hajimemashite. Onamae wa nan desu ka?","Tanishganimdan xursandman. Ismingiz nima?",[("ゾヒドです。よろしくお願いします。",True),("いただきます。",False),("どこですか？",False)]),
              ("日本語を勉強していますか？","Nihongo o benkyou shiteimasu ka?","Yapon tilini o'rganyapsizmi?",[("はい、勉強しています。",True),("いい天気ですね。",False),("コーヒーください。",False)])]),
        ]
        for emoji,title,desc,cat,level,mins,steps in demos:
            s, _ = Scenario.objects.get_or_create(title=title, defaults=dict(
                description=desc, category=cat, level=level, emoji=emoji, estimated_minutes=mins, created_by=admin, is_active=True))
            for i,(jp,rom,tr,choices) in enumerate(steps,1):
                st,_=ConversationStep.objects.get_or_create(scenario=s,order=i,defaults=dict(
                    speaker="AI Sensei", japanese_text=jp, romaji=rom, translation=tr, answer_type="choice"))
                if st.choices.count()==0:
                    for text,correct in choices: AnswerChoice.objects.create(step=st,text=text,is_correct=correct)
        self.stdout.write(self.style.SUCCESS("Demo ma'lumotlar tayyor."))
