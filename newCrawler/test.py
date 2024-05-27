from PTTLibrary import PTT
ID = "kailovemoon"
Password = "111111"
PTTBot = PTT.Library()
ErrCode = PTTBot.login(ID, Password)
PTTBot.logout()