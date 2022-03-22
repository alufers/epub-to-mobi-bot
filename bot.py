
#     A telegram bot that converts epub files to mobi files
#     Copyright (C) 2022 alufers

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.


from telegram import Update
from telegram.ext import Updater, MessageHandler, CallbackContext
import random
import subprocess
import time
import os

def hello(update: Update, context: CallbackContext) -> None:
    # reply with error if update does not contain a file
    if not update.message.document:
        update.message.reply_text("Please send an epub file")
        return
    update.message.reply_text("Converting epub to mobi...")
    
    print ("Converting " + update.message.document.file_name)
    # generate a random string for the filename
    filename = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(10))
    # save the file to /tmp with a random name
    file_path = update.message.document.get_file().download(
        "/tmp/{}.epub".format(filename)
    )
    # convert the epub to mobi and send a message for each line of stderr and stdout
    
    last_msg_sent = time.time()

    line_buffer = ""
    
    for line in subprocess.check_output(
        ['ebook-convert', "/tmp/{}.epub".format(filename), "/tmp/{}.mobi".format(filename)],
        stderr=subprocess.STDOUT
    ).decode().splitlines():
        print(line)
        if time.time() - last_msg_sent > 0.5:
            update.message.reply_text(line_buffer + "\n" + line)
            last_msg_sent = time.time()
            line_buffer = ""
        line_buffer += line
    if not line_buffer == "":
        update.message.reply_text(line_buffer)
    # subprocess.run(["ebook-convert", "/tmp/{}.epub".format(filename), "/tmp/{}.mobi".format(filename)])

    # send the mobi file to the user with the original filename
    update.message.reply_document(
        document=open("/tmp/{}.mobi".format(filename), "rb"),
        filename="{}.mobi".format(update.message.document.file_name)
    )


# read the token from enviroment variable named BOT_TOKEN
updater = Updater(os.environ['BOT_TOKEN'])

updater.dispatcher.add_handler(MessageHandler(None, hello))



updater.start_polling()
updater.idle()
