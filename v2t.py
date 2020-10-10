#!/usr/bin/env python

# Dependencies
import speech_recognition as sr
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence

#########
# Input #
#########

input_file = "audio.wav"

##############
# Processing #
##############

# Recognizer
r = sr.Recognizer()

# Convertion
with sr.AudioFile(input_file) as input:
  # Listen
  audio_data = r.record(input)
  # Recognize
  text = r.recognize_google(audio_data, language="pt-BR")
  print(text)

##########
# Output #
##########

