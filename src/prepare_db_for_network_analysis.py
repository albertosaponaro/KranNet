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
    
    # TODO - Test
    print('\nPreview DataFrame head... \n', df.head(), '\n')

    # Crate DB
    sql_utils.create_db('krannet')

    # Create tables
    create_tables()

    # TODO - Insert data into the tables
    for _, row in tqdm(df.iterrows()):
        
        # Insert meeting ito the meeting table
        query = 'INSERT INTO meeting_table (title, year) VALUES (%s, %s)'
        params = (row.title, row.year)
        sql_utils.transition(query, params, verbose=False)

        for speaker, intervention in row.speakers.items():
            
            # Insert speakers into the speakers table
            query = 'INSERT INTO speaker_table (meeting_id, speaker_name, interventions) VALUES (%s, %s, %s)'
            params = (row.id, speaker, intervention)
            sql_utils.transition(query, params, verbose=False)

    
    # Show head of the two tables
    meeting_df = sql_utils.fetch_table_data(table_name='meeting_table')
    speaker_df = sql_utils.fetch_table_data(table_name='meeting_table')
    print('\nPreview DataFrame head... \n', meeting_df.head(), '\n')
    print('\nPreview DataFrame head... \n', speaker_df.head(), '\n')

    # TODO - Check how many transitions failed and take a decisios on what to do about it

    # TODO - Save database or not?!

    # Drop DB
    sql_utils.drop_db('krannet')
    


if __name__ == '__main__':
    main()