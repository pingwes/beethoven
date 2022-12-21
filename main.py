import pretty_midi
import os
import csv
import spacy
import random

f = open('training_examples/completions.tsv', 'w')
tsv_writer = csv.writer(f, delimiter='\t')
nlp = spacy.load("en_core_web_sm")


def tokenize_prompts(text):

    doc = nlp(text)

    return ([chunk.text for chunk in doc.noun_chunks],\
           [token.lemma_ for token in doc if token.pos_ == "VERB"],
           [token.lemma_ for token in doc if token.pos_ == "ADJ"])


def randomize_tokens(nouns, verbs, adjectives):

    random_tokens = []

    random_value = random.randint(0, len(nouns))
    for x in range(random_value):
        random_tokens.append(nouns[random.randint(0, len(nouns)-1)])

    random_value = random.randint(0, len(verbs))
    for x in range(random_value):
        random_tokens.append(verbs[random.randint(0, len(verbs)-1)])

    random_value = random.randint(0, len(adjectives))
    for x in range(random_value):
        random_tokens.append(adjectives[random.randint(0, len(adjectives)-1)])

    random.shuffle(random_tokens)

    return ' '.join(random_tokens)


def transpose(key, note):

    key = key[:-5].lower().strip("-").split("-")

    if len(key) == 1:
        if key[0] == "a":
            adjusted_pitch = note.pitch + 3
        if key[0] == "b":
            adjusted_pitch = note.pitch + 1
        if key[0] == "c":
            adjusted_pitch = note.pitch
        if key[0] == "d":
            adjusted_pitch = note.pitch - 2
        if key[0] == "e":
            adjusted_pitch = note.pitch - 4
        if key[0] == "f":
            adjusted_pitch = note.pitch - 5
        if key[0] == "g":
            adjusted_pitch = note.pitch - 7

    # handle sharps and flats
    elif len(key) == 2:
        if (key[0] == "a" and key[1] == "sharp") or (key[0] == "b" and key[1] == "flat") :
            adjusted_pitch = note.pitch + 2
        if (key[0] == "g" and key[1] == "sharp") or (key[0] == "a" and key[1] == "flat"):
            adjusted_pitch = note.pitch + 4
        if (key[0] == "c" and key[1] == "sharp") or (key[0] == "d" and key[1] == "flat"):
            adjusted_pitch = note.pitch - 1
        if (key[0] == "d" and key[1] == "sharp") or (key[0] == "e" and key[1] == "flat"):
            adjusted_pitch = note.pitch - 3
        if (key[0] == "f" and key[1] == "sharp") or (key[0] == "g" and key[1] == "flat"):
            adjusted_pitch = note.pitch - 6

    return pretty_midi.Note(velocity=note.velocity, pitch=adjusted_pitch, start=note.start, end=note.end)


def convert_to_string(notes):

    completion = ""

    for note in notes:
        pitch = str(note.pitch)
        velocity = str(note.velocity)
        start = str(note.start)
        end = str(note.end)

        if len(start) >= 7:
            start = start[:7].strip()
        if len(end) >= 7:
            end = end[:7].strip()

        completion += pitch + "," + velocity + "," + start[:5] + "," + end[:5] + "\n"

    return completion


def time_adjust(notes):
    starting_note = notes[0]
    adjusted_notes = []

    for note in notes:
        adjusted_note = pretty_midi.Note(velocity=note.velocity,
                                         pitch=note.pitch,
                                         start=note.start - starting_note.start,
                                         end=note.end - starting_note.start)
        adjusted_notes.append(adjusted_note)
    return adjusted_notes


def process(folder, file):

    midi_data = pretty_midi.PrettyMIDI("midi/historical/" + folder + "/" + file)

    clips = 1
    merged = midi_data.instruments[0].notes + midi_data.instruments[1].notes

    sorted_notes = sorted(merged, key=lambda x: x.start, reverse=False)

    completed_notes = []

    for note in sorted_notes:
        key = folder.split("_")[2]

        transposed_note = transpose(key,note)
        if transposed_note.start < (20*clips):
            completed_notes.append(transposed_note)
        else:
            if completed_notes:
                time_adjusted_notes = time_adjust(completed_notes)

                completion = convert_to_string(time_adjusted_notes)
                completed_notes = []

                tsv_writer.writerow([completion[:103], completion[103:]])
                clips += 1


directory = "midi/historical"
tsv_writer.writerow(["prompt", "completion"])

for folder in os.listdir(directory):
    if folder[:6] == "sonata":
        for file in os.listdir("midi/historical/"+folder):
            if file.endswith('.mid'):
                process(folder,file)


