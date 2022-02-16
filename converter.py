from os import remove
from pydub import AudioSegment
import speech_recognition as sr


def ogg_to_flac(file):

    ogg_audio_file = file
    flac_audio_file = ogg_audio_file.split('.')[0] + '.flac'

    i = AudioSegment.from_ogg(ogg_audio_file)
    i.export(flac_audio_file, format="flac")

    return flac_audio_file


def text_from_ogg(ogg_audio_file) -> str:
    audio_file = ogg_to_flac(ogg_audio_file)

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)  # read the entire audio file

    # recognize speech using Google Speech Recognition
    try:
        texted_speech = r.recognize_google(audio, language='ru_RU')
        print("Google Speech Recognition thinks you said " + texted_speech)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    remove(audio_file)

    return texted_speech

# print(eval(text_from_ogg('/Users/shigarovms/PycharmProjects/SpeechRecognition 1st/Audio_oggs/2022-02-15 18.42.17.ogg')))