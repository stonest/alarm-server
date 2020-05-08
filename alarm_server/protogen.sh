SOURCE=$1 # source of the proto files
TARGET=$2 # where to generate the python files

TMPDIR=$(mktemp -d)
mkdir -p $TMPDIR/$TARGET
cp $SOURCE/* $TMPDIR/$TARGET

python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I $TMPDIR $TMPDIR/$TARGET/*.proto

rm -rf $TMPDIR