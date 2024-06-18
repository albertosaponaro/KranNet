import env, utils, sql_utils
import pandas as pd
from tqdm import tqdm
import pgdumplib


def main():
    input_file, output_file = utils.parse_arguments()

    # Load meeting infos from cache
    df = pd.read_json(input_file)
    print('\nPreview DataFrame head... \n', df.head(), '\n', 'Number of meetings:', len(df), '\n')


    # Crate DB
    sql_utils.create_db('krannet')

    # Create tables
    env.create_krannet_tables()

    numb_of_speakers = 0 # sanity check

    # Insert data into DB tables
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

            numb_of_speakers += 1 # sanity check

    
    # Show head of the two tables
    meeting_df = sql_utils.fetch_table_data(table_name='meeting_table')
    speaker_df = sql_utils.fetch_table_data(table_name='speaker_table')
    print('\nPreview DataFrame head... \n', meeting_df.head(), '\n', 'Number of meetings:', len(meeting_df), 'of', len(df), '\n')
    print('\nPreview DataFrame head... \n', speaker_df.head(), '\n', 'Number of meetings:', len(speaker_df), 'of', numb_of_speakers, '\n')

    # Save tables as CSV
    print('\nBackup tables as CSV files')
    meeting_df.to_csv(f'{output_file}_meeting_table.csv', sep='\t')
    speaker_df.to_csv(f'{output_file}_speaker_table.csv', sep='\t')

    # Drop DB
    sql_utils.drop_db('krannet')
    


if __name__ == '__main__':
    main()