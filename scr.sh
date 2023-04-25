#!/bin/bash
nodes=$(kubectl get nodes -o 'jsonpath={.items[*].metadata.name}')

# Set space as the delimiter
IFS=' '

#Read the split words into an array based on space delimiter
read -a nodes1 <<< "$nodes"

length=${#nodes1[@]}

node_number_to_delete=$(( $RANDOM % $length ))

node_to_delete=${nodes1[$node_number_to_delete]}

kubectl delete node $node_to_delete
