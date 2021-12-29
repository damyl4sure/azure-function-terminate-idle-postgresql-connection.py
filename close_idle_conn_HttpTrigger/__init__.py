import logging
import os
import azure.functions as func
import psycopg2


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        
        # Update connection string information
        host = "<your_db_URL/IP address>"
        dbname = "postgres"
        user = "<user_db_user"
        #password = "secret"
        password = os.environ.get("secret")
        sslmode = "require"

        # Construct connection string
        conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
        conn = psycopg2.connect(conn_string)
        print("Connection established to the DB")

        cursor = conn.cursor()


        # no_idle_conn = cursor.execute("select count(*) from pg_stat_activity where (state = 'idle')")
        # print(no_idle_conn)


        #postgreSQL_select_Query = "select * from pg_stat_activity where (state = 'idle')"

        postgreSQL_select_Query1 = "SELECT count(*) FROM pg_stat_activity WHERE (state = 'idle')"

        cursor.execute(postgreSQL_select_Query1)
        print("Selecting idle_connection from pg_stat_activity table using cursor.fetchall")
        idle_conn1 = cursor.fetchall()

        #Getting the amount of idle_connection from the DB
        for i in idle_conn1:
            i = (i[0])
            print("Amount of idle_connection is:", i)
            #print("no_of_idle_conn = ", row[0], "\n")
            
            if i >= 200:
                print("Idle Connection is too high!")
                postgreSQL_run_Query1 = "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state in ('idle');"
                cursor.execute(postgreSQL_run_Query1)
                print("Idle Connections Terminated")
            else:
                print("Idle Connection is considerate")
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=400  
        )
