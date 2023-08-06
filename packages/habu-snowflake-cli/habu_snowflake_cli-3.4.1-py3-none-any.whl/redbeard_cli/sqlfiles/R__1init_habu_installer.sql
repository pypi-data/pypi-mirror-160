BEGIN

CREATE OR REPLACE SECURE FUNCTION HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.HABU_ORCHESTRATOR(region varchar)
    returns STRING
    language JAVASCRIPT
as $$
    var mapOfRegionToOrchestrator = new Map([
                  ['AZURE_EASTUS2', 'zf49269.east-us-2.azure'],
                  ['GCP_US_CENTRAL1', 'sh82453.us-central1.gcp'],
                  ['AWS_US_EAST_1', 'ptb97855.us-east-1'],
                  ['AWS_US_EAST_2', 'uo60321.us-east-2.aws'],
                  ['AWS_US_WEST_2', 'JYA07515'],
    ]);
return mapOfRegionToOrchestrator.get(REGION);
$$;


CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.INSTALLER()
RETURNS STRING
LANGUAGE JAVASCRIPT
EXECUTE AS OWNER
AS $$
snowflake.execute({ sqlText: `CREATE SCHEMA IF NOT EXISTS HABU_SCHEMA` });
snowflake.execute({ sqlText: `CREATE SCHEMA IF NOT EXISTS CLEAN_ROOM` });
snowflake.execute({ sqlText: `CREATE OR REPLACE PROCEDURE
	HABU_SCHEMA.INIT_FRAMEWORK(ORGANIZATON_ID VARCHAR)
	returns string
	language javascript
	execute as owner as
	\$\$

        sqlcmd = "SELECT HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.HABU_ORCHESTRATOR(current_region())";
        rset = snowflake.execute({ sqlText: sqlcmd });
        rset.next()
        var HABU_ACCOUNT_ID = rset.getColumnValue(1);


        sqlcmd = "CALL HABU_CLEAN_ROOM_COMMON.HABU_SCHEMA.INIT_FRAMEWORK('" + ORGANIZATON_ID + "', '" + HABU_ACCOUNT_ID + "')";
        rset = snowflake.execute({ sqlText: sqlcmd });
        rset.next()

		return rset.getColumnValue(1);
	\$\$`
});


snowflake.execute({ sqlText: `CREATE OR REPLACE PROCEDURE
	HABU_SCHEMA.INIT_FRAMEWORK(ORGANIZATON_ID VARCHAR, HABU_ACCOUNT_ID VARCHAR)
	returns string
	language javascript
	execute as owner as
	\$\$

        sqlcmd = "SELECT current_account()";
        rset = snowflake.execute({ sqlText: sqlcmd });
        rset.next()
        var CUSTOMER_ACCOUNT_ID = rset.getColumnValue(1);

        var SHARE_RESTRICTIONS = "false";

        sqlcmd = "CALL HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.INIT_HABU_SHARES('" + ORGANIZATON_ID + "', '" + HABU_ACCOUNT_ID + "', '" + CUSTOMER_ACCOUNT_ID + "')";
        var rset = snowflake.execute({ sqlText: sqlcmd });
        rset.next()
        if (rset.getColumnValue(1) != 0) {
            return "Could not find the necessary Habu shares. Please contact your Habu representative";
        }
        sqlcmd = "CALL HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.SETUP_DATA_CONNECTION_OBJECTS('" + HABU_ACCOUNT_ID + "', '" + CUSTOMER_ACCOUNT_ID + "', '" + SHARE_RESTRICTIONS + "')";
        snowflake.execute({ sqlText: sqlcmd });
        sqlcmd = "CALL HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.SETUP_CLEANROOM_COMMON('" + HABU_ACCOUNT_ID + "', '" + CUSTOMER_ACCOUNT_ID + "', '" + SHARE_RESTRICTIONS + "')";
        snowflake.execute({ sqlText: sqlcmd });
        sqlcmd = "CALL HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.SETUP_STREAM_TASKS('" + ORGANIZATON_ID + "', '" + HABU_ACCOUNT_ID + "', '" + CUSTOMER_ACCOUNT_ID + "')";
        snowflake.execute({ sqlText: sqlcmd });
		return "Habu framework init successful";
	\$\$`
});


return "Habu installer done";
$$;


end;


