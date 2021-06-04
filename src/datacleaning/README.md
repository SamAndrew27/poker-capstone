This file contains all the work I did to extract information from DriveHud backup data. The ‘create_df’ file is the most important. Using the functions imported from ‘columns_from_hand_history’, ‘time_columns’, ‘dependent_columns’ and ‘betting_columns_CALL_LAST’, the create_df file creates the columns. The ‘load_df’ function loads data from the SQL backup and splits the HandHistory column. To use this yourself, simply change the ‘filepath’ variable to the filepath of your DataFrame. The ‘implement_column_creation’ function creates and fills the columns. In its current form, cash game hands are deleted. To change this set the ‘prior_actions’ variable equal to False. This will lead to a number of columns not being created, but they were not columns I ended up using in my own modeling. The ‘holdout_training’ file splits the created DataFrame into a training and a holdout set, but will require some modification to be used by others since it reads this data from a csv file created with ‘create_df’. To use it yourself, use ‘create_df’ on your data and save to a csv file, then read that csv file into a pandas DataFrame and then use that DataFrame as the argument for the ‘holdout_training_classification’ function.