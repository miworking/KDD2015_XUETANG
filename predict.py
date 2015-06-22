import pandas as pd
import pickle
import numpy as np
import os
from course_tree import *
from full_tree import *
from full_tree_node import *



df = pd.DataFrame(pd.read_csv('./test/enrollment_test.csv',header = 0))

prediction = None


for course_id in pd.unique(df.course_id):
    print "-------------------" + course_id + "---------------------------"
    # load full course tree to full_tree
    course_tree_path = './train/courseDump/' + course_id + ".txt"
    f = open(course_tree_path,'rb')
    full_tree = pickle.load(f)
    f.close()

    #  ------------------------- load all enrollment id to "matrix"  -------------------------
    full_matrix = pd.DataFrame(pd.read_csv('./test/enrollment_test.csv',header = 0))
    del full_matrix['username']
    del full_matrix['course_id']



    #  ------------------------- get all access log of this course tp "log" -------------------------
    course_path = './test/course/' + str(course_id) + '.csv'
    access = pd.DataFrame(pd.read_csv(course_path,header = 0))
    access_grouped= access.groupby('enrollment_id')
    access_count = access_grouped.count()
    del access_count['time']
    del access_count['event']
    del access_count['source']
    access_count = access_count.reset_index()


    # ------------------------- get total access counts -------------------------
    matrix = pd.merge(full_matrix,access_count,on="enrollment_id",how="right")
    matrix['access_counts'] = matrix.object
    del matrix['object']


    # ------------------------- get the first_access_in(days: relative to the module's start time)  -------------------------
    module_path = './train/fullTree/' + course_id + "_moduleIds.csv"
    modules = pd.DataFrame(pd.read_csv(module_path,header = 0))
    get_simple = lambda  x : x[: x.find('.')]
    modules['start'] = modules['start'].apply(get_simple)


    first_access = access.sort("time").groupby("enrollment_id", as_index=False).first()
    first_access_with_time = pd.merge(first_access,modules,left_on='object',right_on='module_id',how='left')
    del first_access_with_time['source']
    del first_access_with_time['event']
    del first_access_with_time['chapterId']
    del first_access_with_time['module_id']
    del first_access_with_time['category']
    del first_access_with_time['sequentialId']

    get_timeT = lambda  x : datetime.datetime.strptime(str(x),"%Y-%m-%dT%H:%M:%S")
    get_time = lambda  x : datetime.datetime.strptime(str(x),"%Y-%m-%d %H:%M:%S")
    first_access_with_time['time'] = first_access_with_time['time'].apply(get_timeT)
    first_access_with_time['start'] = first_access_with_time['start'].apply(get_time)
    first_access_with_time['from'] = first_access_with_time['time'] - first_access_with_time['start']
    get_float_sec = lambda x : x / np.timedelta64(1, 'D')
    first_access_with_time['from'] = first_access_with_time['from'].apply(get_float_sec)
    del first_access_with_time['start']
    del first_access_with_time['time']
    del first_access_with_time['object']
    matrix = pd.merge(matrix,first_access_with_time,on='enrollment_id',how='left')



    # ------------------------- get access timespan(in days: relative to first access start time) -------------------------

    first_access = access.sort("time").groupby("enrollment_id", as_index=False).first()
    del first_access['object']
    del first_access['event']
    del first_access['source']
    first_access.rename(columns={'time':'first_time'},inplace=True)

    last_access = access.sort("time").groupby("enrollment_id", as_index=False).last()
    del last_access['object']
    del last_access['event']
    del last_access['source']
    last_access.rename(columns={'time':'last_time'},inplace=True)
    timespan = pd.merge(first_access,last_access,on="enrollment_id",how="left")
    get_timeT = lambda  x : datetime.datetime.strptime(str(x),"%Y-%m-%dT%H:%M:%S")
    timespan['first_time'] = timespan['first_time'].apply(get_timeT)
    timespan['last_time'] = timespan['last_time'].apply(get_timeT)
    timespan['timespan'] = (timespan['last_time'] -  timespan['first_time']) / np.timedelta64(1, 'D')

    del timespan['first_time']
    del timespan['last_time']

    matrix = pd.merge(matrix,timespan,on='enrollment_id',how='left')





    # ------------------------- get video_access_counts -------------------------

    videos = modules[modules.category == 'video']
    videolist = videos.module_id.tolist()
    video_access = access[access['object'].isin(videolist)]
    video_grouped = video_access.groupby('enrollment_id')
    video_access_count = video_grouped.count()
    del video_access_count['time']
    del video_access_count['source']
    del video_access_count['object']

    video_access_count = video_access_count.reset_index()
    matrix = pd.merge(matrix,video_access_count,on='enrollment_id',how='left')
    matrix.fillna(0,inplace=True)
    matrix.rename(columns={'event':'video_access_counts'},inplace=True)


    # ------------------------- get video_start_in (days) -------------------------

    video_grouped_by2 = video_access.groupby(['enrollment_id','object'])
    video_first_access_time = video_grouped_by2.min()
    video_first_access_time = video_first_access_time.reset_index()

    video_start_in = pd.merge(video_first_access_time,videos,left_on='object',right_on='module_id',how='left')
    del video_start_in['category']
    del video_start_in['sequentialId']
    del video_start_in['chapterId']
    del video_start_in['module_id']
    del video_start_in['source']
    del video_start_in['event']
    get_timeT = lambda  x : datetime.datetime.strptime(str(x),"%Y-%m-%dT%H:%M:%S")
    get_time = lambda  x : datetime.datetime.strptime(str(x),"%Y-%m-%d %H:%M:%S")
    video_start_in['time'] = video_start_in['time'].apply(get_timeT)
    video_start_in['start'] = video_start_in['start'].apply(get_time)
    video_start_in['video_start_in'] = video_start_in['time'] - video_start_in['start']
    get_float_sec = lambda x : x / np.timedelta64(1, 'D')
    video_start_in['video_start_in'] = video_start_in['video_start_in'].apply(get_float_sec)
    del video_start_in['time']
    del video_start_in['start']
    video_start_in_days = video_start_in.groupby('enrollment_id').mean()
    video_start_in_days.reset_index(inplace=True)
    matrix = pd.merge(matrix,video_start_in_days,on='enrollment_id',how='left')
    matrix['video_start_in'].fillna(-1,inplace=True)



    # ------------------------- get problem access counts -------------------------

    problems = modules[modules.category == 'problem']
    problemlist = problems.module_id.tolist()
    problem_access = access[access['object'].isin(problemlist)]
    problem_grouped = problem_access.groupby('enrollment_id')
    problem_access_count = problem_grouped.count()
    del problem_access_count['time']
    del problem_access_count['source']
    del problem_access_count['object']

    problem_access_count = problem_access_count.reset_index()
    matrix = pd.merge(matrix,problem_access_count,on='enrollment_id',how='left')
    matrix.fillna(0,inplace=True)

    matrix.rename(columns={'event':'problem_access_counts'},inplace=True)




    # ------------------------- get problem_start_in (days) -------------------------
    problem_grouped_by2 = problem_access.groupby(['enrollment_id','object'])
    problem_first_access_time = problem_grouped_by2.min()
    problem_first_access_time = problem_first_access_time.reset_index()

    problem_start_in = pd.merge(problem_first_access_time,problems,left_on='object',right_on='module_id',how='left')
    del problem_start_in['category']
    del problem_start_in['sequentialId']
    del problem_start_in['chapterId']
    del problem_start_in['module_id']
    del problem_start_in['source']
    del problem_start_in['event']
    get_timeT = lambda  x : datetime.datetime.strptime(str(x),"%Y-%m-%dT%H:%M:%S")
    get_time = lambda  x : datetime.datetime.strptime(str(x),"%Y-%m-%d %H:%M:%S")
    problem_start_in['time'] = problem_start_in['time'].apply(get_timeT)
    problem_start_in['start'] = problem_start_in['start'].apply(get_time)
    problem_start_in['problem_start_in'] = problem_start_in['time'] - problem_start_in['start']
    get_float_sec = lambda x : x / np.timedelta64(1, 'D')
    problem_start_in['problem_start_in'] = problem_start_in['problem_start_in'].apply(get_float_sec)
    del problem_start_in['time']
    del problem_start_in['start']
    problem_start_in_days = problem_start_in.groupby('enrollment_id').mean()
    problem_start_in_days.reset_index(inplace=True)
    matrix = pd.merge(matrix,problem_start_in_days,on='enrollment_id',how='left')
    matrix['problem_start_in'].fillna(-1,inplace=True)





    # ---------------------------- write matrix to csv ----------------------------

    path = './test/features/' + course_id + '.csv'
    matrix.to_csv(path,index = False,index_label= False,header = 1)



    # ---------------------------- predict ----------------------------
    from sklearn.cross_validation import cross_val_score
    from sklearn.datasets import make_blobs
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.ensemble import ExtraTreesClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import GradientBoostingClassifier


    test_features = matrix
    train_featuer_path = './train/features/' + course_id + '.csv'
    train_features = df = pd.DataFrame(pd.read_csv(train_featuer_path,header = 0))

    y = train_features.result
    del train_features['result']
    del train_features['enrollment_id']
    X = train_features




    clf = RandomForestClassifier(max_depth=None,min_samples_split=1,random_state=0,n_estimators=500)
    # clf = GradientBoostingClassifier(loss='deviance', learning_rate=0.1,
    #                          n_estimators=5, subsample=0.3,
    #                          min_samples_split=2,
    #                          min_samples_leaf=1,
    #                          max_depth=3,
    #                          random_state=None,
    #                          max_features=None,
    #                          verbose=2)
    clf.fit(X,y)


    enrollment_id_list = test_features['enrollment_id']
    del test_features['enrollment_id']
    # result = clf.predict(test_features)
    result = clf.predict_proba(test_features)
    test_features['result'] = result[:,1].tolist()

    test_features['enrollment_id'] = enrollment_id_list

    if prediction is None:
        prediction = test_features
    else:
        prediction = prediction.append(test_features)


predict_path = './test/predict/all.csv'
prediction.to_csv(predict_path,index = False,index_label= False,header = 1)

final_result = prediction[['enrollment_id','result']]
final_result = final_result.sort(['enrollment_id'], ascending=True)
final_result_path = './test/predict_result.csv'
final_result.to_csv(final_result_path,index = False,index_label= False,header = 1)

