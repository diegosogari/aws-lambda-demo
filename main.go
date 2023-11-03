package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-lambda-go/lambdacontext"
)

type MyEvent struct {
	Name string `json:"name"`
}

type MyReply struct {
	StatusCode int    `json:"statusCode"`
	Body       string `json:"body"`
}

func CognitoHandler(ctx context.Context) {
	lc, _ := lambdacontext.FromContext(ctx)
	log.Print(lc.Identity.CognitoIdentityID)
}

func HandleRequest(ctx context.Context, event *MyEvent) (*MyReply, error) {
	CognitoHandler(ctx)
	if event == nil {
		return nil, fmt.Errorf("received nil event")
	}
	reply := MyReply{
		200,
		fmt.Sprintf("Hello %s!", event.Name),
	}
	return &reply, nil
}

func main() {
	lambda.Start(HandleRequest)
}
