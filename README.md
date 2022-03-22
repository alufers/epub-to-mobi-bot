# epub-to-mobi-bot

A dead simple Telegram bot that converts epub files to mobi files (used on Amazon Kindle devices). 

It does nothing else, you just send the file and it replies with the converted file.

Under the hood it uses ebook-convert from Calibre.

## Dependencies

```
$ pip install python-telegram-bot
```

... or docker.

## Usage

Just run bot.py or the docker container. 
Pass the bot token using the `BOT_TOKEN` environment variable.

## License

AGPLv3
