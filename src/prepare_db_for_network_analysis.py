import utils
import sql_utils
import pandas as pd
from tqdm import tqdm 

def create_tables():
    # SQL queries to create the tables
    create_meeting_table = """
    CREATE TABLE IF NOT EXISTS meeting_table (
        meeting_id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        year INT NOT NULL
    );
    """

    create_speaker_table = """
    CREATE TABLE IF NOT EXISTS speaker_table (
        speaker_id SERIAL PRIMARY KEY,
        meeting_id INT NOT NULL,
        speaker_name VARCHAR(50) NOT NULL,
        interventions SMALLINT NOT NULL
    );
    """

    # Execute the transition function to create the tables
    sql_utils.transition(create_meeting_table)
    sql_utils.transition(create_speaker_table)
    print('Tables created successfully.')


def main():
    # Drop DB
    sql_utils.drop_db('krannet')

    input_file, output_file = utils.parse_arguments()

    # Load meeting infos from cache
    df = pd.read_json(input_file)
    print('\nPreview DataFrame head... \n', df.head(), '\n', 'Number of meetings:', len(df), '\n')


    # Crate DB
    sql_utils.create_db('krannet')

    # Create tables
    create_tables()

    numb_of_speakers = 0 # sanity check

    # Insert data into DB tables
    for _, row in tqdm(df.iterrows()):
        
        # Insert meeting ito the meeting table
        query = 'INSERT INTO meeting_table (title, year) VALUES (%s, %s)'
        params = (row.title, row.year)
        sql_utils.transition(query, params, verbose=False)

        # TODO - if the transition fails we shouls skeep inserting the meeting --> too much work maybe just delete restriction of 100 CHARS!!!

        for speaker, intervention in row.speakers.items():
            
            # Insert speakers into the speakers table
            query = 'INSERT INTO speaker_table (meeting_id, speaker_name, interventions) VALUES (%s, %s, %s)'
            params = (row.id, speaker, intervention)
            sql_utils.transition(query, params, verbose=False)

            numb_of_speakers += 1 # sanity check

    
    # Show head of the two tables
    meeting_df = sql_utils.fetch_table_data(table_name='meeting_table')
    speaker_df = sql_utils.fetch_table_data(table_name='speaker_table')
    print('\nPreview DataFrame head... \n', meeting_df.head(), '\n', 'Number of meetings:', len(meeting_df), 'of', len(df), '\n') # 564 of 667
    print('\nPreview DataFrame head... \n', speaker_df.head(), '\n', 'Number of meetings:', len(speaker_df), 'of', numb_of_speakers, '\n')

    # TODO - Save database or not?! --> Save but how (ISSUES with Postgress and VENV)

    # Drop DB
    sql_utils.drop_db('krannet')
    


if __name__ == '__main__':
    main()