package main

import (
	"fmt"
	"log"

	"github.com/samkreter/event-driven-aci/go-server/news"
	"github.com/samkreter/event-driven-aci/go-server/sentiment"
	"github.com/spf13/viper"
)

func init() {
	log.SetFlags(log.LstdFlags | log.Lshortfile)

	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath("config")
	viper.ReadInConfig()

}

func main() {
	newsReader := news.NewNewsReader(viper.GetString("news-api-key"))

	senti, err := sentiment.NewSentiment()
	if err != nil {
		log.Fatal(err)
	}

	newsResponse, err := newsReader.GetNews("bitcoin")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Total Results: ", newsResponse.TotalResults)

	for _, article := range newsResponse.Articles {
		fmt.Println(senti.GetScore(article.Description), senti.GetAnalysis(article.Description).Score)
	}
}
