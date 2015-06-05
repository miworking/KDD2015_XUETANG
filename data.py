import pandas as pd
import numpy as np

df_entroll_train = pd.read_csv('./train/enrollment_train.csv',header = 0)
df_true_train = pd.read_csv('./train/truth_train.csv',header = 0)
df_log_train = pd.read_csv('./train/log_train.csv',header = 0)

df_sampleSubmission = pd.read_csv('./sampleSubmission.csv',header = 0)

df_object = pd.read_csv('./object.csv',header = 0)

df_enrollment_test = pd.read_csv('./test/enrollment_test.csv',header = 0)



