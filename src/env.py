import sql_utils

def create_krannet_tables():
    # SQL queries to create the tables
    create_meeting_table = """
    CREATE TABLE IF NOT EXISTS meeting_table (
        meeting_id SERIAL PRIMARY KEY,
        title VARCHAR(150) NOT NULL,
        year INT NOT NULL
    );
    """

    create_speaker_table = """
    CREATE TABLE IF NOT EXISTS speaker_table (
        speaker_id SERIAL PRIMARY KEY,
        meeting_id INT NOT NULL,
        speaker_name VARCHAR(100) NOT NULL,
        interventions SMALLINT NOT NULL
    );
    """

    # Execute the transition function to create the tables
    sql_utils.transition(create_meeting_table)
    sql_utils.transition(create_speaker_table)
    print('Tables created successfully.')