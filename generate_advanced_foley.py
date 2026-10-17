"""
Journey of Mankind - Advanced Foley & Tactile Sound Synthesizer
Generates ultra-realistic acoustic physical audio:
1. Weather: rain_ambient, rain_roof, thunder_distant, thunder_close
2. Cooking & Metallurgy: meat_sizzle, metal_quench
3. Human Physiology: heavy_panting, yawn, shiver, gear_rustle, baby_coo
4. Canine Companion & Wildlife: whistle, dog_bark, dog_whimper, animal_graze, animal_alert
5. Multi-Sample Footsteps: wood (1-4), dirt (3-4), grass (3-4), stone (3-4), sand (3-4), snow (3-4), water (3-4)
"""

import os
import wave
import struct
import math
import random

SOUNDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sounds')
os.makedirs(SOUNDS_DIR, exist_ok=True)

def clamp(v):
    return max(-32767, min(32767, int(v)))

def write_wav(filename, samples, sample_rate=44100):
    filepath = os.path.join(SOUNDS_DIR, filename)
    with wave.open(filepath, 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        packed = struct.pack(f'<{len(samples)}h', *[clamp(s) for s in samples])
        wav.writeframes(packed)
    print(f"Generated {filename} ({len(samples)} samples, {len(samples)/sample_rate:.2f}s)")

# ----------------- WEATHER FOLEY -----------------

def gen_rain_ambient(duration=4.0, sample_rate=44100):
    """Continuous dense raindrops falling on foliage and earth."""
    n = int(duration * sample_rate)
    samples = [0.0] * n
    # Pink noise base
    b0 = b1 = b2 = b3 = b4 = b5 = b6 = 0.0
    for i in range(n):
        white = random.uniform(-1.0, 1.0)
        b0 = 0.99886 * b0 + white * 0.0555179
        b1 = 0.99332 * b1 + white * 0.0750759
        b2 = 0.96900 * b2 + white * 0.1538520
        b3 = 0.86650 * b3 + white * 0.3104856
        b4 = 0.55000 * b4 + white * 0.5329522
        b5 = -0.7616 * b5 - white * 0.0168980
        pink = b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362
        b6 = white * 0.115926
        samples[i] += pink * 1800.0

    # Distinct droplet pings
    num_drops = int(duration * 120)
    for _ in range(num_drops):
        pos = random.randint(0, n - 400)
        freq = random.uniform(1200.0, 3200.0)
        amp = random.uniform(2500.0, 7000.0)
        for j in range(350):
            t = j / sample_rate
            env = math.exp(-35.0 * t * 100.0)
            samples[pos + j] += math.sin(2 * math.pi * freq * t) * amp * env
    return samples

def gen_rain_roof(duration=4.0, sample_rate=44100):
    """Muffled raindrops drumming on wooden shelter roof planks."""
    n = int(duration * sample_rate)
    samples = [0.0] * n
    # Low muffled rumble
    b0 = 0.0
    for i in range(n):
        white = random.uniform(-1.0, 1.0)
        b0 = 0.98 * b0 + white * 0.02
        samples[i] += b0 * 2500.0

    # Wooden thuds of drops
    num_drops = int(duration * 90)
    for _ in range(num_drops):
        pos = random.randint(0, n - 600)
        freq = random.uniform(160.0, 380.0)
        amp = random.uniform(3500.0, 8500.0)
        for j in range(500):
            t = j / sample_rate
            env = math.exp(-22.0 * t * 100.0)
            wood_body = math.sin(2 * math.pi * freq * t) + 0.4 * math.sin(2 * math.pi * freq * 2.1 * t)
            samples[pos + j] += wood_body * amp * env
    return samples

def gen_thunder_distant(sample_rate=44100):
    """Rolling, low-frequency distant thunder rumble."""
    duration = 3.5
    n = int(duration * sample_rate)
    samples = [0.0] * n
    lp = 0.0
    for i in range(n):
        t = i / sample_rate
        env = math.sin(math.pi * (t / duration)) ** 1.8
        white = random.uniform(-1.0, 1.0)
        lp = lp * 0.985 + white * 0.015
        sub = math.sin(2 * math.pi * (45.0 + 15.0 * math.sin(t * 3.0)) * t) * 0.4
        samples[i] = (lp + sub) * env * 24000.0
    return samples

def gen_thunder_close(sample_rate=44100):
    """Sudden sharp explosive lightning crack followed by massive bass boom."""
    duration = 3.0
    n = int(duration * sample_rate)
    samples = [0.0] * n
    # Initial sharp lightning snap (t=0.0 to 0.05s)
    snap_len = int(0.06 * sample_rate)
    for i in range(snap_len):
        t = i / sample_rate
        env = math.exp(-80.0 * t)
        noise = random.uniform(-1.0, 1.0) * env * 32000.0
        snap_sin = math.sin(2 * math.pi * 1400.0 * t) * env * 20000.0
        samples[i] += noise + snap_sin

    # Low rumble reverberation tail
    lp = 0.0
    for i in range(n):
        t = i / sample_rate
        env = math.exp(-1.4 * t)
        white = random.uniform(-1.0, 1.0)
        lp = lp * 0.982 + white * 0.018
        bass = math.sin(2 * math.pi * (55.0 - 10.0 * (t / duration)) * t) * 0.5
        samples[i] += (lp + bass) * env * 28000.0
    return samples

# ----------------- COOKING & METALLURGY -----------------

def gen_meat_sizzle(duration=3.5, sample_rate=44100):
    """Crisp sizzling fat bubbles and spitting embers of roasting meat."""
    n = int(duration * sample_rate)
    samples = [0.0] * n
    # Continuous frying white noise
    hp = 0.0
    for i in range(n):
        white = random.uniform(-1.0, 1.0)
        hp = white - (hp * 0.92)
        samples[i] += hp * 1400.0

    # Spitting grease pops
    num_pops = int(duration * 75)
    for _ in range(num_pops):
        pos = random.randint(0, n - 300)
        amp = random.uniform(4000.0, 14000.0)
        freq = random.uniform(800.0, 3200.0)
        for j in range(250):
            t = j / sample_rate
            env = math.exp(-80.0 * t * 100.0)
            pop = math.sin(2 * math.pi * freq * t) + random.uniform(-0.3, 0.3)
            samples[pos + j] += pop * amp * env
    return samples

def gen_metal_quench(duration=2.5, sample_rate=44100):
    """Violent steam eruption as red-hot bronze metal is plunged into cold water."""
    n = int(duration * sample_rate)
    samples = [0.0] * n
    lp = 0.0
    for i in range(n):
        t = i / sample_rate
        env = math.exp(-1.8 * t)
        white = random.uniform(-1.0, 1.0)
        # Sibilant steam hiss
        hiss = white * env * (18000.0 + 8000.0 * math.sin(2 * math.pi * 3800.0 * t))
        # Water bubbling cavitation
        bubble = math.sin(2 * math.pi * (220.0 + random.uniform(-40, 40)) * t) * env * 6000.0
        samples[i] = hiss + bubble
    return samples

# ----------------- HUMAN PHYSIOLOGY & FOLEY -----------------

def gen_heavy_panting(sample_rate=44100):
    """Rhythmic deep human breath exhalations when exhausted."""
    duration = 2.4
    n = int(duration * sample_rate)
    samples = [0.0] * n
    # 2 panting cycles
    cycle_samples = int(1.2 * sample_rate)
    for c in range(2):
        start = c * cycle_samples
        in_len = int(0.35 * sample_rate)
        out_len = int(0.65 * sample_rate)
        # Inhale
        for j in range(in_len):
            t = j / in_len
            env = math.sin(math.pi * t)
            noise = random.uniform(-1.0, 1.0) * env * 3500.0
            throat = math.sin(2 * math.pi * 280.0 * (j / sample_rate)) * env * 1500.0
            samples[start + j] += noise + throat
        # Exhale
        for j in range(out_len):
            t = j / out_len
            env = math.sin(math.pi * t) ** 1.4
            noise = random.uniform(-1.0, 1.0) * env * 7500.0
            throat = math.sin(2 * math.pi * 190.0 * (j / sample_rate)) * env * 3000.0
            samples[start + in_len + j] += noise + throat
    return samples

def gen_yawn(sample_rate=44100):
    """Human tiredness yawn vocalization and stretching breath."""
    duration = 2.2
    n = int(duration * sample_rate)
    samples = [0.0] * n
    for i in range(n):
        t = i / sample_rate
        env = math.sin(math.pi * (t / duration)) ** 1.6
        # Pitch starts mid, glides up, and trails off down
        pitch = 140.0 + 60.0 * math.sin(math.pi * (t / duration))
        vocal = math.sin(2 * math.pi * pitch * t) + 0.5 * math.sin(4 * math.pi * pitch * t)
        breath = random.uniform(-0.6, 0.6)
        samples[i] = (vocal * 0.6 + breath * 0.4) * env * 8500.0
    return samples

def gen_shiver(sample_rate=44100):
    """Teeth chattering and shivering exhalation from freezing cold."""
    duration = 1.8
    n = int(duration * sample_rate)
    samples = [0.0] * n
    # Teeth clicks at ~14 clicks per second
    clicks = int(duration * 14)
    for c in range(clicks):
        pos = int(c * (sample_rate / 14) + random.randint(-100, 100))
        if pos + 300 < n:
            amp = random.uniform(5000.0, 11000.0)
            for j in range(250):
                t = j / sample_rate
                env = math.exp(-80.0 * t * 100.0)
                click = math.sin(2 * math.pi * 3200.0 * t) * env * amp
                samples[pos + j] += click
    # Shivering breath undercoat
    for i in range(n):
        t = i / sample_rate
        env = math.sin(math.pi * (t / duration)) * (0.6 + 0.4 * math.sin(2 * math.pi * 14.0 * t))
        samples[i] += random.uniform(-1.0, 1.0) * env * 2500.0
    return samples

def gen_gear_rustle(sample_rate=44100):
    """Subtle leather satchel strap and equipment friction during movement."""
    duration = 0.35
    n = int(duration * sample_rate)
    samples = [0.0] * n
    for i in range(n):
        t = i / sample_rate
        env = math.sin(math.pi * (t / duration)) ** 2
        leather = (random.uniform(-1.0, 1.0) * 0.7 + math.sin(2 * math.pi * 420.0 * t) * 0.3)
        samples[i] = leather * env * 4200.0
    return samples

def gen_baby_coo(sample_rate=44100):
    """Sweet prehistoric infant coo/giggle marking family generation milestone."""
    duration = 1.5
    n = int(duration * sample_rate)
    samples = [0.0] * n
    for i in range(n):
        t = i / sample_rate
        env = math.sin(math.pi * (t / duration)) ** 2
        # Melodic high harmonic cooing
        pitch = 440.0 + 120.0 * math.sin(2 * math.pi * 3.5 * t)
        tone = math.sin(2 * math.pi * pitch * t) + 0.4 * math.sin(4 * math.pi * pitch * t)
        samples[i] = tone * env * 9000.0
    return samples

# ----------------- CANINE COMPANION & FAUNA -----------------

def gen_whistle(sample_rate=44100):
    """Sharp, loud human finger-whistle calling companion."""
    duration = 0.55
    n = int(duration * sample_rate)
    samples = [0.0] * n
    for i in range(n):
        t = i / sample_rate
        env = math.sin(math.pi * (t / duration)) ** 0.5
        # Pitch rises then holds
        pitch = 2400.0 + 400.0 * math.sin(math.pi * (t / duration))
        tone = math.sin(2 * math.pi * pitch * t) + 0.3 * math.sin(4 * math.pi * pitch * t)
        breath = random.uniform(-0.15, 0.15)
        samples[i] = (tone + breath) * env * 18000.0
    return samples

def gen_dog_bark(sample_rate=44100):
    """Warm, friendly companion canine bark."""
    duration = 0.48
    n = int(duration * sample_rate)
    samples = [0.0] * n
    for i in range(n):
        t = i / sample_rate
        env = math.exp(-7.5 * t)
        pitch = 380.0 - 140.0 * (t / duration)
        vocal = math.sin(2 * math.pi * pitch * t) + 0.6 * math.sin(4 * math.pi * pitch * t)
        growl = math.sin(2 * math.pi * 85.0 * t) * 0.4
        noise = random.uniform(-0.3, 0.3)
        samples[i] = (vocal + growl + noise) * env * 22000.0
    return samples

def gen_dog_whimper(sample_rate=44100):
    """Soft, high-pitched dog whine asking for affection or warning."""
    duration = 0.7
    n = int(duration * sample_rate)
    samples = [0.0] * n
    for i in range(n):
        t = i / sample_rate
        env = math.sin(math.pi * (t / duration)) ** 1.8
        pitch = 950.0 + 200.0 * math.sin(2 * math.pi * 5.0 * t)
        tone = math.sin(2 * math.pi * pitch * t)
        samples[i] = tone * env * 7500.0
    return samples

def gen_animal_graze(sample_rate=44100):
    """Herbivore calm chewing and foliage rustling."""
    duration = 1.2
    n = int(duration * sample_rate)
    samples = [0.0] * n
    for i in range(n):
        t = i / sample_rate
        env = (math.sin(2 * math.pi * 2.5 * t) ** 2) * math.sin(math.pi * (t / duration))
        chew = (random.uniform(-1.0, 1.0) * 0.7 + math.sin(2 * math.pi * 260.0 * t) * 0.3)
        samples[i] = chew * env * 5500.0
    return samples

def gen_animal_alert(sample_rate=44100):
    """Low warning predator growl and defensive snort."""
    duration = 1.1
    n = int(duration * sample_rate)
    samples = [0.0] * n
    for i in range(n):
        t = i / sample_rate
        env = math.sin(math.pi * (t / duration)) ** 1.5
        growl = math.sin(2 * math.pi * 65.0 * t + 2.0 * math.sin(2 * math.pi * 22.0 * t))
        snort = random.uniform(-0.5, 0.5) if t < 0.3 else 0.0
        samples[i] = (growl * 0.75 + snort * 0.25) * env * 16000.0
    return samples

# ----------------- FOOTSTEP MULTI-VARIATIONS -----------------

def gen_footstep_wood(var_idx=1, sample_rate=44100):
    """Wood plank footsteps with hollow acoustic cavity."""
    duration = 0.26
    n = int(duration * sample_rate)
    samples = [0.0] * n
    base_freq = 110.0 + var_idx * 18.0
    for i in range(n):
        t = i / sample_rate
        env = math.exp(-24.0 * t)
        thud = math.sin(2 * math.pi * base_freq * t) * 0.7
        creak = math.sin(2 * math.pi * (base_freq * 3.2) * t) * 0.3
        tap = random.uniform(-0.4, 0.4) * math.exp(-90.0 * t)
        samples[i] = (thud + creak + tap) * env * 18000.0
    return samples

def gen_footstep_surface_ext(surface='dirt', var_idx=3, sample_rate=44100):
    """Generates variations 3 and 4 for realistic ground footsteps."""
    duration = 0.28
    n = int(duration * sample_rate)
    samples = [0.0] * n
    freq_map = {'dirt': 130.0, 'grass': 260.0, 'stone': 340.0, 'sand': 190.0, 'snow': 220.0, 'water': 170.0}
    f = freq_map.get(surface, 150.0) + (var_idx * 15.0)
    for i in range(n):
        t = i / sample_rate
        env = math.exp(-22.0 * t)
        base = math.sin(2 * math.pi * f * t) * 0.6
        crunch = random.uniform(-0.8, 0.8) * math.exp(-40.0 * t) * 0.4
        samples[i] = (base + crunch) * env * 16000.0
    return samples

def build_all():
    print("Synthesizing Advanced Foley & Audio Assets...")
    write_wav('rain_ambient.wav', gen_rain_ambient())
    write_wav('rain_roof.wav', gen_rain_roof())
    write_wav('thunder_distant.wav', gen_thunder_distant())
    write_wav('thunder_close.wav', gen_thunder_close())
    write_wav('meat_sizzle.wav', gen_meat_sizzle())
    write_wav('metal_quench.wav', gen_metal_quench())
    write_wav('heavy_panting.wav', gen_heavy_panting())
    write_wav('yawn.wav', gen_yawn())
    write_wav('shiver.wav', gen_shiver())
    write_wav('gear_rustle.wav', gen_gear_rustle())
    write_wav('baby_coo.wav', gen_baby_coo())
    write_wav('whistle.wav', gen_whistle())
    write_wav('dog_bark.wav', gen_dog_bark())
    write_wav('dog_whimper.wav', gen_dog_whimper())
    write_wav('animal_graze.wav', gen_animal_graze())
    write_wav('animal_alert.wav', gen_animal_alert())

    # Footstep multi-samples
    for i in range(1, 5):
        write_wav(f'footstep_wood_{i}.wav', gen_footstep_wood(i))
    for s in ['dirt', 'grass', 'stone', 'sand', 'snow', 'water']:
        for i in [3, 4]:
            write_wav(f'footstep_{s}_{i}.wav', gen_footstep_surface_ext(s, i))

    print("All 23 new tactile Foley sound files generated successfully!")

if __name__ == '__main__':
    build_all()
