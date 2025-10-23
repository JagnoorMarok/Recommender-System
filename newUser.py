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

# Encode categorical responses by extracting the first letter (option alphabet)
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

# Function to safely encode responses
def safe_encode(encoder, new_value):
    # Extract the first letter (alphabet) from the response text (e.g., 'a', 'b', etc.)
    option_letter = new_value[0]  # e.g., 'a', 'b'
    try:
        # Transform the option letter into an integer
        return encoder.transform([option_letter])[0]
    except ValueError:  # If new letter is encountered
        # If the option is unseen, append the new letter to the encoder's classes and return the encoded value
        encoder.classes_ = np.append(encoder.classes_, option_letter)
        return encoder.transform([option_letter])[0]

# Encode the responses in the DataFrame
for col in categorical_columns:
    if col in response_df.columns:
        # Extract the first letter from the response and fit the encoder
        response_df[col] = response_df[col].str[0]  # Only keep the first letter of the response
        encoder.fit(response_df[col].astype(str))

# Prepare the response for a new user
new_user_responses = {
    'Submission ID':'11d734c1-2d1a-4a52-83d1-09112798b34b',
    'Submission time':'2025-03-04 14:36:05',
    'Name':'Jagnoor Singh',
    'Roll No.(8 Digits)':'22103078',
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
}

# Encode the new user responses
new_user_encoded = {}
for col in new_user_responses:
    if col in categorical_columns:
        new_user_encoded[col] = safe_encode(encoder, new_user_responses[col])

# Add the new user data to the response_df
new_user_df = pd.DataFrame([new_user_encoded])
response_df = pd.concat([response_df, new_user_df], ignore_index=True)

# Ensure proper preprocessing and clustering (same as previous code)
# Prepare numeric data for Gower distance
gower_ready_df = response_df.select_dtypes(include=[np.number])

# Handle missing values before clustering
# For numeric columns, replace NaN with the mean of that column
gower_ready_df = gower_ready_df.fillna(gower_ready_df.mean())

# For categorical columns, you can replace NaN with the mode (most frequent value)
for col in categorical_columns:
    response_df[col] = response_df[col].fillna(response_df[col].mode()[0])

# Recompute the Gower distance matrix after handling NaN values
gower_dist_matrix = gower_matrix(response_df)

# Check if there are NaNs in the Gower matrix
if np.any(np.isnan(gower_dist_matrix)):
    print("Warning: Gower matrix contains NaN values. Removing rows/columns with NaNs.")
    # Remove rows and columns that contain NaN values
    gower_dist_matrix = np.nan_to_num(gower_dist_matrix)

# Clustering using KMedoids
n_clusters = 3
kmedoids = KMedoids(n_clusters=n_clusters, metric="precomputed", random_state=42)

# Attempt to fit KMedoids with the preprocessed Gower distance matrix
try:
    kmedoids.fit(gower_dist_matrix)
    response_df['Cluster'] = kmedoids.labels_
except ValueError as e:
    print(f"Error during clustering: {e}")

# Function to recommend courses for the new user based on their cluster
def recommend_courses_for_new_user(response_df, new_user_responses, top_n=3):
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

    # Check if there are NaNs in the Gower matrix
    if np.any(np.isnan(gower_dist_matrix)):
        print("Warning: Gower matrix contains NaN values. Removing rows/columns with NaNs.")
        gower_dist_matrix = np.nan_to_num(gower_dist_matrix)

    kmedoids.fit(gower_dist_matrix)
    response_df['Cluster'] = kmedoids.labels_

    # Find the cluster of the new user (last added user)
    new_user_cluster = response_df.iloc[-1]['Cluster']

    # Get other students in the same cluster
    cluster_students = response_df[response_df['Cluster'] == new_user_cluster]

    # Get the courses taken by students in the same cluster
    cluster_ids = cluster_students['Roll No.(8 Digits)']
    cluster_courses_series = cluster_students['course'].explode()
    common_courses = cluster_courses_series.value_counts().head(top_n).index.tolist()

    # Exclude courses already taken by the new user
    student_courses = cluster_students.loc[cluster_students['Roll No.(8 Digits)'] == new_user_responses['Roll No.(8 Digits)'], 'course']
    recommended_courses = [course for course in common_courses if course not in student_courses]

    return recommended_courses[:top_n]

# Example usage for the new user
recommended_courses = recommend_courses_for_new_user(response_df, new_user_responses)
print(f"Recommended Courses for new user: {recommended_courses}")
