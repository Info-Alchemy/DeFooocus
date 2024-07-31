#!/bin/bash

# Your dataset
DATASET="Bry:nkKKhfBfLqkh
SalesWorkStat01:tvGHJzmjKKdX
SalesWorkStat02:KDtbCfVGRdtf
SalesWorkStat03:cfzrkbpRmGvQ
SalesWorkStat04:WrCSdXXJQngs
ProdWorkStat01:JZHVNXSFQmQj
ProdWorkStat02:PwvnChhgmwtF
ProdWorkStat03:jRGGbqsVJMSz
AdminWorkStat01:TWfptDPNLHmn
FreeUser:RckxBSwQpwXN"

# Initialize the list of dictionary items
echo "["

# Loop through each line in the dataset
while IFS= read -r line; do
    # Split the line into user and password
    IFS=':' read -r user password <<< "$line"

    # Hash the password using sha256sum and extract the hash value
    hash=$(echo -n "$password" | sha256sum | awk '{print $1}')

    # Create a dictionary item and add it to the list
    echo "    {"
    echo "        \"user\": \"$user\","
    echo "        \"hash\": \"$hash\","
    echo "        \"role\": \"user\""
    echo "    },"
done <<< "$DATASET"

# Close the list of dictionary items
echo "]"