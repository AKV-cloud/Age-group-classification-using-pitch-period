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
        st.write(f"l is {l}") 
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
def age_group(pitch_period_ms):
    if 30 <= pitch_period_ms <= 80:
        return "Infant"
    elif 80 < pitch_period_ms <= 260:
        return "Child"
    elif 260 < pitch_period_ms <= 380:
        return "Teenager"
    elif 380 < pitch_period_ms <= 550:
        return "Adult"
    else:
        return "Elderly"

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
age = age_group(pitch_period_To * 1000)

    # Create the plots
fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(8, 8))
axs[0].plot(t, y)
axs[0].set_title('Speech Signal')
axs[0].set_xlabel('time in milliseconds')
st.pyplot(t,y)

kk = np.arange(len(autocor)) * (1/Fs) * 1000
axs[1].plot(kk, autocor)
axs[1].set_title('Autocorrelation of Speech Signal')
axs[1].set_xlabel('time in milliseconds')
st.pyplot(kk,autocor)

    # Display the pitch period and age group
st.write(f"Audio file selected is: {selected_file}")
st.write(f"Pitch period: {pitch_period_To*1000} ms")
st.write(f"Pitch frequency: {pitch_freq_Fo} Hz")
st.write(f"Age group: {age}")
