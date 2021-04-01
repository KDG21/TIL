import moviepy.editor as mp
import numpy as np
import parselmouth
import numpy as np
import matplotlib.pyplot as plt

# clip = mp.VideoFileClip('C:\\Users\\USER\\Downloads\\present.mp4')
# clip.audio.write_audiofile('C:\\Users\\USER\\Downloads\\audio.wav')

audio_path = 'C:/Users/USER/Downloads/eunchan.wav'
file = audio_path.split('/')[4]


pitch_values = []
pitch_ceiling = 400   # In Hz, change according to gender
pitch_floor = 50    # In Hz, change according to gender
smooth_bandwidth = 5


def load_wave(filepath):
    waveform = parselmouth.Sound(filepath)
    waveform = parselmouth.praat.call(waveform, "Convert to mono")
    return waveform

def extract_pitch(waveform):
    return waveform.to_pitch(pitch_ceiling=pitch_ceiling, pitch_floor=pitch_floor)

def set_pitch_analysis(pitch_analysis):
    print(pitch_analysis)

    # Array with fundamental frequency values
    pitch_countour = pitch_analysis.selected_array['frequency']
    pitch_countour[pitch_countour == 0] = np.nan
    pitch_values.append(pitch_countour)
    print(pitch_values)

    # Interpolated contour
    interpolated = pitch_analysis.interpolate().selected_array['frequency']
    interpolated[interpolated == 0] = np.nan

    # Smoothed version
    smoothed = pitch_analysis.smooth(bandwidth=smooth_bandwidth).selected_array['frequency']
    smoothed[smoothed == 0] = np.nan

    draw_pitch(interpolated, pitch_analysis.xs())
    print(np.nanmean(interpolated))

def draw_pitch(interpolated, xaxis):
    plt.clf()
    plt.ylim(pitch_floor, pitch_ceiling)
    plt.ylabel("Fundamental Frequency (Hz)")
    plt.xlabel("Time (s)")
    # plt.plot(xaxis, pitch, color='red', label='pitch')
    plt.plot(xaxis, interpolated, color='purple', label='interpolated', alpha=0.5)
    # plt.plot(xaxis, smoothed, color='blue', label='smoothed')
    plt.legend()
    plt.title('Pitch '+file)
    plt.savefig('Pitch '+file.replace('wav', 'png'))


set_pitch_analysis(extract_pitch(load_wave(audio_path)))