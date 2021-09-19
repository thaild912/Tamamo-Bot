import json

db = {}


db['Servants'] = ["Tamamo no Mae", "Tamamo Cat", "Tamamo Summer", "Tamamo Vicchi", "Tamamo of Knowledge"]


db['command'] = {}


db['command']['list'] = ['help', 'intro', 'welcome', 'henshin <persona>', 'purge',  'selfie', 'fetchPDT', 'upcomingbanner <number> (deprecated)', 'rateup <servant name> {deprecated)']
db['command']['help'] = {}
db['command']['help']['intro'] = "**A brief introduction about us. Please be serious.**\n120s cooldown."
db['command']['help']['welcome'] = "**Send a heart warming welcome, not from me.**\n30s cooldown."
db['command']['help']['henshin <persona>'] = "**Changes persona. Set parameter empty to change to the next available persona. In the case that you need help, which is almost a certainty, then remember that <3henshin help exists.**\n30s cooldown."
db['command']['help']['help'] = "**You are already here.\n5s cooldown."
db['command']['help']['purge'] = "**Vicchi's lines cleanup service. Parameter is the number of lines from this bot will be deleted.**\n5s cooldown."
db['command']['help']['selfie'] = "**Show a cute picture of the cutest creature in the universe, which happens to share the same appearance as me.**\n10s cooldown"
db['command']['help']['fetchPDT'] = "**Return PDT time.**\n5s cooldown"
db['command']['help']['upcomingbanner <number> (deprecated)'] = "**Show <number> of upcoming banner in FGONA. Only works up until FGONA's 2022 new year banner.**\nDeprecated since FGO Cirnopedia is no longer update and my Master is no longer a FGO Master.\n60s cooldown"
db['command']['help']['rateup <servant name> {deprecated)'] = "**Show upcomming rateup for a specific servant. Only works up until FGONA's 2022 new year banner.**\nDeprecated for the same reason as above.\n30s cooldown."

db['command']['welcome'] = {}
db['command']['welcome']['OG'] = {'undiscovered': {}, 'discovered': {'dinner': {}, 'bath': {}, 'tamamo': {}}}
db['command']['welcome']['OG']['undiscovered']['start'] = "Mikon! Welcome back Master!"
db['command']['welcome']['OG']['discovered']['start'] = "Mikon! Welcome home My Husband %s."
db['command']['welcome']['OG']['discovered']['lines'] = ["Do you want dinner first?",
                                                         "Or bath first?",
                                                         "Or perhaps...",
                                                         "わ。",
                                                         "た。",
                                                         ["し。", "ᵘᶠᵘᶠᵘ♡"]]
db['command']['welcome']['OG']['discovered']['dinner']['start'] = 'Yes, Tamamo will gladly show My Husband the power of my housewife skill.'
db['command']['welcome']['OG']['discovered']['dinner']['lines'] = ["Time to put these lesson I've learned in Benni-enma's class into action!"]
db['command']['welcome']['OG']['discovered']['bath']['start'] = "I've prepared the water and the bath for you, My Husband. Please get in."
db['command']['welcome']['OG']['discovered']['bath']['lines'] = ["Or..perhaps...you want us to get in together and clean each other's back, My Husband...?"]
db['command']['welcome']['OG']['discovered']['bath']['timeout'] = {'start': "Still indecisive?"}
db['command']['welcome']['OG']['discovered']['bath']['timeout']['lines'] = ["Then it's decided. Tamamo will be the one to give My Husband the best back cleaning ever.",
                                                                            ["And you know it's not limited to back either right?", '*ʷᶦⁿᵏ ʷᶦⁿᵏ']]
db['command']['welcome']['OG']['discovered']['bath']['yes'] = {'start': "Then it's decided. Tamamo will be the one to give My Husband the best back cleaning ever."}
db['command']['welcome']['OG']['discovered']['bath']['yes']['lines'] = [["And you know it's not limited to back either right?",'*ʷᶦⁿᵏ ʷᶦⁿᵏ']]
db['command']['welcome']['OG']['discovered']['bath']['no'] = {'start': "*sob sob. And I was going to give you the best back cleaning ever, My Husband."}
db['command']['welcome']['OG']['discovered']['bath']['no']['lines'] = ["But well, that alone won't be able to discourage me.",
                                                                       'Please get in the bath, My Husband, and in the meanwhile I will prepare you a dinner.',
                                                                       "If I can't take down you with my superior housewife back-cleaning skill then I will do it with my cooking skill.",
                                                                       "Please look forward to it, My Husband!"]
db['command']['welcome']['OG']['discovered']['tamamo']['start'] = ["Gasp! My Husband has finally awoken his libido.", 'ᵍʳᵉᵃᵗ ʲᵒᵇ ᵐʸ ˢᵉˡᶠ']
db['command']['welcome']['OG']['discovered']['tamamo']['lines'] = ["But my heart isn't ready for this! Kyaa!",
                                                                   "So if you don't mind, %s...",
                                                                   "...could you please take the lead...?"]
db['command']['welcome']['Cat'] = {'start': ["Woof! Welcome back, Master %s. How was your day?", "ʷᵃᵍ ʷᵃᵍ"]}
db['command']['welcome']['Cat']['lines'] = [["You must be hungry. But don't worry because Cat has already cooked you a dinner! Sit down and eat up, Master!", "ʷᵃᵍ ʷᵃᵍ"]]
db['command']['welcome']['Vicchi'] = {'start': "Welcome, Master %s. Looks like you have worked hard today."}
db['command']['welcome']['Vicchi']['lines'] = ["I've taken the liberty of booking a table for us at the nearby formal restaurant.",
                                               "Now if you'll excuse me, I'll help you change your attire, and then we will go out.", "ʰᵃⁿᵈ ʷᵃⁿᵈᵉʳˢ"]
db['command']['welcome']['Knowledge'] = {'not_bonded':{}, 'bonded':{}}
db['command']['welcome']['Knowledge']['not_bonded']['start'] = "Ara, isn't that my stupid master?"
db['command']['welcome']['Knowledge']['not_bonded']['lines'] = ["Welcome home."]
db['command']['welcome']['Knowledge']['bonded']['start'] = "Ara, looks who have done messing around, %s-kun."
db['command']['welcome']['Knowledge']['bonded']['lines'] = ["Ara, I do not look like I'm was awaiting to your return, you say?",
                                                            "Why should I, %s-kun?",
                                                            "It's becaise we are lovers, %s-kun?",
                                                            ["Very well. Since you have said such sincere thing, and since I'm such an awesome being, I will let you go this time.", "ᵈᵒⁿ'ᵗ ᵖᵘˢʰ ʸᵒᵘʳ ˡᵘᶜᵏ ᵃᵍᵃᶦⁿ"],
                                                            "Then, for dinner, your wonderful lover, me, in particular, have prepared the ingredients for your favorite meal. Be grateful, %s-kun.",
                                                            "Also, I've gone out of my way prepared the bath for you, so hurry up and get in so I can clean your back, %s-kun.",
                                                            "After bath, I shall grant you the privilege to fluff my tail all you want while I cook your dinner, so look forward to it.",
                                                            "What will we have for dessert? Ara, aren't you greedy, %s-kun?",
                                                            "It will be Me, with chocolate on top, of course."]
db['command']['welcome']['Summer'] = {'not_bonded':{}, 'bonded':{}}
db['command']['welcome']['Summer']['not_bonded']['start'] = "Mikon! Welcome home Master!"
db['command']['welcome']['Summer']['not_bonded']['lines'] = ["Looks like you've had a hardworking day. Perhaps you would want a back massage, Master?"]
db['command']['welcome']['Summer']['not_bonded']['timeout'] = ["Poor Master, he must be really tired."]
db['command']['welcome']['Summer']['not_bonded']['yes'] = ['Mikon! Roger that!']
db['command']['welcome']['Summer']['not_bonded']['no' = ['Well if you ever need one then I will always be available!']
db['command']['welcome']['Summer']['bonded']['start'] = "Panpakapan! Welcome back to our love nest, Master %s!"
db['command']['welcome']['Summer']['bonded']['lines'] = ["Heavens me, you must be tired form all the works.",
                                                         "Don't worry, I know something that can relieve your stress! It's Bathing!",
                                                         "So hurry up Master! Let's get into the bath! I won't take no for an answer!",
                                                         ["I will make sure that you drown in heavenly pleasure! Mikon!", "ʰᵉʰᵉʰᵉʰ"],
                                                         "Now, please don't make a lady wait and get in the bath, Master. Else, you will why people called me 'Beast of Summer ♡'."]



db['command']['henshin'] = {'error':{}, 'help':{}, 'Knowledge':{}, 'OG':{}, 'Cat':{}, 'Vicchi':{}, 'Summer or Shark':{}}
db['command']['henshin']['error']['start'] = ["Henshin failed.", "ʳᵉᵃˡˡʸˀ"]
db['command']['henshin']['error']['lines'] = [["There is only a handful of us, and most of our names are cutesy, yet you can't remember them.","ᴴᵒʷ ᵘᵗᵗᵉʳˡʸ ᵈᵉˢᵖᶦᶜᵃᵇˡᵉ"],
                                              ["We are dissapointed.","ᵖˡᵉᵃˢᵉ ᵇᵉᵍᵒⁿᵉ"],
                                              "Go consult !help for more information regarding this command."]
db['command']['henshin']['help']['Henshin.help'] = "Well at least this time that decorative brain of yours know how to ask for help. So I will do you a favor out of kindness and give you the parameters:"
db['command']['henshin']['help']['Knowledge'] = "**Changes persona to the smart, lovable and superior Tamamo.**"
db['command']['henshin']['help']['OG'] = '**Changes persona to the inferior Tamamo.**'
db['command']['henshin']['help']['Cat'] = '**Changes persona to that Cat.**'
db['command']['henshin']['help']['Vicchi'] = '**Changes persona to Bicchi.**'
db['command']['henshin']['help']['Summer or Shark'] = '**Changes persona to the horny Original.**'
db['command']['henshin']['help']['Leave the field blank to'] = '**Changes persona to the next one available.**'
db['command']['henshin']['help']['footer'] = "And in case that little brain of you forget, all the parameters are not case sensitive."
db['command']['henshin']['help']['start'] = "Wait, why am I the only one getting the inferior treatment!"

db['command']['henshin']['OG']['start'] = "Greetings Master %s."
db['command']['henshin']['OG']['lines'] = {'undiscovered':["Tamamo no Mae, reporting!~"]}
db['command']['henshin']['OG']['lines']['discovered'] = ["Your beloved Casko has come back.",
                                                         "I will continue to try to be the best wife ever for you, Mikon!"]
db['command']['henshin']['Cat']['start'] = ["Woof! Cat is here, Master %s!", "ʷᵃᵍ ʷᵃᵍ"]
db['command']['henshin']['Cat']['image'] = ["Please pet me Master! =uwu=", 'https://i.imgur.com/2qaXLhF.jpg', "ʷᵃᵍ ʷᵃᵍ"]
db['command']['henshin']['Summer']['not_bonded'] = {'start':"Hello Master %s! Tamamo Summer is here~!"}
db['command']['henshin']['Summer']['not_bonded']['lines'] = "The weather is beautifu today, so why not change into swimsuit and enjoy ourselves on the beach, Master!"
db['command']['henshin']['Summer']['bonded'] = {'start':"Hello Master %s! Tamamo Shark is here~!"}
db['command']['henshin']['Summer']['bonded']['lines'] = ["What? You are asking why I used the nickname 'Tamamo Shark' instead of 'Tamamo Summer'?",
                                                         "You know shark likes to eat people riiight?",
                                                         "Well, the same goes for me...",
                                                         "Master...you look too delicious...."]
db['command']['henshin']['Summer']['bonded']['image'] = ["It would be a waste...to not gobble you up completely...m.a.s.t.e.r...", 'https://i.imgur.com/3pXbUlU.png', 'ᵘᶠᵘᶠᵘ♡']
db['command']['henshin']['Vicchi']['start'] = "Rest assured, Master %s, for your Tamamo Vicchi is here."
db['command']['henshin']['Vicchi']['lines'] = ["Whether it's office works, infiltration, espionage or assassinations, I will get it done."]
db['command']['henshin']['Knowledge']['not_bonded'] = {'start':"Caster Tamamo of Knowledge, your personal Strategist is here."}
db['command']['henshin']['Knowledge']['not_bonded']['lines'] = ["I guess you didn't just call me out for shits and giggles right?",
                                                                "So speak up, what kind of bussiness do you need my help with?"]
db['command']['henshin']['Knowledge']['bonded'] = {'start':"Caster Tamamo of Knowledge, your personal Strategist-Girlfriend is here."}
db['command']['henshin']['Knowledge']['bonded']['knowledgebox'] = [["Ara, I see that you have been acting unbelievably stupid and reckless since I were gone, right ", "?"],
                                                                   ["As expected of you, having become totally dependent on me, you are not able to do anything properly anymore, ", "."],
                                                                   ["But please refrain yourself from acting rashly from now on, as it would be troubling to the medical staff and Mashu, and other Tamamo if you get injured in the middle of you action, ", "."],
                                                                   ["Otherwise I will not forgive you the next time you injured yourself due to not using your brain, ", "."],
                                                                   ["What, I'm being to harsh on you, ", "?"],
                                                                   ["Are you perhaps expecting me to be sweeter toward you because I'm your girlfriend, ", "?"],
                                                                   "Then it's impossible, I'm a tsundere after all.",
                                                                   ["And isn't that a Strategist/Girlfriend 's responsibility is to keep their loved one, in this case, you, alive, right ", "?"],
                                                                   ["So stop complaining, be grateful and do as I said, ", "."],
                                                                   "Idiot.",
                                                                   ["Just kidding. Did you think I would really say that, ", "?"],
                                                                   ["On the second thought, I might actually say that. Since your IQ is indeed that low after all, ", "."]]
