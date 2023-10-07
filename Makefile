.PHONY: deploy-functions
deploy-functions:
	firebase deploy --only functions

.PHONY: start-local-emulator
start-local-emulator:
	firebase emulators:start

.PHONY: request-to-local-emulator
request-to-local-emulator:
	curl "http://127.0.0.1:5001/cheers-connect-db-sandbox/us-central1/stations"