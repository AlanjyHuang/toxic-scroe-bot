from telegram.ext import *
import telegram
import requests
import configparser
import os
from Toxic import Toxic
userdata={}
userscore={}
class telbot:
    def __init__(self):
        self.read_token()
        self.toxic=Toxic()

    def read_token(self):
       self.config = configparser.ConfigParser()
       self.config.read('config.ini')
       print(self.config['TELBOT'])
       

    def startbot(self):
        # 初始化bot
        self.bot=telegram.Bot(token=self.config['TELBOT']['token'])
        self.updater = Updater(token=self.config['TELBOT']['token'],use_context=False)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CommandHandler('hi', self.hi))
        self.dispatcher.add_handler(CommandHandler('toxic_score', self.toxic_score))
        self.dispatcher.add_handler(CommandHandler('toxic_report', self.toxic_report))
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.reply_handler))
        

    def hi(self,bot, update): # 新增指令/start
        message = update.message
        chat = message['chat']
        update.message.reply_text(text='HI  ' + str(chat['first_name'])+' '+str(chat['last_name']))

    def reply_handler(self,bot, update):
        print("got it")
        message = update.message
        chat = message['chat']
        update.message.reply_text(text="Testing toixc score, please wait ....")
        text = update.message.text
        back=self.toxic.predict(text)
        score=int((back.mean())*100)
        update.message.reply_text(text="Your toxic score of  \""+str(text)+"\" is "+str(score))
        user=str(chat['first_name'])+' '+str(chat['last_name'])
        userdata[user]=text
        userscore[user]=score

    def toxic_score(self,bot, update):
        message = update.message
        chat = message['chat']
        user=str(chat['first_name'])+' '+str(chat['last_name'])
        if userscore.get(user):
            score=userscore[user]
            if 0<=score<=20:
                self.bot.send_photo(chat_id=chat['id'], photo=open('picfolder/0.jpg', 'rb'))
                update.message.reply_text(text=" 你太善良了")
            elif 20<score<=40:
                self.bot.send_photo(chat_id=chat['id'], photo=open('picfolder/1.jpg', 'rb'))
                update.message.reply_text(text="男人不壞 女人不愛")
            elif 40<score <= 60:
                self.bot.send_photo(chat_id=chat['id'], photo=open('picfolder/2.jpg', 'rb'))
                update.message.reply_text(text="你超壞!")
            elif 60<score <= 80:
                self.bot.send_photo(chat_id=chat['id'], photo=open('picfolder/3.jpg', 'rb'))
                update.message.reply_text(text="你死掉後會下地獄")
            elif 80<score <= 100:
                self.bot.send_photo(chat_id=chat['id'], photo=open('picfolder/4.jpg', 'rb'))
                update.message.reply_text(text="NMSL")
        else:
            update.message.reply_text(text="You have no latest toxic comment")
    def toxic_report(self,bot,update):
        message = update.message
        chat = message['chat']
        user=str(chat['first_name'])+' '+str(chat['last_name'])
        
        if userdata.get(user):
            back=self.toxic.predict(userdata[user])
            score=int((back.mean())*100)
            update.message.reply_text(text=self.make_report(user,userdata[user],int(back[0]*100),int(back[1]*100),int(back[2]*100),int(back[3]*100),int(back[4]*100),int(back[5]*100),score))
        else:
            update.message.reply_text(text="You have no latest toxic comment")
    
    def make_report(self,user,wd,s1,s2,s3,s4,s5,s6,score):
        text="===================================================\n"
        text+=(user+"\'s Toxic Report \n")
        text+="*************************************************\n"
        text+=("\""+wd+"\"\n")
        text+="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n"
        text+=("Toxic : "+str(s1)+"\n")
        text+="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n"
        text+=("Servere toxic : "+str(s2)+"\n")
        text+="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n"
        text+=("Obscene : "+str(s3)+"\n")
        text+="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n"
        text+=("Threat : "+str(s4)+"\n")
        text+="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n"
        text+=("Insult : "+str(s5)+"\n")
        text+="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n"
        text+=("Identity hate : "+str(s6)+"\n")
        text+="*************************************************\n"
        text+=("Your total score is : "+str(score)+"\n")
        text+="===================================================\n"
        return text

    # def set_host(self,bot,update):
    #     message = update.message
    #     newhost=update.message['text']
    #     chat = message['chat']
    #     if chat['id']==os.environ.get('admin_ID'):    
    #         print(str(chat['first_name'])+' '+str(chat['last_name'])+" setup new host as: ",newhost)
    #         self.host=newhost
    #         update.message.reply_text(text='new host is :'+str(self.host))
    #     else :
    #         update.message.reply_text(text='Sorry you are not an admin')

    def off(self,bot,update):
        print("turn off")
        self.updater.stop()

    


if __name__=='__main__':
    mybot=telbot()
    mybot.startbot()
    mybot.updater.start_polling()
    
"""     while True:
        text = input()
        # Gracefully stop the event handler
        if text == 'stop':
            mybot.updater.stop()
            break

        # else, put the text into the update queue to be handled by our handlers
        elif len(text) > 0:
            mybot.update_queue.put(text) """
