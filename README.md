# Boxbot

Hello, I am boxbot, your friendly e-ink display bot.

## Service config
1. Copy `botbox.service` to `~/.config/systemd/user`
2. Run the following:
```bash
sudo loginctl enable-linger pie
systemctl --user daemon-reload
systemctl --user enable boxbot
```
