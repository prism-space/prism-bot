# prism-bot
A special-purpose Discord bot with Django-based web management

## Development Setup
Hopefully I've made this as simple as possible. Let me know on Discord (BlergRush#8601) if something went wrong with your install.

Note: Currently the easy setup supports only MacOS and Debian-based Linux systems. It _probably_ works in WSL (Windows Subsystem for Linux) but I've not yet tested it. Consider Windows to be "hard mode". 😅

```shell
# Install system-level pre-requisites
make install

# Install python packages
make setup

# Start the webserver and visit localhost:9999 in your web browser to check!
make run
```

Once you've confirmed the Django server runs, you can go ahead and run the database migrations (`python manage.py migrate`) and create an admin user (`python manage.py createsuperuser`).