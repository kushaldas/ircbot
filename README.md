# IRCBOT

This is the new bot which we use in #dgplug channel for summer training.

## Development

- go get github.com/thoj/go-ircevent
- go get github.com/spf13/viper

## Config file

The name of the file is **config.yml**, and it is in the current directory. The logs will be in the same directory.

```
---
nick: "awesomenick"
fullname: "Your full name"
channel: "#irchannel"
masters:
 - "nick1"
 - "nick2"
 - "nick3"
```
