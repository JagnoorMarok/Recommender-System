import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn_extra.cluster import KMedoids
from gower import gower_matrix

# Load CSV Files
dispersion_df = pd.read_csv('dispersion.csv')
marks_df = pd.read_csv('marks.csv')
courses_df = pd.read_csv('courses.csv')
response_df = pd.read_csv('response.csv')

# Rename for consistency
marks_df.rename(columns={'roll no': 'Roll No.(8 Digits)'}, inplace=True)
courses_df.rename(columns={'roll no': 'Roll No.(8 Digits)'}, inplace=True)

# Merge marks and courses with response data based on Roll No
response_df = response_df.merge(marks_df, how='left', on='Roll No.(8 Digits)')
response_df = response_df.merge(courses_df, how='left', on='Roll No.(8 Digits)')

# Merge degree of dispersion for specific question
dispersion_df.set_index('Question Title', inplace=True)
response_df = response_df.join(
    dispersion_df[['Degree of Dispersion (Std Dev)']],
    on='Interest in Subjects: How interested are you in exploring new subjects?',
    rsuffix='_dispersion'
)

# Encode categorical responses
encoder = LabelEncoder()
categorical_columns = [
    'Interest in Subjects: How interested are you in exploring new subjects?',
    'Skill Development: How important is skill development in your choice of electives?',
    'Preferred Learning Method: Which learning method do you prefer?',
    'Time Commitment: How many hours per week can you dedicate to a subject?',
    'Exam Preparation: How do you usually prepare for exams?',
    'Mock Test Participation: How often do you take mock tests?',
    'Psychological State Before Tests: How do you feel before taking an exam?',
    'Time Management: How do you plan to manage the workload?',
    'Career Goals: How important is alignment with career goals in choosing a Subject?',
    'Learning Motivation: What motivates you to choose a Subject?',
    'Peer Influence: Would you consider a subject because your peers are choosing it?',
    'Feedback from Seniors: Have you received feedback from seniors about your course in general?',
    'Resource Availability: Do you have access to necessary resources for Subjects?',
    'Future Studies: Are you planning further studies in any area?'
]

for col in categorical_columns:
    if col in response_df.columns:
        response_df[col] = encoder.fit_transform(response_df[col].astype(str))

# Prepare one-hot encoded course matrix
course_matrix = response_df.groupby('Roll No.(8 Digits)')['course'].apply(lambda x: ', '.join(x.dropna())).reset_index()
course_matrix['course'] = course_matrix['course'].apply(lambda x: x.split(', ') if x else [])
course_matrix = course_matrix.set_index('Roll No.(8 Digits)')

# One-hot encode courses
course_onehot = course_matrix['course'].apply(pd.Series).stack().str.get_dummies().groupby(level=0).sum()

# Set index for response_df for merge
response_df = response_df.set_index('Roll No.(8 Digits)')

# Ensure unique indices before merging
response_df = response_df[~response_df.index.duplicated(keep='first')]
course_onehot = course_onehot[~course_onehot.index.duplicated(keep='first')]

# Align indices and merge
common_index = response_df.index.intersection(course_onehot.index)
response_df = response_df.loc[common_index]
course_onehot = course_onehot.loc[common_index]
response_df = pd.concat([response_df, course_onehot], axis=1).fillna(0)

# Reset index for flat DataFrame
response_df.reset_index(inplace=True)

# Prepare numeric data for Gower distance
gower_ready_df = response_df.select_dtypes(include=[np.number])

# Compute Gower distance matrix
gower_dist_matrix = gower_matrix(gower_ready_df)

# Clustering using KMedoids
n_clusters = 3
kmedoids = KMedoids(n_clusters=n_clusters, metric="precomputed", random_state=42)
kmedoids.fit(gower_dist_matrix)

# Add cluster labels to DataFrame
response_df['Cluster'] = kmedoids.labels_

# Safe encoding for new user
def safe_encode(encoder, response):
    try:
        return encoder.transform([response])[0]
    except ValueError:
        return encoder.fit([response]).transform([response])[0]

# New user data
new_user_responses = {
    'Interest in Subjects: How interested are you in exploring new subjects?': 'a) Very interested',
    'Skill Development: How important is skill development in your choice of electives?': 'a) Very important',
    'Preferred Learning Method: Which learning method do you prefer?': 'b) Hands-on projects',
    'Time Commitment: How many hours per week can you dedicate to a subject?': 'b) 2-4 hours',
    'Exam Preparation: How do you usually prepare for exams?': 'a) Last-minute',
    'Mock Test Participation: How often do you take mock tests?': 'b) Rarely',
    'Psychological State Before Tests: How do you feel before taking an exam?': 'b) Anxious',
    'Time Management: How do you plan to manage the workload?': 'b) Balance with other courses',
    'Career Goals: How important is alignment with career goals in choosing a Subject?': 'b) Important',
    'Learning Motivation: What motivates you to choose a Subject?': 'a) Interest in the subject',
    'Peer Influence: Would you consider a subject because your peers are choosing it?': 'a) Yes',
    'Feedback from Seniors: Have you received feedback from seniors about your course in general?': 'a) Yes, positive',
    'Resource Availability: Do you have access to necessary resources for Subjects?': 'a) Yes',
    'Future Studies: Are you planning further studies in any area?': 'b) No',
    'marks': 75,
    'courses_taken': []  # New user, no courses taken yet
}

# Encode the new user's responses
new_user_encoded = {}
for col in new_user_responses:
    if col in categorical_columns:
        new_user_encoded[col] = safe_encode(encoder, new_user_responses[col])

# Add the new user data to the response_df (as a new row)
new_user_df = pd.DataFrame([new_user_encoded])
response_df = pd.concat([response_df, new_user_df], ignore_index=True)

# Prepare numeric data for Gower distance
gower_ready_df = response_df.select_dtypes(include=[np.number])

# Compute Gower distance matrix
gower_dist_matrix = gower_matrix(gower_ready_df)

# Re-cluster including the new user
kmedoids.fit(gower_dist_matrix)
response_df['Cluster'] = kmedoids.labels_

# Function to recommend courses for the new user based on their cluster
def recommend_courses_for_new_user(new_user_responses, top_n=3):
    new_user_encoded = {}
    for col in new_user_responses:
        if col in categorical_columns:
            new_user_encoded[col] = safe_encode(encoder, new_user_responses[col])

    # Add the new user data to the response DataFrame
    new_user_df = pd.DataFrame([new_user_encoded])
    response_df = pd.concat([response_df, new_user_df], ignore_index=True)

    # Now that the new user is part of the dataset, perform clustering and recommend courses
    gower_ready_df = response_df.select_dtypes(include=[np.number])
    gower_dist_matrix = gower_matrix(gower_ready_df)

    kmedoids.fit(gower_dist_matrix)
    response_df['Cluster'] = kmedoids.labels_

    # Find the cluster of the new user (last added user)
    new_user_cluster = response_df.iloc[-1]['Cluster']

    # Get other students in the same cluster
    cluster_students = response_df[response_df['Cluster'] == new_user_cluster]

    # Get the courses taken by students in the same cluster
    cluster_ids = cluster_students['Roll No.(8 Digits)']
    cluster_courses_series = course_matrix.loc[course_matrix.index.isin(cluster_ids), 'course'].explode()
    common_courses = cluster_courses_series.value_counts().head(top_n).index.tolist()

    # Exclude courses already taken by the new user
    student_courses = course_matrix.loc[new_user_df.index[0], 'course'] if new_user_df.index[0] in course_matrix.index else []
    recommended_courses = [course for course in common_courses if course not in student_courses]

    return recommended_courses[:top_n]

# Recommendation function
def recommend_courses_based_on_cluster(student_id, top_n=3):
    if student_id not in response_df['Roll No.(8 Digits)'].values:
        return ["Student ID not found."]

    student_row = response_df[response_df['Roll No.(8 Digits)'] == student_id]
    student_cluster = student_row['Cluster'].values[0]
    cluster_students = response_df[response_df['Cluster'] == student_cluster]

    # Courses taken by students in the same cluster
    cluster_ids = cluster_students['Roll No.(8 Digits)']
    cluster_courses_series = course_matrix.loc[course_matrix.index.isin(cluster_ids), 'course'].explode()
    common_courses = cluster_courses_series.value_counts().head(top_n).index.tolist()

    # Exclude already taken by the student
    student_courses = course_matrix.loc[student_id, 'course'] if student_id in course_matrix.index else []
    recommended = [c for c in common_courses if c not in student_courses]

    return recommended[:top_n]

# Example usage
recommended_courses = recommend_courses_for_new_user(new_user_responses)
print(f"Recommended Courses for the new student: {recommended_courses}")
