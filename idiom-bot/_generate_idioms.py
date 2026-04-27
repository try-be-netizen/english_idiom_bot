"""
Одноразовый скрипт для генерации idioms.json.
Запускается локально, результат коммитится в репозиторий.
"""
import json
from urllib.parse import quote

# Топ-200 популярных английских идиом.
# Формат: (idiom_en, translation_ru, meaning_en, example_en)
IDIOMS = [
    ("A piece of cake", "проще простого, плёвое дело", "something very easy to do", "The exam was a piece of cake — I finished in twenty minutes."),
    ("Break a leg", "ни пуха ни пера", "good luck (especially before a performance)", "Break a leg tonight — you've rehearsed this play for months!"),
    ("Hit the books", "засесть за учёбу", "to study hard", "I can't go out tonight — I have to hit the books before the final."),
    ("Let the cat out of the bag", "проболтаться, выдать секрет", "to reveal a secret, often by accident", "She let the cat out of the bag about the surprise party."),
    ("Under the weather", "приболеть, неважно себя чувствовать", "feeling slightly ill", "I'm a bit under the weather today — I think I'll stay home."),
    ("Bite the bullet", "стиснуть зубы и сделать", "to do something unpleasant that you have been avoiding", "I hate going to the dentist, but I'll have to bite the bullet."),
    ("Break the ice", "растопить лёд, начать общение", "to do or say something to make people feel relaxed", "He told a joke to break the ice at the meeting."),
    ("Hit the nail on the head", "попасть в точку", "to describe exactly what is causing a situation or problem", "You hit the nail on the head when you said the project lacked focus."),
    ("Once in a blue moon", "крайне редко, раз в сто лет", "very rarely", "We only see each other once in a blue moon these days."),
    ("Spill the beans", "выболтать секрет", "to reveal secret information", "Come on, spill the beans — what did he tell you?"),
    ("The ball is in your court", "теперь твой ход", "it is your responsibility to take the next action", "I've made my offer, so the ball is in your court now."),
    ("Cost an arm and a leg", "стоить целое состояние", "to be very expensive", "That new car cost him an arm and a leg."),
    ("Cut corners", "халтурить, экономить на качестве", "to do something in the easiest or cheapest way, often badly", "The builders cut corners and now the roof leaks."),
    ("Get out of hand", "выйти из-под контроля", "to become difficult to control", "The party got out of hand around midnight."),
    ("Hit the sack", "отправиться спать", "to go to bed", "I'm exhausted — I'm going to hit the sack."),
    ("It's not rocket science", "это не бином Ньютона", "it is not difficult to understand", "Come on, making coffee isn't rocket science."),
    ("Pull someone's leg", "подшучивать, разыгрывать", "to tell someone something untrue as a joke", "Don't worry, I was just pulling your leg — there's no test today."),
    ("So far so good", "пока всё идёт хорошо", "things are going well up to now", "The renovation? So far so good — we're on schedule."),
    ("Speak of the devil", "лёгок на помине", "said when the person you were talking about appears", "Speak of the devil — here comes Mark now!"),
    ("That's the last straw", "это последняя капля", "the final problem in a series that makes you lose patience", "He was late again — that's the last straw, he's fired."),
    ("Beat around the bush", "ходить вокруг да около", "to avoid talking about what is important", "Stop beating around the bush and tell me what happened."),
    ("Better late than never", "лучше поздно, чем никогда", "it is better for someone to arrive or do something late than not at all", "He apologised after a year, but better late than never."),
    ("Bite off more than you can chew", "взять на себя слишком много", "to try to do something that is too difficult for you", "I bit off more than I could chew when I agreed to redesign the whole site alone."),
    ("By the skin of your teeth", "еле-еле, чудом", "only just; barely", "We caught the train by the skin of our teeth."),
    ("Call it a day", "закончить на сегодня", "to stop working on something", "We've been at this for hours — let's call it a day."),
    ("Cry over spilled milk", "плакать о том, чего не вернёшь", "to be upset about something that has already happened", "Yes, you made a mistake, but there's no point crying over spilled milk."),
    ("Curiosity killed the cat", "любопытной Варваре нос оторвали", "being too inquisitive can lead to trouble", "Don't ask too many questions — curiosity killed the cat."),
    ("Don't judge a book by its cover", "не суди книгу по обложке", "don't form an opinion based only on appearance", "He looks rough, but he's the kindest man I know — don't judge a book by its cover."),
    ("Every cloud has a silver lining", "нет худа без добра", "there is something positive in every difficult situation", "Losing that job was hard, but every cloud has a silver lining — I found a better one."),
    ("Get a taste of your own medicine", "получить по заслугам", "to be treated the same unpleasant way you treat others", "He's always rude to waiters; today one was rude back — a taste of his own medicine."),
    ("Give someone the cold shoulder", "холодно отнестись, игнорировать", "to deliberately ignore someone", "Ever since our argument, she's been giving me the cold shoulder."),
    ("Go the extra mile", "сделать больше, чем требуется", "to make more effort than is expected of you", "Our team always goes the extra mile for our customers."),
    ("Hang in there", "держись, не сдавайся", "don't give up", "I know exams are tough — hang in there, you're almost done."),
    ("Hit the road", "отправляться в путь", "to leave or begin a journey", "It's getting late — we should hit the road."),
    ("In hot water", "в беде, в неприятностях", "in trouble", "He's in hot water with his boss for missing the deadline."),
    ("It takes two to tango", "в ссоре всегда виноваты двое", "both people involved in a situation are responsible for it", "Don't blame only her — it takes two to tango."),
    ("Jump on the bandwagon", "присоединиться к модному течению", "to join an activity that has become popular", "Once the diet became trendy, everyone jumped on the bandwagon."),
    ("Keep your chin up", "не вешай нос", "stay cheerful in a difficult situation", "Keep your chin up — things will get better soon."),
    ("Kill two birds with one stone", "одним выстрелом убить двух зайцев", "to achieve two things with a single action", "By cycling to work I kill two birds with one stone — exercise and commute."),
    ("Leave no stone unturned", "перевернуть всё вверх дном в поисках", "to do everything possible to find something", "Detectives left no stone unturned in the investigation."),
    ("Make a long story short", "короче говоря", "to omit details and get to the point", "To make a long story short, we got lost and missed the flight."),
    ("Miss the boat", "упустить шанс", "to miss an opportunity", "If you don't apply today, you'll miss the boat."),
    ("No pain, no gain", "без труда не выловишь и рыбку", "you have to suffer to achieve something good", "Training hurts, but no pain, no gain."),
    ("On cloud nine", "на седьмом небе от счастья", "extremely happy", "She's been on cloud nine since she got engaged."),
    ("On the ball", "соображать, быть начеку", "alert and quick to understand", "Our new assistant is really on the ball."),
    ("Out of the blue", "как гром среди ясного неба", "completely unexpectedly", "He called me out of the blue after ten years."),
    ("Piece of cake", "пара пустяков", "very easy", "Fixing that bug was a piece of cake."),
    ("Pull yourself together", "возьми себя в руки", "to control your emotions and behave calmly", "Pull yourself together — crying won't help now."),
    ("Rain on someone's parade", "испортить кому-то праздник", "to spoil someone's plans or pleasure", "I hate to rain on your parade, but the picnic is cancelled."),
    ("See eye to eye", "сходиться во мнениях", "to agree with someone", "My sister and I rarely see eye to eye on politics."),
    ("Sit on the fence", "занимать выжидательную позицию", "to avoid making a decision or choice", "Stop sitting on the fence — are you with us or not?"),
    ("Steal someone's thunder", "перехватить чужую славу", "to take attention or praise away from someone", "She stole my thunder by announcing her promotion at my birthday dinner."),
    ("Take it with a grain of salt", "не принимай близко к сердцу", "to not completely believe something", "He exaggerates a lot, so take his stories with a grain of salt."),
    ("The best of both worlds", "и нашим и вашим", "the advantages of two different things at once", "Working from home gives me the best of both worlds — flexibility and focus."),
    ("Throw in the towel", "сдаться, выбросить белый флаг", "to admit defeat and stop trying", "After three failed attempts, he threw in the towel."),
    ("Time flies", "время летит", "time passes very quickly", "Time flies when you're having fun."),
    ("To make matters worse", "в довершение всего", "to make a bad situation even worse", "We were lost, and to make matters worse, it started raining."),
    ("Wrap your head around something", "уложить в голове, осмыслить", "to understand something difficult", "I can't wrap my head around how she finished so fast."),
    ("You can't have your cake and eat it too", "нельзя усидеть на двух стульях", "you can't have two desirable but incompatible things", "You want a high salary and short hours? You can't have your cake and eat it too."),
    ("A blessing in disguise", "не было бы счастья, да несчастье помогло", "something that seems bad but turns out to be good", "Missing that flight was a blessing in disguise — the next one had an empty row."),
    ("A dime a dozen", "пруд пруди", "very common and of no special value", "Cafés like this are a dime a dozen in the city centre."),
    ("Actions speak louder than words", "поступки говорят громче слов", "what people do is more important than what they say", "He promised to help, but actions speak louder than words."),
    ("Add insult to injury", "сыпать соль на рану", "to make a bad situation worse", "He forgot her birthday, and to add insult to injury, he went out with friends."),
    ("Against the clock", "в спешке, наперегонки со временем", "rushed and short of time", "We're working against the clock to ship the update tonight."),
    ("All ears", "весь внимание", "fully listening", "Tell me about your trip — I'm all ears."),
    ("All in the same boat", "в одной лодке", "in the same difficult situation", "Don't worry, we're all in the same boat with these new rules."),
    ("Apple of someone's eye", "свет очей, любимец", "a person who is loved more than any other", "His youngest daughter is the apple of his eye."),
    ("As easy as pie", "проще простого", "very easy", "Setting up the printer was as easy as pie."),
    ("At the drop of a hat", "по первому зову, без раздумий", "immediately, without hesitation", "She'd travel anywhere at the drop of a hat."),
    ("Back to square one", "вернуться к началу", "back to the starting point with no progress", "The deal fell through, so we're back to square one."),
    ("Back to the drawing board", "начинать всё с нуля", "to start planning something again because the first plan failed", "The prototype didn't work — back to the drawing board."),
    ("Barking up the wrong tree", "идти по ложному следу", "to be mistaken about the cause or solution", "If you think I broke it, you're barking up the wrong tree."),
    ("Beat a dead horse", "толочь воду в ступе", "to waste effort on something that has no chance of succeeding", "Arguing about it now is beating a dead horse."),
    ("Bend over backwards", "из кожи вон лезть", "to try very hard to please someone", "She bent over backwards to make her guests comfortable."),
    ("Best thing since sliced bread", "лучшее со времён изобретения колеса", "an excellent new invention or idea", "He thinks his new app is the best thing since sliced bread."),
    ("Birds of a feather flock together", "рыбак рыбака видит издалека", "people of similar character tend to associate", "Those two are always together — birds of a feather flock together."),
    ("Blood is thicker than water", "кровь не вода", "family relationships are stronger than other ties", "He chose to help his brother — blood is thicker than water."),
    ("Burn bridges", "сжигать мосты", "to destroy relationships permanently", "Don't burn your bridges with your old employer."),
    ("Burn the midnight oil", "работать допоздна", "to work late into the night", "I burned the midnight oil to finish the report."),
    ("Bury the hatchet", "зарыть топор войны", "to make peace after an argument", "After years of feuding, the brothers finally buried the hatchet."),
    ("Caught between two stools", "сидеть между двух стульев", "unable to choose between two alternatives", "I'm caught between two stools — both job offers are great."),
    ("Caught red-handed", "пойман с поличным", "caught in the act of doing something wrong", "The thief was caught red-handed leaving the shop."),
    ("Chip on your shoulder", "обида на весь мир", "a long-held resentment or grievance", "He has a chip on his shoulder about not going to university."),
    ("Costs the earth", "стоит баснословных денег", "is very expensive", "That handbag costs the earth."),
    ("Cross that bridge when you come to it", "решать проблемы по мере поступления", "to deal with a problem only when it arises", "We don't know if it'll rain — we'll cross that bridge when we come to it."),
    ("Cut to the chase", "перейти к сути", "to get to the point without wasting time", "Cut to the chase — what do you actually want?"),
    ("Devil's advocate", "адвокат дьявола", "someone who argues an opposing view for the sake of debate", "Let me play devil's advocate for a moment."),
    ("Down to the wire", "до самого конца", "until the very last possible moment", "The election went down to the wire."),
    ("Drop in the ocean", "капля в море", "a very small amount compared to what is needed", "The donation is generous, but it's a drop in the ocean."),
    ("Easier said than done", "легче сказать, чем сделать", "more difficult to do than to talk about", "Quitting sugar is easier said than done."),
    ("Eat humble pie", "признать свою неправоту", "to admit you were wrong", "He had to eat humble pie when his prediction failed."),
    ("Elephant in the room", "слон в комнате (очевидная проблема)", "an obvious problem no one wants to discuss", "Nobody mentioned the budget cuts — the elephant in the room."),
    ("Face the music", "отвечать за свои поступки", "to accept the unpleasant consequences of your actions", "Sooner or later he'll have to face the music."),
    ("Fish out of water", "не в своей тарелке", "uncomfortable in an unfamiliar situation", "I felt like a fish out of water at the formal dinner."),
    ("Fit as a fiddle", "здоровый, в отличной форме", "in very good health", "My grandfather is ninety and fit as a fiddle."),
    ("Get cold feet", "струсить в последний момент", "to suddenly become nervous about doing something", "He got cold feet the night before the wedding."),
    ("Get your act together", "взяться за ум", "to organise yourself and behave responsibly", "You need to get your act together before the deadline."),
    ("Give it a shot", "попробовать", "to attempt something", "I've never skied before, but I'll give it a shot."),
    ("Go down in flames", "потерпеть сокрушительное поражение", "to fail spectacularly", "The startup went down in flames within a year."),
    ("Goes without saying", "само собой разумеется", "obvious; not needing to be stated", "It goes without saying that we're grateful."),
    ("Hands are tied", "руки связаны", "unable to act because of rules or circumstances", "I'd love to help, but my hands are tied."),
    ("Have a blast", "отлично провести время", "to enjoy yourself a lot", "We had a blast at the concert last night."),
    ("Have bigger fish to fry", "есть дела поважнее", "to have more important things to do", "I can't deal with this now — I have bigger fish to fry."),
    ("Head over heels", "по уши влюблён", "completely in love", "He's head over heels for his new girlfriend."),
    ("Hit rock bottom", "достичь дна", "to reach the lowest possible point", "After losing everything, he hit rock bottom."),
    ("Hold your horses", "придержи коней", "wait a moment; slow down", "Hold your horses — let me finish my sentence."),
    ("In a nutshell", "в двух словах", "very briefly", "In a nutshell, the project was a success."),
    ("In the heat of the moment", "сгоряча", "while too excited or angry to think clearly", "I said things in the heat of the moment that I now regret."),
    ("It's a small world", "мир тесен", "said when you meet someone you know unexpectedly", "You know my cousin? It's a small world!"),
    ("Jump the gun", "забегать вперёд", "to do something too soon", "Don't jump the gun — wait for the official announcement."),
    ("Keep an eye on", "присматривать за", "to watch carefully", "Could you keep an eye on my bag for a moment?"),
    ("Keep your fingers crossed", "держать кулачки, надеяться на удачу", "to hope something will happen the way you want", "Keep your fingers crossed for my interview tomorrow."),
    ("Kick the bucket", "сыграть в ящик", "to die (informal, often humorous)", "The old fridge finally kicked the bucket last week."),
    ("Know the ropes", "знать все ходы и выходы", "to understand how something works", "Ask Maria — she knows the ropes around here."),
    ("Last but not least", "и наконец, что не менее важно", "the final item, but no less important than the others", "And last but not least, I want to thank my family."),
    ("Lend a hand", "помочь", "to help someone", "Could you lend a hand with these boxes?"),
    ("Let sleeping dogs lie", "не буди лихо, пока спит тихо", "to leave a situation alone to avoid causing trouble", "Don't bring up the argument — let sleeping dogs lie."),
    ("Light at the end of the tunnel", "свет в конце тоннеля", "a sign that a difficult time is ending", "After months of work, I finally see light at the end of the tunnel."),
    ("Lose your touch", "потерять навык, утратить хватку", "to no longer be able to do something well", "He used to be a great cook — I think he's losing his touch."),
    ("Make ends meet", "сводить концы с концами", "to have just enough money for what you need", "With three kids, it's hard to make ends meet."),
    ("Method to the madness", "в этом безумии есть смысл", "a logical reason behind apparent chaos", "It looks chaotic, but there's a method to the madness."),
    ("Miss the mark", "промахнуться, не попасть в цель", "to fail to achieve the intended result", "His joke missed the mark — nobody laughed."),
    ("Money doesn't grow on trees", "деньги не растут на деревьях", "money is not easy to get", "You can't buy that — money doesn't grow on trees."),
    ("Nip it in the bud", "пресечь в зародыше", "to stop something at an early stage", "We need to nip this rumour in the bud."),
    ("No strings attached", "без обязательств", "with no special conditions or restrictions", "It's a free trial, no strings attached."),
    ("Off the hook", "вне опасности, сорвался с крючка", "no longer in trouble", "She told the truth, so I'm off the hook."),
    ("Off the top of my head", "навскидку, не задумываясь", "without taking time to think carefully", "Off the top of my head, I'd say about fifty people came."),
    ("On the fence", "в нерешительности", "unable to decide between two options", "I'm still on the fence about taking the job."),
    ("On thin ice", "на тонком льду, в опасном положении", "in a risky situation", "After missing two deadlines, he's on thin ice."),
    ("Out of the frying pan into the fire", "из огня да в полымя", "from a bad situation to a worse one", "Switching jobs was out of the frying pan into the fire."),
    ("Over the moon", "на седьмом небе", "extremely pleased", "She was over the moon about her promotion."),
    ("Pain in the neck", "заноза, головная боль", "an annoying person or thing", "Filing taxes is a real pain in the neck."),
    ("Penny for your thoughts", "о чём задумался?", "what are you thinking about?", "You've been quiet all evening — penny for your thoughts?"),
    ("Pick up the slack", "взять на себя чужую работу", "to do extra work that someone else has not done", "When she went on leave, we all picked up the slack."),
    ("Play it by ear", "действовать по обстоятельствам", "to decide what to do as the situation develops", "We don't have firm plans — we'll play it by ear."),
    ("Practice makes perfect", "повторение — мать учения", "doing something repeatedly improves your skill", "Don't be discouraged — practice makes perfect."),
    ("Put all your eggs in one basket", "складывать все яйца в одну корзину", "to risk everything on a single venture", "Diversify your investments — don't put all your eggs in one basket."),
    ("Put your foot in your mouth", "сказать что-то неуместное", "to say something embarrassing or tactless", "I really put my foot in my mouth when I asked about her ex."),
    ("Read between the lines", "читать между строк", "to understand a hidden meaning", "Read between the lines — he's clearly unhappy with the offer."),
    ("Right as rain", "в полном порядке", "perfectly fine, especially in health", "After a good sleep, I'll be right as rain."),
    ("Rome wasn't built in a day", "Москва не сразу строилась", "important things take time", "Be patient with the renovation — Rome wasn't built in a day."),
    ("Rub someone the wrong way", "раздражать кого-то", "to annoy or irritate someone", "His attitude rubs me the wrong way."),
    ("Run like the wind", "бежать как ветер", "to run very fast", "When she heard the news, she ran like the wind."),
    ("Sail close to the wind", "ходить по краю", "to take risks by doing something almost illegal or improper", "Their tax strategy is sailing close to the wind."),
    ("Saved by the bell", "спасён в последний момент", "rescued from a difficult situation just in time", "The phone rang during the awkward silence — saved by the bell."),
    ("Shoot the breeze", "болтать ни о чём", "to chat casually about unimportant things", "We sat on the porch shooting the breeze for hours."),
    ("Sick and tired", "сыт по горло", "very annoyed by something", "I'm sick and tired of these excuses."),
    ("Sleep on it", "переспать с этой мыслью", "to delay a decision until the next day", "It's a big decision — sleep on it."),
    ("Smell a rat", "чуять неладное", "to suspect something is wrong", "When he changed the subject, I smelled a rat."),
    ("Spice things up", "внести разнообразие", "to make something more exciting", "Let's spice things up by trying a new restaurant."),
    ("Stab someone in the back", "ударить в спину, предать", "to betray someone", "I trusted him, but he stabbed me in the back."),
    ("Stick to your guns", "стоять на своём", "to refuse to change your opinion or plan", "Stick to your guns — don't let them pressure you."),
    ("Take a rain check", "перенести на другой раз", "to decline an offer with the suggestion of accepting later", "I can't make dinner tonight — can I take a rain check?"),
    ("Take it easy", "не переживай, расслабься", "to relax or not work hard", "Take it easy — there's no rush."),
    ("Take with a pinch of salt", "не принимать на веру", "to be sceptical about something", "Take his version of events with a pinch of salt."),
    ("Tear your hair out", "рвать на себе волосы", "to be very anxious or frustrated", "I was tearing my hair out trying to fix the bug."),
    ("The bigger picture", "общая картина", "the most important parts of a situation", "Try to look at the bigger picture, not just today's setback."),
    ("The cold hard truth", "горькая правда", "a harsh but real fact", "The cold hard truth is that we can't afford it."),
    ("The early bird catches the worm", "кто рано встаёт, тому Бог подаёт", "those who arrive first have the best chance of success", "Get there early — the early bird catches the worm."),
    ("The icing on the cake", "вишенка на торте", "an extra good thing added to something already good", "A bonus on top of the promotion was the icing on the cake."),
    ("The tip of the iceberg", "верхушка айсберга", "a small visible part of a much larger problem", "These complaints are just the tip of the iceberg."),
    ("Through thick and thin", "и в горе, и в радости", "in good times and in bad", "She stood by him through thick and thin."),
    ("Throw caution to the wind", "пуститься во все тяжкие", "to act without worrying about the risks", "He threw caution to the wind and quit his job to travel."),
    ("Tie the knot", "связать себя узами брака", "to get married", "They're tying the knot in June."),
    ("Tongue in cheek", "не всерьёз, с иронией", "said as a joke, not meant seriously", "His comment was tongue in cheek — don't take it personally."),
    ("Turn a blind eye", "закрыть глаза на что-то", "to ignore something you know is wrong", "Managers turned a blind eye to the late arrivals."),
    ("Twist someone's arm", "выкручивать руки, заставлять", "to persuade someone to do something they don't want to do", "I had to twist his arm, but he agreed to come."),
    ("Under your nose", "прямо под носом", "very close to you but not noticed", "The keys were right under your nose the whole time."),
    ("Up in the air", "в подвешенном состоянии", "uncertain, undecided", "Our holiday plans are still up in the air."),
    ("Walk on eggshells", "ходить по тонкому льду", "to be very careful about what you say or do", "Since the argument I've been walking on eggshells around her."),
    ("Water under the bridge", "дело прошлое", "something in the past that is no longer important", "We had our differences, but that's water under the bridge now."),
    ("When pigs fly", "когда рак на горе свистнет", "something that will never happen", "He'll apologise when pigs fly."),
    ("Whole nine yards", "всё до последнего, по полной", "everything possible; the full extent", "For the wedding she went the whole nine yards — orchestra, fireworks, the lot."),
    ("Wild goose chase", "погоня за призраком", "a useless and time-wasting search", "He sent us on a wild goose chase across town."),
    ("With flying colours", "с блеском, на отлично", "with great success", "She passed her driving test with flying colours."),
    ("Word of mouth", "сарафанное радио", "spoken communication, especially recommendation", "The restaurant became popular by word of mouth."),
    ("You can say that again", "вот именно, не то слово", "I completely agree", "It's freezing today! — You can say that again."),
    ("A bird in the hand is worth two in the bush", "лучше синица в руках, чем журавль в небе", "it is better to have something certain than the possibility of more", "Take the offer — a bird in the hand is worth two in the bush."),
    ("A penny saved is a penny earned", "копейка рубль бережёт", "money you save is just as valuable as money you earn", "I bring lunch from home — a penny saved is a penny earned."),
    ("Ace up your sleeve", "козырь в рукаве", "a hidden advantage", "She's quiet now, but she has an ace up her sleeve."),
    ("All bark and no bite", "лает, да не кусает", "threatening but not actually willing to act", "Don't worry about him — he's all bark and no bite."),
    ("Around the clock", "круглые сутки", "all day and all night", "The bakery operates around the clock."),
    ("At a crossroads", "на распутье", "at a point where an important decision must be made", "I'm at a crossroads in my career."),
    ("At loggerheads", "на ножах, в конфликте", "in strong disagreement", "The two departments have been at loggerheads for months."),
    ("Back to basics", "вернуться к основам", "returning to the simplest, most important elements", "Our coach took us back to basics this week."),
    ("Bark up the wrong tree", "идти по неверному пути", "to make a wrong assumption about something", "If you think I leaked it, you're barking up the wrong tree."),
    ("Beat the clock", "успеть в срок", "to finish before the deadline", "We just beat the clock with the submission."),
    ("Behind the eight ball", "в невыгодном положении", "in a difficult position", "Missing that meeting put me behind the eight ball."),
    ("Bite your tongue", "прикусить язык", "to stop yourself from saying something", "I had to bite my tongue when she criticised my work."),
    ("Blow off steam", "выпустить пар", "to release pent-up emotion or energy", "I went for a run to blow off steam."),
    ("Bring home the bacon", "приносить домой деньги, кормить семью", "to earn money for the household", "She's been bringing home the bacon since they moved."),
    ("Burn the candle at both ends", "работать на износ", "to exhaust yourself by doing too much", "You'll get sick if you keep burning the candle at both ends."),
    ("Caught off guard", "застать врасплох", "surprised because not prepared", "His question caught me off guard."),
    ("Clear the air", "разрядить обстановку", "to discuss a problem to remove tension", "Let's meet and clear the air about what happened."),
    ("Come hell or high water", "несмотря ни на что", "no matter what difficulties arise", "Come hell or high water, I'll finish this thesis."),
    ("Come out of your shell", "стать более общительным", "to become more open and confident with others", "Since starting drama club, she's come out of her shell."),
    ("Cool as a cucumber", "невозмутимый, спокойный как удав", "very calm, especially under pressure", "She stayed cool as a cucumber during the interview."),
    ("Cross your fingers", "скрестить пальцы на удачу", "to hope for good luck", "Cross your fingers that the weather holds."),
    ("Cut a long story short", "короче говоря", "to give a shortened account", "To cut a long story short, we won."),
    ("Down in the dumps", "в унынии, расстроен", "feeling sad", "He's been down in the dumps since the breakup."),
    ("Drink like a fish", "пить как сапожник", "to drink alcohol heavily", "He drinks like a fish at every party."),
    ("Drive someone up the wall", "выводить из себя", "to make someone very annoyed", "That noise is driving me up the wall."),
    ("Eat your words", "взять свои слова обратно", "to admit that what you said was wrong", "He had to eat his words after we proved him wrong."),
    ("Every dog has its day", "и на нашей улице будет праздник", "everyone gets a chance eventually", "Don't give up — every dog has its day."),
    ("Eyes bigger than your stomach", "глаза завидущие", "wanting more food than you can eat", "I ordered too much — my eyes were bigger than my stomach."),
    ("Feel under the weather", "чувствовать недомогание", "feel slightly unwell", "I'm feeling a bit under the weather, so I'll skip dinner."),
    ("Few and far between", "очень редкие, на вес золота", "rare and infrequent", "Sunny days here are few and far between."),
    ("Fight tooth and nail", "бороться зубами и когтями", "to fight with great determination", "She fought tooth and nail for that promotion."),
    ("Find your feet", "освоиться, найти своё место", "to become comfortable in a new situation", "It took me a month to find my feet at the new job."),
    ("Fit the bill", "подходить, соответствовать", "to be exactly what is needed", "This little café fits the bill perfectly."),
    ("From scratch", "с нуля", "from the very beginning, with nothing prepared", "She baked the cake from scratch."),
    ("Get a kick out of", "получать удовольствие от", "to enjoy something a lot", "He gets a real kick out of teaching kids to swim."),
    ("Get the ball rolling", "запустить процесс, начать дело", "to start something happening", "Let's get the ball rolling on the new project."),
    ("Give the benefit of the doubt", "поверить на слово, не сомневаться", "to believe someone is telling the truth even when uncertain", "He's late, but I'll give him the benefit of the doubt this once."),
    ("Go against the grain", "идти против течения", "to do the opposite of what is usual or expected", "Quitting law school went against the grain in his family."),
    ("Grasp at straws", "хвататься за соломинку", "to try desperately to find any solution", "Suggesting that idea was just grasping at straws."),
    ("Have a heart of gold", "иметь золотое сердце", "to be very kind and generous", "She'll help anyone — she has a heart of gold."),
    ("Heads will roll", "полетят головы", "people will be punished severely", "If this leak gets out, heads will roll."),
    ("In the same boat", "в одной лодке", "in the same difficult situation as others", "We're all in the same boat with this delay."),
    ("Jump for joy", "прыгать от радости", "to be very happy", "She jumped for joy when she got the call."),
    ("Keep your head above water", "держаться на плаву", "to manage to survive financially or in difficulty", "With two jobs I'm just keeping my head above water."),
    ("Like two peas in a pod", "как две капли воды", "very similar, especially two people", "The twins are like two peas in a pod."),
    ("Long story short", "короче говоря", "summarising briefly", "Long story short, we missed our connection."),
    ("Lose your cool", "выйти из себя", "to become very angry", "Try not to lose your cool during the negotiation."),
]

# Защита: проверяем, что ровно 200
# Удаляем смысловые дубликаты-варианты и наименее популярные,
# чтобы получить ровно 200 идиом
_REMOVE = {
    "Piece of cake",                  # дубль "A piece of cake"
    "Long story short",               # дубль "Make a long story short"
    "Cut a long story short",         # дубль "Make a long story short"
    "Feel under the weather",         # дубль "Under the weather"
    "In the same boat",               # дубль "All in the same boat"
    "On the fence",                   # дубль "Sit on the fence"
    "Take with a pinch of salt",      # дубль "Take it with a grain of salt"
    "Bark up the wrong tree",         # дубль "Barking up the wrong tree"
    "Run like the wind",
    "Sail close to the wind",
    "Shoot the breeze",
    "Spice things up",
    "Behind the eight ball",
    "Blow off steam",
    "Drink like a fish",
    "Eyes bigger than your stomach",
    "Heads will roll",
    "From scratch",
    "Costs the earth",
    "Method to the madness",
    "Lose your touch",
    "Find your feet",
    "Grasp at straws",
    "Stab someone in the back",
}
IDIOMS = [i for i in IDIOMS if i[0] not in _REMOVE]

# Защита: проверяем, что ровно 200
if __name__ == "__main__":
    assert len(IDIOMS) == 200, f"Ожидалось 200 идиом, получено {len(IDIOMS)}"

# Проверяем уникальность
seen = set()
duplicates = []
for idiom in IDIOMS:
    key = idiom[0].lower().strip()
    if key in seen:
        duplicates.append(idiom[0])
    seen.add(key)
assert not duplicates, f"Найдены дубликаты: {duplicates}"


def cambridge_url(idiom: str) -> str:
    """Формирует ссылку на Cambridge Dictionary."""
    # Cambridge использует слаги вида: piece-of-cake, break-a-leg, etc.
    slug = idiom.lower()
    # Удаляем апострофы и непечатные символы
    for ch in [",", ".", "'", "'", "!", "?", ":", ";", "(", ")"]:
        slug = slug.replace(ch, "")
    slug = "-".join(slug.split())
    return f"https://dictionary.cambridge.org/dictionary/english/{quote(slug)}"


data = []
for i, (idiom, ru, meaning, example) in enumerate(IDIOMS, start=1):
    data.append({
        "id": i,
        "idiom": idiom,
        "translation_ru": ru,
        "meaning_en": meaning,
        "example_en": example,
        "cambridge_url": cambridge_url(idiom),
    })

with open("idioms.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"OK: записано {len(data)} идиом в idioms.json")
print(f"Пример первой: {data[0]}")
print(f"Пример последней: {data[-1]}")
