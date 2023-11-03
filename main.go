package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"strings"
	"time"

	"github.com/MicahParks/keyfunc/v2"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/golang-jwt/jwt/v5"
)

type MyEvent struct {
	Headers struct {
		UserClaims string `json:"x-amzn-oidc-data"`
	} `json:"headers"`
	Body string `json:"body"`
}

type Body struct {
	Name string `json:"name"`
}

type MyReply struct {
	StatusCode int    `json:"statusCode"`
	Body       string `json:"body"`
}

func HandleRequest(ctx context.Context, event *MyEvent) (*MyReply, error) {
	if event == nil {
		return nil, fmt.Errorf("received nil event")
	}

	err := validateJWT(event.Headers.UserClaims)
	if err != nil {
		return nil, err
	}

	var body Body
	json.Unmarshal([]byte(event.Body), &body)
	reply := MyReply{
		200,
		fmt.Sprintf("Hello %s!", body.Name),
	}
	return &reply, nil
}

func main() {
	lambda.Start(HandleRequest)

	// End the background refresh goroutine when it's no longer needed.
	jwks.EndBackground()
}

var jwks *keyfunc.JWKS

func init() {
	// Get the JWKS URL from your AWS region and userPoolId.
	// https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-verifying-a-jwt.html
	userPoolEndpoint := os.Getenv("USER_POOL_ENDPOINT")
	jwksURL := fmt.Sprintf("https://%s/.well-known/jwks.json", userPoolEndpoint)
	log.Printf("JWKS URL: %s", jwksURL)

	// Create the keyfunc options. Use an error handler that logs. Refresh the JWKS when a JWT signed by an unknown KID
	// is found or at the specified interval. Rate limit these refreshes. Timeout the initial JWKS refresh request after
	// 10 seconds. This timeout is also used to create the initial context.Context for keyfunc.Get.
	options := keyfunc.Options{
		RefreshErrorHandler: func(err error) {
			log.Printf("There was an error with the jwt.Keyfunc\nError: %s", err.Error())
		},
		RefreshInterval:   time.Hour,
		RefreshRateLimit:  time.Minute * 5,
		RefreshTimeout:    time.Second * 10,
		RefreshUnknownKID: true,
	}

	// Create the JWKS from the resource at the given URL.
	var err error
	jwks, err = keyfunc.Get(jwksURL, options)
	if err != nil {
		log.Fatalf("Failed to create JWKS from resource at the given URL.\nError: %s", err.Error())
	}
}

func validateJWT(jwtB64 string) error {
	log.Println(jwtB64)

	// Omit padding.
	jwtB64UrlSafe := strings.ReplaceAll(jwtB64, "=", "")

	// Parse the JWT.
	token, err := jwt.Parse(jwtB64UrlSafe, jwks.Keyfunc)
	if err != nil {
		return err
	}

	// Check if the token is valid.
	if !token.Valid {
		return fmt.Errorf("the JWT is invalid")
	}
	log.Println("The JWT is valid.")
	return nil
}
