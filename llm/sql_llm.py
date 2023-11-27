import re
from .llm_handler import LLMHandler
from genai.schemas import GenerateParams

class SqlLLmHandler(LLMHandler):
    CO_IDLING_PETROL = 0.3
    HC_PETROL = 200
    CO_RPM_PETROL = 0.2
    RPM_PETROL = 200

    def __init__(self):
        parmaeters = GenerateParams(decoding_method="greedy", stop_sequences=[";"], max_new_tokens=1024)
        super().__init__(model_type='google/flan-ul2', parameters=parmaeters)
    
    def get_prompt(self, query):
        return (f"""
                Pay attention to use date('now') functions to get the current date, if the question involves "today".
                Use the following format:

                Question: Question here
                SQLResult: SQL query to run;

                Only use the following tables:

                CREATE TABLE device (
                id UUID NOT NULL, 
                created_time BIGINT NOT NULL, 
                additional_info VARCHAR, 
                customer_id UUID, 
                device_profile_id UUID NOT NULL, 
                device_data JSONB, 
                type VARCHAR(255), 
                name VARCHAR(255), 
                label VARCHAR(255), 
                tenant_id UUID, 
                firmware_id UUID, 
                software_id UUID, 
                external_id UUID, 
                CONSTRAINT device_pkey PRIMARY KEY (id), 
                CONSTRAINT fk_device_profile FOREIGN KEY(device_profile_id) REFERENCES device_profile (id), 
                CONSTRAINT fk_firmware_device FOREIGN KEY(firmware_id) REFERENCES ota_package (id), 
                CONSTRAINT fk_software_device FOREIGN KEY(software_id) REFERENCES ota_package (id), 
                CONSTRAINT device_external_id_unq_key UNIQUE (tenant_id, external_id), 
                CONSTRAINT device_name_unq_key UNIQUE (tenant_id, name)
                )

                /*
                3 rows from device table:
                id created_time additional_info customer_id device_profile_id device_data type name label tenant_id firmware_id software_id external_id
                f664a610-5a0d-11ee-a84c-35d042965ec0 1695472650993 None f5fdf500-5a0d-11ee-a84c-35d042965ec0 f54f3e70-5a0d-11ee-a84c-35d042965ec0 {{'configuration': {{'type': 'DEFAULT'}}, 'transportConfiguration': {{'type': 'DEFAULT'}} }} default Test Device A1 None f5424620-5a0d-11ee-a84c-35d042965ec0 None None None
                f67ebdc0-5a0d-11ee-a84c-35d042965ec0 1695472651164 None f5fdf500-5a0d-11ee-a84c-35d042965ec0 f54f3e70-5a0d-11ee-a84c-35d042965ec0 {{'configuration': {{'type': 'DEFAULT'}}, 'transportConfiguration': {{'type': 'DEFAULT'}} }} default Test Device A2 None f5424620-5a0d-11ee-a84c-35d042965ec0 None None None
                f683ede0-5a0d-11ee-a84c-35d042965ec0 1695472651198 None f5fdf500-5a0d-11ee-a84c-35d042965ec0 f54f3e70-5a0d-11ee-a84c-35d042965ec0 {{'configuration': {{'type': 'DEFAULT'}}, 'transportConfiguration': {{'type': 'DEFAULT'}} }} default Test Device A3 None f5424620-5a0d-11ee-a84c-35d042965ec0 None None None
                */


                CREATE TABLE ts_kv_latest (
                entity_id UUID NOT NULL, 
                key INTEGER NOT NULL, 
                ts BIGINT NOT NULL, 
                bool_v BOOLEAN, 
                str_v VARCHAR(10000000), 
                long_v BIGINT, 
                dbl_v DOUBLE PRECISION, 
                json_v JSON, 
                CONSTRAINT ts_kv_pkey PRIMARY KEY (entity_id, key, ts)
                )

                /*
                3 rows from ts_kv_latest table:
                entity_id key ts bool_v str_v s dbl_v json_v
                391a7020-5a0e-11ee-0000-000000000000 16 1695968230726 False None None None None
                391a7020-5a0e-11ee-0000-000000000000 17 1695968230726 None None 2 None None
                391a7020-5a0e-11ee-0000-000000000000 18 1695968230726 None None 35 None None
                */


                CREATE TABLE ts_kv_dictionary (
                key VARCHAR(255) NOT NULL, 
                key_id INTEGER DEFAULT nextval('ts_kv_dictionary_key_id_seq'::regclass) NOT NULL, 
                CONSTRAINT ts_key_id_pkey PRIMARY KEY (key), 
                CONSTRAINT ts_kv_dictionary_key_id_key UNIQUE (key_id)
                )

                /*
                3 rows from ts_kv_dictionary table:
                key key_id
                transportApiState 1
                dbApiState 2
                ruleEngineApiState 3
                */

                Guidelines:
                - device.type should always be "PollutionSensors"
                - Use device.name to filter on region
                - A "puc" is considered to be "failed" when
                CO_Idling > {self.CO_IDLING_PETROL} OR HC > {self.HC_PETROL} OR CO_RPM > {self.CO_RPM_PETROL}
                The OR of all above conditions results in "puc failure". These metrics can be found in ts_kv_dictionary.key. You will only use this condition when puc failures are asked. You will use the above values unless specified otherwise in the question
                - Consider that Pune device names start with "MH"
                - Do not use tenant id
                - You will have to perform a join on all these 3 tables to get a result

                Examples:
                Question: List all devices with their metrics
                SQLResult: SELECT d.id, d.name, tsk.long_v, tsk.ts, tsm.key FROM device d JOIN ts_kv_latest tsk ON d.id = tsk.entity_id JOIN ts_kv_dictionary tsm ON tsk.key = tsm.key_id;

                Question: How many failing devices are there as of today ?
                SQLResult: SELECT COUNT(DISTINCT d.id) FROM device d JOIN ts_kv_latest tsk ON d.id = tsk.entity_id JOIN ts_kv_dictionary tsm ON tsk.key = tsm.key_id WHERE  ( tsm.key = 'CO_Idling'  AND tsk.long_v > {self.CO_IDLING_PETROL} ) OR ( tsm.key = 'HC'  AND tsk.long_v > {self.HC_PETROL} ) OR ( tsm.key = 'CO_RPM'  AND tsk.long_v > {self.CO_RPM_PETROL} );

                Question: List the names of all the failing devices
                SQLResult: SELECT DISTINCT d.id, d.name FROM device d JOIN ts_kv_latest tsk ON d.id = tsk.entity_id JOIN ts_kv_dictionary tsm ON tsk.key = tsm.key_id WHERE  ( tsm.key = 'CO_Idling'  AND tsk.long_v > {self.CO_IDLING_PETROL} ) OR ( tsm.key = 'HC'  AND tsk.long_v > {self.HC_PETROL} ) OR ( tsm.key = 'CO_RPM'  AND tsk.long_v > {self.CO_RPM_PETROL} );

                Question: {query}
                SQLResult:""")
    
    def parse_result(self, query):
        parsed_query = re.findall(r'SELECT\s+.*$', query)
        if parsed_query[0].endswith(";"):
            return parsed_query[0]
        return parsed_query[0] + ";"