#!bin/bash
#Script to make new microBlockchain transaction
#arguments:
#	<str> sender
#	<str> recipient
#	<int> amount

sender=$1
recipient=$2
amount=$3

curl -X POST -H "Content-Type: application/json" -d '{
	"sender": "$1",
	"recipient": "$2",
	"amount": "$3"
}' "http://0.0.0.0:5000/transactions/new"
