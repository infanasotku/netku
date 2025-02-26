xray-generate-go:
	protoc --go_out=services/xray/infra/grpc/ \
	--go_opt=Mproto/xray.proto=./gen \
	--go-grpc_out=services/xray/infra/grpc/ \
	--go-grpc_opt=Mproto/xray.proto=./gen \
	proto/xray.proto

xray-generate-py:
	python -m grpc_tools.protoc -Iapp/infra/grpc/gen=proto/ \
	--python_out=services/proxy \
	--grpc_python_out=services/proxy \
	--pyi_out=services/proxy \
	proto/xray.proto
