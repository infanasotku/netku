generate-go:
	protoc --go_out=services/xray \
	--go_opt=Mprotobuf/handler.proto=./handler \
	--go-grpc_out=services/xray \
	--go-grpc_opt=Mprotobuf/handler.proto=./handler \
	protobuf/handler.proto

generate-py:
	python -m grpc_tools.protoc -Ixray/handler/handler=protobuf/handler.proto \
	--python_out=services/assistant/ \
	--grpc_python_out=services/assistant/ \
	--pyi_out=services/assistant/ \
	protobuf/handler.proto