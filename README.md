# Boxbot

Hello, I am boxbot, your friendly e-ink display bot.

## Config Requirements
Enable SPI interface in the raspberry pi config
```bash
sudo raspi-config
```
Interface Options -> SPI

## Install requirements
1. Install system dependencies
   ```bash
      sudo apt install liblgpio-dev
    ```
2. Create a virtual environment. From this directory, run
  ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
  ```

## Service config
1. Copy `botbox.service` to `~/.config/systemd/user`
2. Run the following:
  ```bash
    sudo loginctl enable-linger pie
    systemctl --user daemon-reload
    systemctl --user enable boxbot
  ```

To see the logs and current status of the service, run
```bash
systemctl --user status boxbot
```

## Connecting to Grist
To connect to grist, you'll need to set the `GRIST_API_KEY` and `GRIST_DOC_ID`.

Copy the `.env.example` to `.env` and set the values
