#!/usr/bin/env python

################
# Dependencies #
################

import sys
import speech_recognition as sr
import os
from pydub.silence import split_on_silence
from pydub import AudioSegment

###########
# Classes #
###########

class log:
  reset     = '\033[0m'
  bold      = '\033[1m'
  dim       = '\033[2m'
  underline = '\033[4m'
  red       = '\033[91m'
  green     = '\033[92m'
  yellow    = '\033[93m'
  blue      = '\033[94m'
  magenta   = '\033[95m'
  cyan      = '\033[96m'

  def debug(string):
    print(f"\033[2m[debug]\033[0m {string}")

  def error(string, exit_code=1):
    print(f"\033[2m[\033[0m\033[91merror\033[0m\033[2m]\033[0m {string}")
    exit(exit_code)

  def info(string):
    print(f"\033[2m[\033[0m\033[92minfo \033[0m\033[2m]\033[0m {string}")

  def warn(string):
    print(f"\033[2m[\033[0m\033[93mwarn \033[0m\033[2m]\033[0m {string}")

#############
# Functions #
#############

def get_help():

  print(f"{log.bold}V2T{log.reset}")
  print()
  print(f"{log.bold}{log.green}Usage:{log.reset}")
  print(f"  v2t.py {log.bold}{log.cyan}--file{log.reset} {log.underline}FILE.wav{log.reset} {log.bold}{log.cyan}--language{log.reset} {log.underline}LANGUAGE{log.reset}")
  print()
  
  exit(0)

def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    print(f"Processing {arg_file} in {arg_language}:")
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened, language=arg_language)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print("=>", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text

def parse_args():

  global arg_file
  global arg_language

  arg_file = None # Required
  arg_language = None # Required

  # Eliminating the first arg (self program name)
  sys.argv.pop(0)

  # Printing help if called without user args
  if not sys.argv:
    get_help()

  # Processing user args
  while sys.argv:

    # File
    if sys.argv[0] == '--file':

      # Value
      sys.argv.pop(0)
      if sys.argv:
        arg_file = sys.argv[0]
        sys.argv.pop(0)
      else:
        log.error('Missing value for \'--file\' argument')

    # Language
    elif sys.argv[0] == '--language':

      # Value
      sys.argv.pop(0)
      if sys.argv:
        arg_language = sys.argv[0]
        sys.argv.pop(0)
      else:
        log.error('Missing value for \'--language\' argument')

    # Unknown
    else:
      log.debug(f"Ignoring unknown arg '{sys.argv[0]}'")
      sys.argv.pop(0)

  # Checking if all required args was informed

  if arg_file is None:
    log.error('Missing required argument \'--file\'')

  if arg_language is None:
    log.error('Missing required argument \'--language\'')

  return(0)

##########
# Script #
##########

# Processing user args
parse_args()

# # Recognizer
r = sr.Recognizer()

# # Convertion
# with sr.AudioFile(arg_file) as input:
#   # Listen
#   audio_data = r.record(input)
#   # Recognize
#   text = r.recognize_google(audio_data, language=arg_language)
#   print(text)

full_text = get_large_audio_transcription(arg_file)

print("\nFull text:\n")
print(full_text)
