generate-go:
	protoc --go_out=services/xray \
	--go_opt=Mprotobuf/handler.proto=./handler \
	--go-grpc_out=services/xray \
	--go-grpc_opt=Mprotobuf/handler.proto=./handler \
	protobuf/handler.proto