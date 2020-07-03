
import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Voice)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, )

from teleBotDatabase import TeleDB

db = TeleDB()
db.setup()



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

FILL, NAME, COLLEGE, SIDEPROJECT, PLANGUAGE, MULTIPLESELECT, FRAMEWORK,CHECKFRAMEWORK, PROJECTS, PSKILLS, GITHUB, LEVEL= range(12)


def start(update, context):
    update.message.reply_text('Side Projects is a community of young developers '
    'and professionals looking for programming projects to do while the country is '
    'under lockdown. \n\n'
    'If you are interested, press /fillup to send us about yourself')

    return FILL

def fill(update, context):
    id = update.message.chat_id
    text = update.message.text
    if text == '/fillup':
        update.message.reply_text('What is your name?')
        return NAME
    elif text == 'No' and db.get_items(id) != 'error':
        update.message.reply_text('Please, Fillup your details carefully!')
        update.message.reply_text('What is your name?')
        return NAME
    else:
        update.message.reply_text('Press /fillup to send us about yourself')
        


def name(update, context):
    id = update.message.chat_id
    text = update.message.text
    db.add_item('Name',text,id)
    update.message.reply_text('Which college are you from?')

    return COLLEGE

def college(update, context):
    reply_keyboard = [['Friends'],['Whatsapp Group'],['LinkedIn'],['Facebook']]
    id = update.message.chat_id
    text = update.message.text
    db.add_item('College',text,id)

    update.message.reply_text('How did you get to know about SideProjects?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return SIDEPROJECT


def side_project(update, context):
    ReplyKeyboardRemove()
    reply_keyboard = [['Done'],['Java'],['JavaScript'],['Python'],['CSS'],['C++'],['C'],['C#'],['HTML'],['HTML5'],['PHP'],['Objective C'],['SQL'],['R'],['Ruby']]
    id = update.message.chat_id
    text = update.message.text
    db.add_item('Source',text,id)
    update.message.reply_text('Which programming languages do you know?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard))

    return PLANGUAGE

dict = {}
def multiple_select(update, context):
    global dict
    id = update.message.chat_id
    text = update.message.text
    if id not in dict:
        dict[id]= []
    dict[id].append(text)

    return PLANGUAGE
    


def programming_language(update, context):
    global dict
    ReplyKeyboardRemove()
    reply_keyboard = [['Yes'],['No']]
    id = update.message.chat_id
    dict[id] = set(dict[id])
    lang_list = dict[id]
    text = (','.join(lang_list))
    db.add_item('Programming_language',text,id)
    del dict[id]

    update.message.reply_text('Do you know any frameworks? ',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    return CHECKFRAMEWORK

def list_framework(update, context):
    ReplyKeyboardRemove()
    update.message.reply_text('List them with comma(,) seperated.')

    return FRAMEWORK


def framework(update, context):
    ReplyKeyboardRemove()
    reply_keyboard = [['Yes'],['No']]
    id = update.message.chat_id
    text = update.message.text

    db.add_item('Framework',text,id)
    update.message.reply_text('Have you previously done any projects?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return PROJECTS

def projects(update, context):
    ReplyKeyboardRemove()
    reply_keyboard = [['Very Confident'],['Confident Enough'],['Still learning']]
    id = update.message.chat_id
    text = update.message.text

    db.add_item('Projects',text,id)
    update.message.reply_text('How confident are you about your programming skills?.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return PSKILLS

def programming_skills(update, context):
    ReplyKeyboardRemove()
    id = update.message.chat_id
    text = update.message.text

    db.add_item('Skill_level',text,id)
    update.message.reply_text('Please share your github repository for us to keep a track of your work if you have.\n\n.'
            'Otherwise, Press /No.')

    return GITHUB

def github_repository(update, context):
    reply_keyboard = [['Yes'],['No']]
    id = update.message.chat_id
    text = update.message.text
    if text == '/No':
        text = 'Not Provided'
    db.add_item('Github',text,id)
    ls = db.get_items(id)

    update.message.reply_text('Displayed below are your details,\n\n'
            f'Name : {ls[0]}\n'
            f'College : {ls[1]}\n'
            f'Source : {ls[2]}\n'
            f'Programming Language : {ls[3]}\n'
            f'Framework : {ls[4]}\n'
            f'Projects : {ls[5]}\n'
            f'Programming Skill Level : {ls[6]}\n'
            f'Github Id : {ls[7]}\n\n'
            'Please let us know if your previous details were correct. '
            'Press "Yes" to confirm or "No" to fill details again',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return LEVEL


def level(update, context):
    ReplyKeyboardRemove()
    id = update.message.chat_id
    ls = db.get_items(id)

    # calculate points
    points = 0
    no_pl = len(ls[3].split(','))
    no_fw = len(ls[4].split(','))
    if no_pl > 2:
        points += 3
    else:
        points += 1
    if ls[4].split(',')[0] != 'No':
        points += 2 + no_fw
    if ls[5] == 'Yes':
        points += 2
    if ls[6] == 'Very Confident':
        points += 3
    elif ls[6] == 'Confident Enough':
        points += 2
    elif ls[6] == 'Still Learning':
        points += 2

    # decide level
    if points >= 10:
        level = 'Level4'
    elif 8 <= points <10:
        level = 'Level3'
    elif 6 <= points <8:
        level = 'Level2'
    else:
        level = 'Level1'

    update.message.reply_text('Based on your skills and experience, we feel you should join the SideProjects levelling process at:'
    f' - {level}\n\n'
    'Please further communicate with SideProjects admin. Happy Coding!')

    
    context.bot.send_voice(chat_id=id, voice=open('{}.mp3'.format(level), 'rb'))
    

    return ConversationHandler.END



def cancel(update, context):
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main():
    
    updater = Updater("1041303018:AAGRqQDNwcmjTmKSUhmqLPIJ-qAcN1ko8MU", use_context=True)

    dp = updater.dispatcher
    

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            FILL: [MessageHandler(Filters.text, fill)],

            NAME: [MessageHandler(Filters.text, name)],

            COLLEGE: [MessageHandler(Filters.text, college)],

            SIDEPROJECT: [MessageHandler(Filters.regex('^(Friends|Whatsapp Group|LinkedIn|Facebook)$'), side_project)],

            PLANGUAGE: [MessageHandler(Filters.regex('^(Java|JavaScript|Python|CSS|C\+\+|C|C#|HTML|HTML5|PHP|Objective C|SQL|R|Ruby)$'), multiple_select),
                        MessageHandler(Filters.regex('Done$'),programming_language)
                        ],
            
            MULTIPLESELECT:[MessageHandler(Filters.regex('^(Java|JavaScript|Python|CSS|C\+\+|C|C#|HTML|HTML5|PHP|Objective C|SQL|R|Ruby)$'), multiple_select),
                        MessageHandler(Filters.regex('Done$'),programming_language)
                        ],

            CHECKFRAMEWORK: [MessageHandler(Filters.regex('^Yes$'),list_framework),
                       MessageHandler(Filters.regex('^No$'),framework),
                       ],

            FRAMEWORK: [MessageHandler(Filters.text, framework)],

            PROJECTS: [MessageHandler(Filters.regex('^(Yes|No)$'), projects)],

            PSKILLS: [MessageHandler(Filters.regex('^(Very Confident|Confident Enough|Still learning)$'), programming_skills)],

            GITHUB: [MessageHandler(Filters.text, github_repository)],

            LEVEL: [MessageHandler(Filters.regex('^Yes$'), level),
                    MessageHandler(Filters.regex('^No$'),fill),]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
