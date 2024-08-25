generate-go:
	protoc --go_out=services/xray \
	--go_opt=Mprotobuf/handler.proto=genproto/handler \
	--go-grpc_out=services/xray \
	--go-grpc_opt=Mprotobuf/handler.proto=genproto/handler \
	protobuf/handler.proto