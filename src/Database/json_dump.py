import json


inputstr = '''
{
    "People": {
        "Ikaros": {
            "ID" : "357182434946842625",
            "Callable" : "<@!357182434946842625>"
        },
        "Remine The Cat": {
            "ID": "323666728716599308",
            "Callable": "<@!323666728716599308>"
        },
        "Luella": {
            "ID": "346311438144372736",
            "Callable": "<@!346311438144372736>"
        },
        "Zeeees": {
             "ID": "317254725823365131",
            "Callable": "<@!317254725823365131>"
        },
        "AmagiriAyato": {
            "ID": "453207669701083136",
            "Callable": "<@!453207669701083136>"
        },
        "SukvatELuck": {
            "ID": "486570686324670485",
            "Callable": "<@!486570686324670485>"
        },
        "KypxZ": {
            "ID": "276709770100998146",
            "Callable": "<@!276709770100998146>"
        }    
    },
    "Bots": {
        "TamamoBot": {
             "ID": "587563434577625088",
            "Callable": "<@!587563434577625088>"
        },
        "KiaraBot": {
            "ID": "587684210266079264",
            "Callable": "<@!587684210266079264>"
        }
    },
    "Server": {
        "BotToken": "NTg3NTYzNDM0NTc3NjI1MDg4.XP9B7A.RmEl2P8ZEK8kaHFaxa0i8Tb0iUg",
        "ClientID": "587563434577625088",
        "PrimChannelID": "493267174262308875",
        "PrimTestID": "587565335763484694",
        "Redis": "redis://h:p344993de1a481c1c6e4bb8c378f86ded8e752bd5f26694ca36a9b8d312a0fb58@ec2-52-2-161-194.compute-1.amazonaws.com:14109"
    },
    "Persona": {
        "Tamamo no Mae": {
            "Color": "0x2f25dc",
            "Expression": {
                "Normal": {
                    "URL": "https://i.imgur.com/DFeXJ8o.png",
                    "Source": "Wada Arco"
                },
                "Riyo": {
                    "URL": "https://i.imgur.com/odsWRbo.png",
                    "Source": "Riyo"
                },
                "Cry": {
                    "URL": "",
                    "Source": ""
                },
                "Angry": {
                    "URL": "",
                    "Source": ""
                },
                "Blush": {
                    "URL": "",
                    "Source": ""
                }
            },  
            "Booru": {
                "SFW": "https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=rating%3asafe+animal_ears+tamamo_no_mae_%28fate%29+-tamamo_cat_%28fate%29+-tamamo_no_mae_%28swimsuit_lancer%29_%28fate%29+-tamamo_%28assassin%29_%28fate%29+-koyanskaya+1girl+-straw_hat&json=1",
                "NSFW": ""
            }
        },
        "Tamamo Cat": {
            "Color" : "0xfb0909",
            "Expression": {
                "Normal": {
                    "URL": "https://i.imgur.com/WFz2ilV.png",
                    "Source": "https://www.pixiv.net/member_illust.php?mode=medium&illust_id=75063630"
                },
                "Riyo": {
                    "URL": "https://i.imgur.com/qEcT6Xg.png",
                    "Source": "Riyo"
                },
                "Cry": {
                    "URL": "https://i.imgur.com/x5mp0x6.png",
                    "Source": "Wada Arco"
                },
                "Angry": {
                    "URL": "https://i.imgur.com/tonwJsV.png",
                    "Source": "Riyo"
                },
                "Blush": {
                    "URL": "",
                    "Source": ""
                }
            },
            "Booru": {
                "SFW": "",
                "NSFW": ""
            }
        },
        "Tamamo Summer": {
            "Color": "0x52d6e0",
            "Expression": {
                "Normal": {
                    "URL": "",
                    "Source": ""
                },
                "Riyo": {
                    "URL": "",
                    "Source": ""
                },
                "Cry": {
                    "URL": "",
                    "Source": ""
                },
                "Angry": {
                    "URL": "",
                    "Source": ""
                },
                "Blush": {
                    "URL": "",
                    "Source": ""
                }
            },
            "Booru": {
                "SFW": "",
                "NSFW": ""
            }
        },
        "Tamamo Vicchi": {
            "Color": "0xdf24df",
            "Expression": {
                "Normal": {
                    "URL": "",
                    "Source": ""
                },
                "Riyo": {
                    "URL": "",
                    "Source": ""
                },
                "Cry": {
                    "URL": "",
                    "Source": ""
                },
                "Angry": {
                    "URL": "",
                    "Source": ""
                },
                "Blush": {
                    "URL": "",
                    "Source": ""
                }
            },
            "Booru": {
                "SFW": "",
                "NSFW": ""
            }
        },
        "Tamamo Rabbit": {
            "Color": "0x5e56e4",
            "Expression": {
                "Normal": {
                    "URL": "https://i.imgur.com/49Tk8Yv.png",
                    "Source": "Wada Arco"
                },
                "Riyo": {
                    "URL": "",
                    "Source": ""
                },
                "Cry": {
                    "URL": "",
                    "Source": ""
                },
                "Angry": {
                    "URL": "",
                    "Source": ""
                },
                "Blush": {
                    "URL": "",
                    "Source": ""
                }
            },
            "Booru": {
                "SFW": "",
                "NSFW": ""
            }
        }
    }
}
'''

data = json.loads(inputstr)
with open("info.json", 'w+') as f:
    json.dump(data, f, indent = 3)
    