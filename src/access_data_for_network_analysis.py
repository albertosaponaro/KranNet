import env, utils, sql_utils
import pandas as pd
from tqdm import tqdm


def restore_krannet_db_from_backup(backup_path, verbose=True):
    
    # Restore database and tables
    sql_utils.create_db('krannet')
    env.create_krannet_tables()
    
    # Load tables as DataFrames
    meeting_df = pd.read_csv(f'{backup_path}/krannet_meeting_table.csv', sep='\t')
    speaker_df = pd.read_csv(f'{backup_path}/krannet_speaker_table.csv', sep='\t')

    # Sanity Check
    if verbose: print('\nPreview DataFrame head... \n', meeting_df.head(), '\n', 'Number of meetings:', len(meeting_df))
    if verbose: print('\nPreview DataFrame head... \n', speaker_df.head(), '\n', 'Number of meetings:', len(speaker_df))

    # Restore 'meeting_table'
    for _, row in tqdm(meeting_df.iterrows()):
        query = """INSERT INTO meeting_table (meeting_id, title, year) VALUES (%s, %s, %s)"""
        params = (row.meeting_id, row.title, row.year)
        sql_utils.transition(query, params, verbose=False)

    # Sanity Check - 'meeting_table'
    meeting_df = sql_utils.fetch_table_data('meeting_table')
    if verbose: print('\nPreview DataFrame head... \n', meeting_df.head(), '\n', 'Number of meetings:', len(meeting_df))

    # Restore 'speaker_table'
    for _, row in tqdm(speaker_df.iterrows()):
        query = """INSERT INTO speaker_table (speaker_id, meeting_id, speaker_name, interventions) VALUES (%s, %s, %s, %s)"""
        params = (row.speaker_id, row.meeting_id, row.speaker_name, row.interventions)
        sql_utils.transition(query, params, verbose=False)

    # Sanity Check - 'speaker_table' 
    speaker_df = sql_utils.fetch_table_data('speaker_table')
    if verbose: print('\nPreview DataFrame head... \n', speaker_df.head(), '\n', 'Number of meetings:', len(speaker_df))

    # Optimize space
    del meeting_df
    del speaker_df

def main():
    cache_dir, output_file = utils.parse_arguments()
    restore_krannet_db_from_backup(cache_dir)
    

    query = """
    SELECT DISTINCT
        M.year AS year,
        S.*
    FROM 
        meeting_table M
    JOIN 
        speaker_table S ON M.meeting_id = S.meeting_id
    WHERE
        M.year IN ('1861', '1862');
    """

    df = sql_utils.fetch_data(query)
    print(df.head(), '\nLength: ', len(df))

    df.to_json(output_file)
    
    # Drop DB
    sql_utils.drop_db('krannet')


if __name__ == '__main__':
    main()