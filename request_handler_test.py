import unittest
import request_handler

class TestHandleAuth(unittest.TestCase):

    def test_without_token(self):
        self.assertIsNone(request_handler.handle_auth({}))

    def test_with_good_accesstoken(self):
        self.assertEqual(request_handler.handle_auth({
            "x-amzn-oidc-accesstoken": "eyJraWQiOiIwU3pKejlUVzYrUW16cVRtVUFhbWdRMElSQ3BUbjZwTWQ2a0FQR09JN1pvPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJhMjI5M2I0OC05NzQxLTQ1ZDYtOTE3NC03MjE3Yzk2MTMxY2IiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV96Qm1jOHl0Y0ciLCJ2ZXJzaW9uIjoyLCJjbGllbnRfaWQiOiIxdDJpNmFkYnYwczJiZmswcWY0dXAyNWkxaiIsIm9yaWdpbl9qdGkiOiIzNWI0ZDEzOC01OTJkLTQ5ZmUtYmFjNy1lZjZiYjU2OWEzOTQiLCJldmVudF9pZCI6IjJkMTI3MGE0LTI5OTEtNDU2Yi1iYjMwLTFmYzRkMDc3NDAyYyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoib3BlbmlkIGVtYWlsIiwiYXV0aF90aW1lIjoxNjk4OTc1MDk5LCJleHAiOjE2OTkwNjk4NTEsImlhdCI6MTY5OTA2NjI1MSwianRpIjoiYWM4MTM5ZGQtNzhhNS00NTk5LTg2M2ItYWIyNDU1MWRhY2I0IiwidXNlcm5hbWUiOiJhMjI5M2I0OC05NzQxLTQ1ZDYtOTE3NC03MjE3Yzk2MTMxY2IifQ.mPK5mEbWYgANvoC6mcmBtZftY6-D0i8Pblcfq0CHobuhwWXkud9qytT4D7febna1bopguJ4BbGep7BEpBCX8p_cEqeIrT-YTf52H0mzNKiGHVWjk_aPUTprib2QSFx3wuoRK8apZkE16ejPk87xO5aajb6CoTHPiWMF4siAOnkrMeZdRV0byufgnianzDxTrYtIsreJo7HBVyHxSQ1s4TNbphAkdaOrqmJb4TiW6PutXv-iuyzRqy-aMr79XGZy6509P9heE65TfrY_KirfcohrtjQNU6Eo9fMatszy7L5wLSiVA631vsAoWyKYrqSbyhcckVpkbiWC8SvEpjacZGg"
        }), "diego.sogari@gmail.com")

    def test_with_good_userclaims(self):
        self.assertEqual(request_handler.handle_auth({
            "x-amzn-oidc-data": "eyJ0eXAiOiJKV1QiLCJraWQiOiJmZWQ1NzhkMi0wZWI5LTRhZTQtYTI3Yy05YjQyMzA3NWUxMzIiLCJhbGciOiJFUzI1NiIsImlzcyI6Imh0dHBzOi8vY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb20vdXMtZWFzdC0xX3pCbWM4eXRjRyIsImNsaWVudCI6IjF0Mmk2YWRidjBzMmJmazBxZjR1cDI1aTFqIiwic2lnbmVyIjoiYXJuOmF3czplbGFzdGljbG9hZGJhbGFuY2luZzp1cy1lYXN0LTE6NTc0NTYzMjg0NDk1OmxvYWRiYWxhbmNlci9hcHAvZGVmYXVsdC80NjY5NGFlYTU3NjZhYTQyIiwiZXhwIjoxNjk5MDY2MzcyfQ==.eyJzdWIiOiJhMjI5M2I0OC05NzQxLTQ1ZDYtOTE3NC03MjE3Yzk2MTMxY2IiLCJlbWFpbF92ZXJpZmllZCI6InRydWUiLCJlbWFpbCI6ImRpZWdvLnNvZ2FyaUBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImEyMjkzYjQ4LTk3NDEtNDVkNi05MTc0LTcyMTdjOTYxMzFjYiIsImV4cCI6MTY5OTA2NjM3MiwiaXNzIjoiaHR0cHM6Ly9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbS91cy1lYXN0LTFfekJtYzh5dGNHIn0=.B08QVKsDCML9SpdQWxywCXTYAEc1JWZTFknz_rXyXYCcglT74lS32eBhIvfhoJ2IPxng0QiY1NruDDPfmGUrIQ=="
        }), "diego.sogari@gmail.com")

    def test_with_bad_accesstoken(self):
        with self.assertRaises(Exception):
            request_handler.handle_auth({"x-amzn-oidc-accesstoken":""})
            
    def test_with_bad_userclaims(self):
        with self.assertRaises(Exception):
            request_handler.handle_auth({"x-amzn-oidc-data":""})

if __name__ == '__main__':
    unittest.main()