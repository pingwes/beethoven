import csv
import pretty_midi

piano_midi = pretty_midi.PrettyMIDI()
piano_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
piano = pretty_midi.Instrument(piano_program)

f = open('sonata.csv', 'r')
csv_reader = csv.reader(f, delimiter=",")

for row in csv_reader:
    pitch = int(row[0])
    velocity = int(row[1])
    start = float(row[2])
    end = float(row[3])

    note = pretty_midi.Note(
        pitch=pitch,
        velocity=velocity,
        start=start,
        end=end
    )

    piano.notes.append(note)
    print(row)

piano_midi.instruments.append(piano)
piano_midi.write("midi/generated/piano79.mid")