================
Usage of ircbot
================


This is a bot written for #dgplug summer training.
This also means it follows the way, we organize the sessions on
#dgplug channel on freenode.

config.yml
==========

This file contains the configuration of the tool.
An example is given below:

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

Masters are nicks who have power over the bot. They can execute various actions, as explained below.

Add a master
============

::

    add: newnick

Execute the above command in your channel.

Remove a master
===============

::

    rm: nick_to_remove

Removes a given nick, from the master list.

Start a session
===============

::

    #startclass

Give the above command in the *IRC channel* itself. Remember, that this does not work in PM.

End a class
===========

::

    #endclass

This ends the class. This also has to be provided in the channel itself.  
After ending the session the bot will try to upload the log.

You can also end in a different way, which doesn’t try to upload the log.

::

    #endclass nolog

Raise a hand to ask a question
==============================

::

    !

Typing only a ! puts you on the question queue.


Ask the next person to ask their question
=========================================

::

    next


Stop taking questions
=====================



::

    #questions off


Start taking questions again
============================

::

    #questions on


Can students ask questions now?
===============================


::

    #questions


This gets reset to true, everytime we start a new session.
==========================================================


