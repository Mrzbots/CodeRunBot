package main

import (
 "log"

 tb "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func main() {
 bot, err := tb.NewBotAPI("YOUR_BOT_TOKEN")
 if err != nil {
  log.Panic(err)
 }

 bot.Debug = true

 log.Printf("Authorized on account %s", bot.Self.UserName)

 u := tb.NewUpdate(0)
 u.Timeout = 60

 updates, err := bot.GetUpdatesChan(u)

 for update := range updates {
  if update.Message != nil {
   handleMessage(bot, update.Message)
  }
 }
}

func handleMessage(bot *tb.BotAPI, message *tb.Message) {
 if message.Text == "/start" {
  startCommand(bot, message)
 }
}

func startCommand(bot *tb.BotAPI, message *tb.Message) {
 btn := tb.NewInlineKeyboardButton("Visit mrz_bots channel", "https://t.me/mrz_bots")
 kb := tb.NewInlineKeyboardMarkup(btn)
 msg := tb.NewMessage(message.Chat.ID, "Welcome to our bot!")
 msg.ReplyMarkup = kb
 bot.Send(msg)
}
