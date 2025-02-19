proto-generate:
	protoc --go_out=. \
	--go_opt=Mxray.proto=./gen \
	--go-grpc_out=. \
	--go-grpc_opt=Mxray.proto=./gen \
	xray.proto
