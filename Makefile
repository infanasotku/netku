generate-xray-go:
	protoc --go_out=services/xray \
	--go_opt=Mprotobuf/xray.proto=./gen \
	--go-grpc_out=services/xray \
	--go-grpc_opt=Mprotobuf/xray.proto=./gen \
	protobuf/xray.proto

generate-xray-py:
	python -m grpc_tools.protoc -Ixray/gen/xray.proto=protobuf/xray.proto \
	--python_out=services/assistant/ \
	--grpc_python_out=services/assistant/ \
	--pyi_out=services/assistant/ \
	protobuf/xray.proto