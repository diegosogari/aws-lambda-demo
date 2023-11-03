package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/MicahParks/keyfunc/v2"
	"github.com/golang-jwt/jwt/v5"
)

var jwks *keyfunc.JWKS
var publicKeys = map[string]string{}

func init() {
	// Get the JWKS URL from your AWS region and userPoolId.
	// https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-verifying-a-jwt.html
	jwksURL := fmt.Sprintf("https://%s/.well-known/jwks.json", os.Getenv("USER_POOL_ENDPOINT"))
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

func getPublicKey(token *jwt.Token) (interface{}, error) {
	kid := token.Header["kid"].(string)
	publicKey, ok := publicKeys[kid]
	if !ok {
		// Get the public key from ALB the endpoint.
		// https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-authenticate-users.html
		keyUrl := fmt.Sprintf("https://public-keys.auth.elb.%s.amazonaws.com/%s", os.Getenv("AWS_REGION"), kid)
		log.Printf("Key URL: %s", keyUrl)

		resp, err := http.Get(keyUrl)
		if err != nil {
			return nil, err
		}
		if resp.StatusCode != http.StatusOK {
			return nil, fmt.Errorf(resp.Status)
		}
		defer resp.Body.Close()

		body, err := io.ReadAll(resp.Body)
		if err != nil {
			return nil, fmt.Errorf("could not read response body")
		}
		publicKey = string(body)
		publicKeys[kid] = publicKey
	}
	return []byte(publicKey), nil
}

func validateToken(jwtB64 string, keyFunc jwt.Keyfunc) error {
	// Omit padding.
	jwtB64UrlSafe := strings.ReplaceAll(jwtB64, "=", "")
	log.Printf("JWT: %s", jwtB64UrlSafe)

	token, err := jwt.Parse(jwtB64UrlSafe, keyFunc)
	if err != nil {
		return err
	}
	if !token.Valid {
		return fmt.Errorf("the JWT is invalid")
	}
	return nil
}
