import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

st.markdown("<h1 style='text-align: center; color: white;'>Age Group Classification Using Pitch Period Computed Using Autocorrelation Function</h1>",
            unsafe_allow_html=True)
st.sidebar.markdown("Submitted By : ")
st.sidebar.markdown(" **_Arun Kumar V_** ")
st.sidebar.markdown(" **_122001049_**")
st.sidebar.markdown("Under the Supervision of : ")
st.sidebar.markdown(" **Dr. M. Sabarimalai Manikandan** ")
st.sidebar.markdown(" **IIT Palakkad**")

# Define a function to compute autocorrelation
def autocorr(y):
    autocor = np.zeros(len(y))
    for l in range(len(y)): 
        sum1 = 0
        for u in range(len(y)-l):
            s = y[u] * y[u+l]
            sum1 = sum1 + s
        autocor[l] = np.sum(sum1)
    return autocor

# Define a function to find the pitch period and pitch frequency
def pitch_period_freq(autocor, Fs):
    auto = autocor[20:]
    max1 = 0
    sample_no = 0
    for uu in range(len(auto)):
        if auto[uu] > max1:
            max1 = auto[uu]
            sample_no = uu
    pitch_period_To = (20 + sample_no) * (1/Fs)
    pitch_freq_Fo = 1 / pitch_period_To
    return pitch_period_To, pitch_freq_Fo

# Define a function to get age group based on pitch period
def age_group(pitch_freq):
    if  pitch_freq <= 110:
        return "Elderly"
    elif 110 < pitch_freq <= 190:
        return "Adult"
    elif 190 < pitch_freq <= 280:
        return "Teenager"
    elif 280 < pitch_freq <= 450:
        return "Infant"
    else:
        return "Unknown"

# Define a list of input file names
input_files = ['adult1.wav', 'oldman8K1sec.wav', 'infant1sec.wav']

selected_file = st.radio("Select an input file", input_files)
Fs, y = wavfile.read(selected_file)
bits = 16  # assuming the audio file is 16-bit

# Normalize the signal
max_value = np.max(np.abs(y))
y = y / max_value

# Create a time vector
t = np.arange(len(y)) * (1/Fs) * 1000

with st.spinner(f"Computing {selected_file}..."):
    # Calculate the autocorrelation of the signal
     autocor = autocorr(y)

# Find the pitch period and pitch frequency
pitch_period_To, pitch_freq_Fo = pitch_period_freq(autocor, Fs)
age = age_group(pitch_freq_Fo)

    # Create the plots
# Create a separate figure for speech signal plot
fig1, axs1 = plt.subplots(figsize=(8, 4))
axs1.plot(t, y)
axs1.set_title('Speech Signal')
axs1.set_xlabel('time in milliseconds')
st.pyplot(fig1)

kk = np.arange(len(autocor)) * (1/Fs) * 1000
# Create a separate figure for ACF plot
fig2, axs2 = plt.subplots(figsize=(8, 4))
axs2.plot(kk, autocor)
axs2.set_title('Autocorrelation of Speech Signal')
axs2.set_xlabel('time in milliseconds')
st.pyplot(fig2)


    # Display the pitch period and age group
st.write(f"Audio file selected is: {selected_file}")
st.write(f"Pitch period: {pitch_period_To*1000} ms")
st.write(f"Pitch frequency: {pitch_freq_Fo} Hz")
st.write(f"Age group: {age}")
