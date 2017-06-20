================
Usage of ircbot
================


This is a bot written for #dgplug summer training. This also means it follows the way we organize the sessions on
#dgplug channel on freenode.

config.yml
===========

This file contains the configuration of the tool. Example is given below:

::

    ---
    nick: "botnic,"
    fullname: "fullname"
    channel: "#yourchannel"
    destination: "Path for autoupload the logs"
    masters:
     - kushal
     - sayan
     - praveenkumar
     - chandankumar
     - rtnpro
     - mbuf

Masters are nicks which has power over the bot. They can do various actions as explained below.

Add a master
============

::

    add: newnick

Execute the above command in your channel.

Removes a master
================

::

    rm: nick_to_remove

Removes a given nick from master list.

Start a session
===============

::

    #startclass

Give the above command in the *IRC channel* itself. Remember that this does not work in PM.

End a class
============

::

    #endclass

This ends the class. This also has to be provided in the channel itself. After ending the session
the bot will try to upload the log. So, you can end in a different way, which will not try to upload the log.

::

    #endclass nolog

Raise a hand to ask a question
=============================

::

    !

Only typing a ! puts you on the question queue.


Ask the next person to ask the question
=======================================

::

    next

Stop taking anymore questions
============================

::

    #questions off


Start taking questions again
===========================

::

    #questions on


Can students ask questions now?
================================


::

    #questions

This gets reset to true everytime we star a new session.
