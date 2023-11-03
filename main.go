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

func CognitoHandler(ctx context.Context) {
	lc, _ := lambdacontext.FromContext(ctx)
	log.Print(lc.Identity.CognitoIdentityID)
}

func HandleRequest(ctx context.Context, event *MyEvent) (*string, error) {
	CognitoHandler(ctx)
	if event == nil {
		return nil, fmt.Errorf("received nil event")
	}
	message := fmt.Sprintf("Hello %s!", event.Name)
	return &message, nil
}

func main() {
	lambda.Start(HandleRequest)
}
