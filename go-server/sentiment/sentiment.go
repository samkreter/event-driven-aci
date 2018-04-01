package sentiment

import (
	"github.com/cdipaolo/sentiment"
)

type Sentiment struct {
	Model sentiment.Models
}

func NewSentiment() (*Sentiment, error) {
	model, err := sentiment.Restore()
	if err != nil {
		return &Sentiment{}, err
	}

	return &Sentiment{Model: model}, nil
}

func (s Sentiment) GetAnalysis(msg string) *sentiment.Analysis {
	return s.Model.SentimentAnalysis(msg, sentiment.English)
}

func (s Sentiment) GetScore(msg string) float64 {
	analysis := s.Model.SentimentAnalysis(msg, sentiment.English)

	var total int

	if analysis.Score == 1 {
		total++
	}

	for _, word := range analysis.Words {
		if word.Score == 1 {
			total++
		}
	}

	return float64(total) / float64(len(analysis.Words))
}
