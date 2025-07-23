import pandas as pd
from rich.jupyter import display

meeting_note_csv_path = '../audio/싼기타_비싼기타_csv'
df_rttm = pd.read_csv(meeting_note_csv_path, sep='|')

display(df_rttm)