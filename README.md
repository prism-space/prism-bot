# prism-bot
A special-purpose Discord bot with Django-based web management

## Development Setup
Hopefully I've made this as simple as possible. Let me know on Discord (BlergRush#8601) if something went wrong with your install.

Note: Currently the easy setup supports only MacOS and Debian-based Linux systems. It _probably_ works in WSL (Windows Subsystem for Linux) but I've not yet tested it. Consider Windows to be "hard mode". 😅

```shell
# Create a .env file and paste in the required API keys and tokens for your test application and test server
cp .env.example .env

# Install system-level pre-requisites
make setup

# Install python packages
make install

# Start the webserver and visit localhost:9999 in your web browser to check!
make run-web

# Create the database and run the migrations
python manage.py sqlcreate | psql
python manage.py migrate

# Start the bot in a separate terminal instance from the webserver
make run-bot
```

