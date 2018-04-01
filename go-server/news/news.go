package news

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"time"
)

const (
	BaseURI = "https://newsapi.org/v2/everything?q=%s&sortBy=publishedAt&apiKey=%s"
)

type NewsResponse struct {
	Status       string    `json:"status"`
	TotalResults int       `json:"totalResults"`
	Articles     []Article `json:"articles"`
}

type Article struct {
	Source struct {
		Name string `json:"name"`
	} `json:"source"`
	Author      string    `json:"author"`
	Title       string    `json:"title"`
	Description string    `json:"description"`
	URL         string    `json:"url"`
	URLToImage  string    `json:"urlToImage"`
	PublishedAt time.Time `json:"publishedAt"`
}

type NewsReader struct {
	apiKey string
}

func NewNewsReader(apiKey string) *NewsReader {
	return &NewsReader{apiKey: apiKey}
}

func (nr NewsReader) GetNews(keyword string) (NewsResponse, error) {
	uri := fmt.Sprintf(BaseURI, keyword, nr.apiKey)

	response, err := http.Get(uri)
	if err != nil {
		return NewsResponse{}, err
	}

	defer response.Body.Close()

	contents, err := ioutil.ReadAll(response.Body)
	if err != nil {
		return NewsResponse{}, err
	}

	var newsResponse NewsResponse
	err = json.Unmarshal(contents, &newsResponse)
	if err != nil {
		return NewsResponse{}, err
	}

	return newsResponse, nil
}
