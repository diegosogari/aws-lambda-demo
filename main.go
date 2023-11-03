package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-lambda-go/lambda"
)

type MyEvent struct {
	Headers struct {
		UserClaims string `json:"x-amzn-oidc-data"`
	} `json:"headers"`
	Body struct {
		Name string `json:"name"`
	} `json:"body"`
}

type MyReply struct {
	StatusCode int    `json:"statusCode"`
	Body       string `json:"body"`
}

func HandleRequest(ctx context.Context, event *MyEvent) (*MyReply, error) {
	if event == nil {
		return nil, fmt.Errorf("received nil event")
	}
	log.Print(event.Headers.UserClaims)
	reply := MyReply{
		200,
		fmt.Sprintf("Hello %s!", event.Body.Name),
	}
	return &reply, nil
}

func main() {
	lambda.Start(HandleRequest)
}
