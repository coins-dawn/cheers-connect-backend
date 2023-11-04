.PHONY: deploy-functions
deploy-functions:
	firebase deploy --only functions

.PHONY: start-local-emulator
start-local-emulator:
	firebase emulators:start

.PHONY: sample-req-recommend-store
sample-req-recommend-store:
	curl "http://127.0.0.1:5001/cheers-connect-db-sandbox/us-central1/execute/recommend-store?station_id=00005767&search_radius=500"

.PHONY: sample-req-search-route
sample-req-search-route:
	curl "http://127.0.0.1:5001/cheers-connect-db-sandbox/us-central1/execute/search-route?org_station_id=00006668&dst_station_id=00009451"