class RGBLedSettings(object):
    R_pin = 37
    G_pin = 35
    B_pin = 33

    adc_R = 0
    adc_G = 1
    adc_B = 2

class ButtonSettings(object):
    pin = 12

class MusicGeneratorSettings(object):
    log = "INFO"
    qpm = 120
    steps_per_iteration = 1
    temperature = 1.0
    branch_factor = 1
    beam_size = 1
    condition_on_primer = True
    inject_primer_during_generation = True
    num_steps = 128
    num_outputs = 5
    output_dir = "/tmp/polyphony_rnn/generated"
    config = "polyphony"
    bundle_file = "/home/pi/resources/polyphony_rnn.mag"
    hparams = ""