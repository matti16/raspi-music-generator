import ast
import os
import time
import threading
import random

from magenta.models.polyphony_rnn import polyphony_model
from magenta.models.polyphony_rnn import polyphony_sequence_generator
from magenta.models.shared import sequence_generator
from magenta.models.shared import sequence_generator_bundle
import note_seq
from note_seq.protobuf import generator_pb2
from note_seq.protobuf import music_pb2

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

from raspi_music_generator.settings import MusicGeneratorSettings
from raspi_music_generator.adapters.button import Button
from raspi_music_generator.adapters.player import Player


class MusicGenerator():

    def __init__(self, led):
        self.button = Button()
        self.player = Player(MusicGeneratorSettings.output_dir)
        self.led = led

        bundle_file = os.path.expanduser(MusicGeneratorSettings.bundle_file)
        bundle = sequence_generator_bundle.read_bundle_file(bundle_file)
        tf.logging.set_verbosity(MusicGeneratorSettings.log)

        config_id = bundle.generator_details.id
        config = polyphony_model.default_configs[config_id]
        config.hparams.parse(MusicGeneratorSettings.hparams)
        
        # Having too large of a batch size will slow generation down unnecessarily.
        config.hparams.batch_size = min(
            config.hparams.batch_size, 
            MusicGeneratorSettings.beam_size * MusicGeneratorSettings.branch_factor
            )

        self.generator = polyphony_sequence_generator.PolyphonyRnnSequenceGenerator(
            model=polyphony_model.PolyphonyRnnModel(config),
            details=config.details,
            steps_per_quarter=config.steps_per_quarter,
            checkpoint=None,
            bundle=bundle
            )


    def _get_note_from_perc(self, x):
        return int(x / 100 * (MusicGeneratorSettings.max_note - MusicGeneratorSettings.min_note) + MusicGeneratorSettings.min_note)

    def _get_primer_melody(self):
        r, g, b = self.led.read_values()
        r_note, g_note, b_note = self._get_note_from_perc(r), self._get_note_from_perc(g), self._get_note_from_perc(b)
        primer = []
        for n in [r_note, g_note, b_note]:
            for _ in range(random.randint(1, 3)):
                primer.append(n)
                primer.append(-2)
        return str(primer)


    def run(self):
        """Generates polyphonic tracks and saves them as MIDI files.
        Uses the options specified by the flags defined in this module.
        Args:
            generator: The PolyphonyRnnSequenceGenerator to use for generation.
        """
        primer_melody = self._get_primer_melody()

        output_dir = os.path.expanduser(MusicGeneratorSettings.output_dir)

        if not tf.gfile.Exists(output_dir):
            tf.gfile.MakeDirs(output_dir)
        
        for i in os.listdir(output_dir):
            os.remove(os.path.join(output_dir, i))

        primer_sequence = None
        qpm = MusicGeneratorSettings.qpm 

        primer_melody = note_seq.Melody(ast.literal_eval(primer_melody))
        primer_sequence = primer_melody.to_sequence(qpm=qpm)

        # Derive the total number of seconds to generate.
        seconds_per_step = 60.0 / qpm / self.generator.steps_per_quarter
        generate_end_time = MusicGeneratorSettings.num_steps * seconds_per_step

        # Specify start/stop time for generation based on starting generation at the
        # end of the priming sequence and continuing until the sequence is num_steps
        # long.
        generator_options = generator_pb2.GeneratorOptions()
        # Set the start time to begin when the last note ends.
        generator_options.generate_sections.add(
            start_time=primer_sequence.total_time,
            end_time=generate_end_time)

        generator_options.args['temperature'].float_value = MusicGeneratorSettings.temperature
        generator_options.args['beam_size'].int_value = MusicGeneratorSettings.beam_size
        generator_options.args['branch_factor'].int_value = MusicGeneratorSettings.branch_factor
        generator_options.args['steps_per_iteration'].int_value = MusicGeneratorSettings.steps_per_iteration
        generator_options.args['condition_on_primer'].bool_value = MusicGeneratorSettings.condition_on_primer
        generator_options.args['no_inject_primer_during_generation'].bool_value = not MusicGeneratorSettings.inject_primer_during_generation

        # Make the generate request num_outputs times and save the output as midi
        # files.
        digits = len(str(MusicGeneratorSettings.num_outputs))
        for i in range(MusicGeneratorSettings.num_outputs):
            generated_sequence = self.generator.generate(primer_sequence, generator_options)
            midi_filename = str(i + 1).zfill(digits) + ".mid"
            midi_path = os.path.join(output_dir, midi_filename)
            note_seq.sequence_proto_to_midi_file(generated_sequence, midi_path)
            
            if i == 0:
                threading.Thread(target=self.player.play).start()
            elif i == 1:
                self.player.enqueue(midi_path)

        tf.logging.info('Wrote %d MIDI files to %s',
                        MusicGeneratorSettings.num_outputs, output_dir)    

    
    def _button_listener(self):
        playing = False
        while True:
            if self.button.read_button():
                if not playing:
                    self.run()
                    playing = True
                else:
                    self.player.stop()
                    playing = False


    def start_button_listener(self):
        self.button_thread = threading.Thread(target=self._button_listener)
        self.button_thread.start()