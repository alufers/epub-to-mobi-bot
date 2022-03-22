FROM archlinux:latest

RUN pacman -Sy --noconfirm calibre python-pip && pip install python-telegram-bot

COPY . /opt

ENTRYPOINT ["/bin/bash", "-c", "cd /opt && python3 /opt/bot.py"]
