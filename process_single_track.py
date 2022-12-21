import pretty_midi


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


midi_data = pretty_midi.PrettyMIDI("midi/historical/for_elise/elise.mid")
merged = midi_data.instruments[0].notes + midi_data.instruments[1].notes


sonata = convert_to_string(merged)

print(sonata)