# H-funding

H-funding is a crowfunding platform written for an academic project.

This is a port for the [weppy framework](http://weppy.org) of the original Rails project (https://github.com/michaelgenesini/h-funding).

UI and logo are copyrighted by Michael Genesini.

## How to use it?

Clone this repository and in your terminal do:

    pip install -r requirements.txt
    python run.py

To launch the cron helper that opens and closes campaigns do:

    weppy --app hfunding cron

## Project notes

Since this is an academic project, it doesn't include payments flows and related technology.
