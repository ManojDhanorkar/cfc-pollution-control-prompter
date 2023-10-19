# Ensure that tenant, tenant admin users, tenant rule chain, device profile are already created.
# this script will provision devices and telemetry data
export THINGSBOARD_HOST_NAME=ec2-3-213-147-200.compute-1.amazonaws.com:8080
export PROVISION_KEY=vehicleskey
export PROVISION_SECRET=vehiclessecret
for c in "Mumbai:01" "Pune:12" "Nagpur:31"
do
    for f in {1101..1133}
    do
        # device provision
        echo "MH`echo $c|cut -f2 -d:`AA$f"
        curl -s -X POST --data "{"deviceName": "MH`echo $c|cut -f2 -d:`AA$f","provisionDeviceKey": "$PROVISION_KEY","provisionDeviceSecret": "$PROVISION_SECRET","credentialsType": "ACCESS_TOKEN", "token": "MH`echo $c|cut -f2 -d:`AA$f"}" http://$THINGSBOARD_HOST_NAME/api/v1/provision --header "Content-Type:application/json"
    done
done
