.PHONY: deploy-functions
deploy-functions:
	firebase deploy --only functions

.PHONY: start-local-emulator
start-local-emulator:
	firebase emulators:start

.PHONY: sample-req-recommend-store
sample-req-recommend-store:
	curl "http://127.0.0.1:5001/cheers-connect-db-sandbox/us-central1/execute/recommend-store?station_id=00007820-00009451-00000813&nearest_station_distance_limit=1000&budget=5000&min_comment_num=10&max_transit_time_minute=40&min_rate=3.3&genre_code=12-43-94"

.PHONY: sample-req-search-route
sample-req-search-route:
	curl "http://127.0.0.1:5001/cheers-connect-db-sandbox/us-central1/execute/search-route?org_station_id=00006599&dst_station_id=00007820"
