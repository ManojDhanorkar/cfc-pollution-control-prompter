# Ensure that tenant, tenant admin users, tenant rule chain, device profile are already created.
# this script will provision devices and telemetry data
export THINGSBOARD_HOST_NAME=ec2-3-213-147-200.compute-1.amazonaws.com:8080
export PROVISION_KEY=vehicleskey
export PROVISION_SECRET=vehiclessecret
BASEDATE=1693526430000
for c in "Mumbai:01"
do
    for f in {1110..1120}
    do
        # device provision
        echo "MH`echo $c|cut -f2 -d:`AA$f"
        BASEDATE=1693526430000
        # device telemetry
        for k in {1..1}
        do
            curl -s -X POST --data "{"ts":$((BASEDATE+2592000)),"values":{"CO_Idling":`seq 0.3 .001 0.4 | shuf | head -n1`,"CO_RPM":`seq 0.2 .001 0.3 | shuf | head -n1`,"HC": `shuf -i 201-220 -n 1`,"RPM":`shuf -i 2400-2600 -n 1`,"City":"`echo $c|cut -f1 -d:`", "Fuel_Type": "Petrol", "Date_of_Manufacturing": `shuf -i 2010-2021 -n 1`-`shuf -i 01-12 -n 1`-`shuf -i 01-25 -n 1`}}" http://$THINGSBOARD_HOST_NAME/api/v1/MH`echo $c|cut -f2 -d:`AA$f/telemetry --header "Content-Type:application/json"
            BASEDATE=$((BASEDATE+1296000000))
        done
    done
done

for c in "Mumbai:01"
do
    for f in {1101..1109}
    do
        # device provision
        echo "MH`echo $c|cut -f2 -d:`AA$f"
        BASEDATE=1693526430000
        # device telemetry
        for k in {1..1}
        do
            curl -s -X POST --data "{"ts":$((BASEDATE+2592000)),"values":{"CO_Idling":`seq 0 .001 0.3 | shuf | head -n1`,"CO_RPM":`seq 0 .001 0.2 | shuf | head -n1`,"HC": `shuf -i 170-199 -n 1`,"RPM":`shuf -i 2400-2600 -n 1`,"City":"`echo $c|cut -f1 -d:`", "Fuel_Type": "Petrol", "Date_of_Manufacturing": `shuf -i 2010-2021 -n 1`-`shuf -i 01-12 -n 1`-`shuf -i 01-25 -n 1`}}" http://$THINGSBOARD_HOST_NAME/api/v1/MH`echo $c|cut -f2 -d:`AA$f/telemetry --header "Content-Type:application/json"
            BASEDATE=$((BASEDATE+1296000000))
        done
    done
done

for c in "Mumbai:01"
do
    for f in {1121..1133}
    do
        # device provision
        echo "MH`echo $c|cut -f2 -d:`AA$f"
        BASEDATE=1693526430000
        # device telemetry
        for k in {1..1}
        do
            curl -s -X POST --data "{"ts":$((BASEDATE+2592000)),"values":{"CO_Idling":`seq 0 .001 0.3 | shuf | head -n1`,"CO_RPM":`seq 0 .001 0.2 | shuf | head -n1`,"HC": `shuf -i 170-199 -n 1`,"RPM":`shuf -i 2400-2600 -n 1`,"City":"`echo $c|cut -f1 -d:`", "Fuel_Type": "Petrol", "Date_of_Manufacturing": `shuf -i 2010-2021 -n 1`-`shuf -i 01-12 -n 1`-`shuf -i 01-25 -n 1`}}" http://$THINGSBOARD_HOST_NAME/api/v1/MH`echo $c|cut -f2 -d:`AA$f/telemetry --header "Content-Type:application/json"
            BASEDATE=$((BASEDATE+1296000000))
        done
    done
done

for c in "Pune:12"
do
    for f in {1105..1113}
    do
        # device provision
        echo "MH`echo $c|cut -f2 -d:`AA$f"
        BASEDATE=1693526430000
        # device telemetry
        for k in {1..1}
        do
            curl -s -X POST --data "{"ts":$((BASEDATE+2592000)),"values":{"CO_Idling":`seq 0.3 .001 0.4 | shuf | head -n1`,"CO_RPM":`seq 0.2 .001 0.3 | shuf | head -n1`,"HC": `shuf -i 201-220 -n 1`,"RPM":`shuf -i 2400-2600 -n 1`,"City":"`echo $c|cut -f1 -d:`", "Fuel_Type": "Petrol", "Date_of_Manufacturing": `shuf -i 2010-2021 -n 1`-`shuf -i 01-12 -n 1`-`shuf -i 01-25 -n 1`}}" http://$THINGSBOARD_HOST_NAME/api/v1/MH`echo $c|cut -f2 -d:`AA$f/telemetry --header "Content-Type:application/json"
            BASEDATE=$((BASEDATE+1296000000))
        done
    done
done

for c in "Pune:12"
do
    for f in {1101..1104}
    do
        # device provision
        echo "MH`echo $c|cut -f2 -d:`AA$f"
        BASEDATE=1693526430000
        # device telemetry
        for k in {1..1}
        do
            curl -s -X POST --data "{"ts":$((BASEDATE+2592000)),"values":{"CO_Idling":`seq 0 .001 0.3 | shuf | head -n1`,"CO_RPM":`seq 0 .001 0.2 | shuf | head -n1`,"HC": `shuf -i 170-199 -n 1`,"RPM":`shuf -i 2400-2600 -n 1`,"City":"`echo $c|cut -f1 -d:`", "Fuel_Type": "Petrol", "Date_of_Manufacturing": `shuf -i 2010-2021 -n 1`-`shuf -i 01-12 -n 1`-`shuf -i 01-25 -n 1`}}" http://$THINGSBOARD_HOST_NAME/api/v1/MH`echo $c|cut -f2 -d:`AA$f/telemetry --header "Content-Type:application/json"
            BASEDATE=$((BASEDATE+1296000000))
        done
    done
done

for c in "Pune:12"
do
    for f in {1114..1133}
    do
        # device provision
        echo "MH`echo $c|cut -f2 -d:`AA$f"
        BASEDATE=1693526430000
        # device telemetry
        for k in {1..1}
        do
            curl -s -X POST --data "{"ts":$((BASEDATE+2592000)),"values":{"CO_Idling":`seq 0 .001 0.3 | shuf | head -n1`,"CO_RPM":`seq 0 .001 0.2 | shuf | head -n1`,"HC": `shuf -i 170-199 -n 1`,"RPM":`shuf -i 2400-2600 -n 1`,"City":"`echo $c|cut -f1 -d:`", "Fuel_Type": "Petrol", "Date_of_Manufacturing": `shuf -i 2010-2021 -n 1`-`shuf -i 01-12 -n 1`-`shuf -i 01-25 -n 1`}}" http://$THINGSBOARD_HOST_NAME/api/v1/MH`echo $c|cut -f2 -d:`AA$f/telemetry --header "Content-Type:application/json"
            BASEDATE=$((BASEDATE+1296000000))
        done
    done
done

for c in "Nagpur:31"
do
    for f in {1112..1127}
    do
        # device provision
        echo "MH`echo $c|cut -f2 -d:`AA$f"
        BASEDATE=1693526430000
        # device telemetry
        for k in {1..1}
        do
            curl -s -X POST --data "{"ts":$((BASEDATE+2592000)),"values":{"CO_Idling":`seq 0.3 .001 0.4 | shuf | head -n1`,"CO_RPM":`seq 0.2 .001 0.3 | shuf | head -n1`,"HC": `shuf -i 201-220 -n 1`,"RPM":`shuf -i 2400-2600 -n 1`,"City":"`echo $c|cut -f1 -d:`", "Fuel_Type": "Petrol", "Date_of_Manufacturing": `shuf -i 2010-2021 -n 1`-`shuf -i 01-12 -n 1`-`shuf -i 01-25 -n 1`}}" http://$THINGSBOARD_HOST_NAME/api/v1/MH`echo $c|cut -f2 -d:`AA$f/telemetry --header "Content-Type:application/json"
            BASEDATE=$((BASEDATE+1296000000))
        done
    done
done

for c in "Nagpur:31"
do
    for f in {1101..1111}
    do
        # device provision
        echo "MH`echo $c|cut -f2 -d:`AA$f"
        BASEDATE=1693526430000
        # device telemetry
        for k in {1..1}
        do
            curl -s -X POST --data "{"ts":$((BASEDATE+2592000)),"values":{"CO_Idling":`seq 0 .001 0.3 | shuf | head -n1`,"CO_RPM":`seq 0 .001 0.2 | shuf | head -n1`,"HC": `shuf -i 170-199 -n 1`,"RPM":`shuf -i 2400-2600 -n 1`,"City":"`echo $c|cut -f1 -d:`", "Fuel_Type": "Petrol", "Date_of_Manufacturing": `shuf -i 2010-2021 -n 1`-`shuf -i 01-12 -n 1`-`shuf -i 01-25 -n 1`}}" http://$THINGSBOARD_HOST_NAME/api/v1/MH`echo $c|cut -f2 -d:`AA$f/telemetry --header "Content-Type:application/json"
            BASEDATE=$((BASEDATE+1296000000))
        done
    done
done

for c in "Nagpur:31"
do
    for f in {1128..1133}
    do
        # device provision
        echo "MH`echo $c|cut -f2 -d:`AA$f"
        BASEDATE=1693526430000
        # device telemetry
        for k in {1..1}
        do
            curl -s -X POST --data "{"ts":$((BASEDATE+2592000)),"values":{"CO_Idling":`seq 0 .001 0.2 | shuf | head -n1`,"CO_RPM":`seq 0 .001 0.2 | shuf | head -n1`,"HC": `shuf -i 170-199 -n 1`,"RPM":`shuf -i 2400-2600 -n 1`,"City":"`echo $c|cut -f1 -d:`", "Fuel_Type": "Petrol", "Date_of_Manufacturing": `shuf -i 2010-2021 -n 1`-`shuf -i 01-12 -n 1`-`shuf -i 01-25 -n 1`}}" http://$THINGSBOARD_HOST_NAME/api/v1/MH`echo $c|cut -f2 -d:`AA$f/telemetry --header "Content-Type:application/json"
            BASEDATE=$((BASEDATE+1296000000))
        done
    done
done
