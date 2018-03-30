az container create \
    -g aciherodemo \
    -n web-server \
    --image pskreter/web-server:prod \
    --ip-address public \
    --ports 80 \
    --azure-file-volume-account-name $STORAGE_NAME \
    --azure-file-volume-account-key $STORAGE_KEY \
    --azure-file-volume-share-name $SHARE_NAME \
    --azure-file-volume-mount-path /app/config/