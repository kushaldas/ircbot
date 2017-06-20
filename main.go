package main

import (
	"crypto/tls"
	"fmt"
	"os"
	"strings"
	"time"

	"github.com/spf13/viper"
	"github.com/thoj/go-ircevent"
)

const serverssl = "irc.freenode.net:7000"

var masters = map[string]bool{}
var questions []string
var queue = map[string]bool{}

func main() {
	var f *os.File
	var classStatus bool
	canAsk := true

	// The following is for configuration using viper
	viper.SetConfigName("config")
	viper.AddConfigPath("./")
	err := viper.ReadInConfig()

	if err != nil {
		fmt.Println("No configuration file loaded - using defaults")
	}
	viper.SetDefault("nick", "yournick")
	viper.SetDefault("fullname", "Our nice bot")
	viper.SetDefault("channel", "#yooooooops")
	viper.SetDefault("masters", []string{"kushal"})

	channel := viper.GetString("channel")
	ms := viper.GetStringSlice("masters")
	// Now let us populate the masters map
	for _, v := range ms {
		masters[v] = true
	}

	irccon := irc.IRC(viper.GetString("nick"), viper.GetString("fullname"))
	defer irccon.Quit()
	irccon.VerboseCallbackHandler = true
	irccon.Debug = false
	irccon.UseTLS = true
	irccon.TLSConfig = &tls.Config{InsecureSkipVerify: true}
	irccon.AddCallback("001", func(e *irc.Event) { irccon.Join(channel) })

	irccon.AddCallback("366", func(e *irc.Event) {
		irccon.Privmsg(channel, "Joined in.\n")
	})
	irccon.AddCallback("PRIVMSG", func(e *irc.Event) {
		channame := e.Arguments[0]
		nick := e.Nick
		message := e.Message()
		fmt.Println("Received:", message)
		if strings.HasPrefix(channame, "#") {
			// We have a message in a channel

			if strings.HasPrefix(message, "#hello") {
				// Let us reply back
				irccon.Privmsgf(channame, "%s: hello\n", nick)
			} else if strings.HasPrefix(message, "add: ") {
				// We will add someone into the masters list
				// If this command is given by a master
				newmaster := strings.Split(message, " ")[1]
				if masters[nick] {
					masters[newmaster] = true
					irccon.Privmsgf(channame, "%s is now a master.\n", newmaster)
				}
			} else if strings.HasPrefix(message, "rm: ") && masters[nick] {
				oldmaster := strings.Split(message, " ")[1]
				delete(masters, oldmaster)
				irccon.Privmsgf(channame, "%s is now removed from masters.\n", oldmaster)

			} else if strings.HasPrefix(message, "#questions off") && masters[nick] {
				canAsk = false
			} else if strings.HasPrefix(message, "#questions on") && masters[nick] {
				canAsk = true
			} else if message == "!" {
				if !classStatus {
					msg := fmt.Sprintf("%s no class is going on. Feel free to ask any question.\n", nick)
					irccon.Privmsgf(channame, msg)
				} else if !queue[nick] && canAsk {
					questions = append(questions, nick)
					queue[nick] = true
				}
			} else if message == "next" && masters[nick] {
				l := len(questions)
				if l > 0 {
					cnick := questions[0]
					questions = questions[1:]
					irccon.Privmsgf(channame, fmt.Sprintf("%s ask your question.", cnick))
					if len(questions) > 0 {
						irccon.Privmsgf(channame, fmt.Sprintf("%s you are next, get ready with your question.\n", questions[0]))
					}
					delete(queue, cnick)
				} else {
					irccon.Privmsgf(channame, "No one is in the queue.\n")
				}
			} else if message == "#startclass" && !classStatus && masters[nick] {
				// We will start a class now
				irccon.Privmsgf(channame, "----BEGIN CLASS----\n")
				classStatus = true
				t := time.Now().UTC()
				fname := t.Format("Logs-2006-01-02-15-04.txt")
				f, _ = os.Create(fname)
				f.WriteString("----BEGIN CLASS----\n")
			} else if message == "#endclass" && classStatus && masters[nick] {
				irccon.Privmsgf(channame, "----END CLASS----\n")
				classStatus = false
				f.WriteString("----END CLASS----\n")
				f.Close()
			}
			// Now log the messages
			tstamp := time.Now().UTC()
			f.WriteString(fmt.Sprintf("[%s] <%s> %s\n", tstamp.Format("15:04"), nick, message))

		} else if masters[nick] {
			if message == "showqueue" {
				irccon.Privmsg(nick, strings.Join(questions, ","))
			} else if message == "masters" {
				localname := []string{}
				for k, _ := range masters {
					localname = append(localname, k)
				}
				irccon.Privmsg(nick, strings.Join(localname, ","))
			}
		}
	})

	err = irccon.Connect(serverssl)
	if err != nil {
		fmt.Println(err)
		irccon.Quit()
		return
	}

	irccon.Loop()

}
