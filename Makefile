xray-generate-go:
	protoc --go_out=services/xray/ \
	--go_opt=Mprotobuf/xray.proto=./gen \
	--go-grpc_out=services/xray/ \
	--go-grpc_opt=Mprotobuf/xray.proto=./gen \
	protobuf/xray.proto

xray-generate-py:
	python -m grpc_tools.protoc -Iinfra/grpc/gen=protobuf/ \
	--python_out=services/assistant/app \
	--grpc_python_out=services/assistant/app \
	--pyi_out=services/assistant/app \
	protobuf/xray.proto

booking-generate-go:
	protoc --go_out=services/booking/ \
	--go_opt=Mprotobuf/booking.proto=./gen \
	--go-grpc_out=services/booking/ \
	--go-grpc_opt=Mprotobuf/booking.proto=./gen \
	protobuf/booking.proto

booking-generate-py:
	python -m grpc_tools.protoc -Iinfra/grpc/gen=protobuf/ \
	--python_out=services/assistant/app \
	--grpc_python_out=services/assistant/app \
	--pyi_out=services/assistant/app \
	protobuf/booking.proto
