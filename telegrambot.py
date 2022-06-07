from telegram.ext import *
import telegram
import requests
import configparser
import os
userdata={}

class telbot:
    def __init__(self):
        self.read_token()
        

    def read_token(self):
       self.config = configparser.ConfigParser()
       self.config.read('config.ini')
       print(self.config['TELBOT'])
       

    def startbot(self):
        # 初始化bot
        self.updater = Updater(token=self.config['TELBOT']['token'],use_context=False)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CommandHandler('hi', self.hi))
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
        score=90
        update.message.reply_text(text="Your toxic score of  \""+str(text)+"\" is "+str(score))
        user=str(chat['first_name'])+' '+str(chat['last_name'])
        userdata[user]=text

    def toxic_report(self,bot,update):
        message = update.message
        chat = message['chat']
        user=str(chat['first_name'])+' '+str(chat['last_name'])
        if userdata.get(user):
            update.message.reply_text(text=self.make_report(user,userdata[user],1,2,3,4,5,6,90))
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