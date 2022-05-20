# IRCBOT

This is the new bot which we use in #dgplug channel for summer training.

## Development

- go get github.com/thoj/go-ircevent
- go get github.com/spf13/viper

## Config file

The name of the file is **config.toml**, and it is in the current directory. The logs will be in the same directory.


```
nick = "ircbot42"
realname = "ircbot42"
fullname = "ircbot42"
channel = "#libera"
password = ""
trainers = ["nick1", "nick2"]
```

You will also need **SASL EXTERNAL** access based on **certfp** for the
nickname. Follow [the guide](https://libera.chat/guides/certfp) from Libera for
the steps.
