"""
Journey of Mankind - High-Fidelity Realistic Procedural Audio Synthesizer
Generates ultra-realistic multi-layer acoustic physical footsteps, map-specific 3D ambiances,
real human vocalizations, and UI earcons using Python's standard library.
"""

import os
import wave
import struct
import math
import random

SAMPLE_RATE = 44100

def _write_wav(filename, samples, sample_rate=SAMPLE_RATE, channels=1):
    """Write float samples (-1.0 to 1.0) to a 16-bit PCM WAV file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        raw_data = bytearray()
        for s in samples:
            val = max(-32767, min(32767, int(s * 32767)))
            raw_data.extend(struct.pack('<h', val))
        wav_file.writeframes(raw_data)

# ==============================================================================
# 1. ULTRA-REALISTIC MULTI-LAYER PHYSICAL FOOTSTEPS (LEFT & RIGHT VARIATIONS)
# ==============================================================================

def generate_step_dirt(path, seed=1):
    random.seed(seed)
    duration = 0.22
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    pink = 0.0
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        thump = 0.0
        if t < 0.08:
            env_thump = math.exp(-38.0 * t)
            freq = 75.0 * math.exp(-22.0 * t) + 45.0
            thump = 0.65 * math.sin(2 * math.pi * freq * t) * env_thump
            
        white = random.random() * 2.0 - 1.0
        pink = 0.85 * pink + 0.15 * white
        bursts = (math.sin(2 * math.pi * 65 * t) ** 2) * (random.random() * 0.5 + 0.5)
        env_crunch = math.exp(-18.0 * max(0.0, t - 0.02)) if t >= 0.02 else t / 0.02
        crunch = pink * 0.45 * bursts * env_crunch
        
        res = 0.22 * math.sin(2 * math.pi * 140 * t) * math.exp(-22.0 * t)
        val = thump + crunch + res
        samples.append(max(-1.0, min(1.0, val)))
    _write_wav(path, samples)

def generate_step_stone(path, seed=2):
    random.seed(seed)
    duration = 0.16
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        click = 0.85 * (random.random() * 2.0 - 1.0) * math.exp(-180.0 * t) if t < 0.02 else 0.0
        env_rock = math.exp(-42.0 * t)
        res1 = 0.45 * math.sin(2 * math.pi * 380 * t) * env_rock
        res2 = 0.28 * math.sin(2 * math.pi * 920 * t) * env_rock
        grit = (random.random() * 2.0 - 1.0) * 0.18 * math.exp(-25.0 * t)
        val = click + res1 + res2 + grit
        samples.append(max(-1.0, min(1.0, val)))
    _write_wav(path, samples)

def generate_step_grass(path, seed=3):
    random.seed(seed)
    duration = 0.20
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    pink = 0.0
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        thump = 0.35 * math.sin(2 * math.pi * 70 * t) * math.exp(-30.0 * t) if t < 0.08 else 0.0
        white = random.random() * 2.0 - 1.0
        pink = 0.8 * pink + 0.2 * white
        env_swish = math.sin(math.pi * (t / duration)) ** 1.8
        swish = pink * 0.45 * env_swish
        stalk = (random.random() * 2.0 - 1.0) * 0.25 * math.exp(-25.0 * t)
        val = thump + swish + stalk
        samples.append(max(-1.0, min(1.0, val)))
    _write_wav(path, samples)

def generate_step_water(path, seed=4):
    random.seed(seed)
    duration = 0.26
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        wobble = math.sin(2 * math.pi * 45 * t)
        freq = 320.0 + 180.0 * wobble
        env_fluid = math.exp(-15.0 * t)
        fluid = 0.4 * math.sin(2 * math.pi * freq * t) * env_fluid
        spray = (random.random() * 2.0 - 1.0) * 0.38 * (1.0 - t / duration) ** 1.6
        droplets = (random.random() * 2.0 - 1.0) * 0.25 * math.sin(2 * math.pi * 1200 * t) * math.exp(-22.0 * t)
        val = fluid + spray + droplets
        samples.append(max(-1.0, min(1.0, val)))
    _write_wav(path, samples)

def generate_step_sand(path, seed=5):
    random.seed(seed)
    duration = 0.24
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    pink = 0.0
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        thump = 0.3 * math.sin(2 * math.pi * 60 * t) * math.exp(-26.0 * t) if t < 0.09 else 0.0
        white = random.random() * 2.0 - 1.0
        pink = 0.9 * pink + 0.1 * white
        env_sand = math.sin(math.pi * (t / duration)) ** 1.5
        hiss = pink * 0.4 * env_sand
        val = thump + hiss
        samples.append(max(-1.0, min(1.0, val)))
    _write_wav(path, samples)

def generate_step_snow(path, seed=6):
    random.seed(seed)
    duration = 0.20
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        squeak = 0.35 * math.sin(2 * math.pi * (520 + 280 * math.sin(2 * math.pi * 40 * t)) * t) * math.exp(-20.0 * t)
        crunch = (random.random() * 2.0 - 1.0) * 0.45 * (1.0 - t / duration) ** 2
        val = squeak + crunch
        samples.append(max(-1.0, min(1.0, val)))
    _write_wav(path, samples)

# ==============================================================================
# 2. MAP-SPECIFIC 3D ATMOSPHERIC AMBIENT SOUNDSCAPES (5 UNIQUE REALMS)
# ==============================================================================

def generate_ambience_cradle(path):
    duration = 3.0
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    pink = 0.0
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        white = random.random() * 2.0 - 1.0
        pink = 0.95 * pink + 0.05 * white
        swell = 0.4 + 0.3 * math.sin(2 * math.pi * 0.35 * t)
        wind = pink * 0.7 * swell
        chirp = 0.0
        if 0.5 < t < 0.75:
            tc = t - 0.5
            freq = 2400.0 + 800.0 * math.sin(2 * math.pi * 18 * tc)
            chirp = 0.12 * math.sin(2 * math.pi * freq * tc) * math.sin(math.pi * (tc / 0.25))
        elif 1.8 < t < 2.05:
            tc = t - 1.8
            freq = 2800.0 + 600.0 * math.sin(2 * math.pi * 22 * tc)
            chirp = 0.10 * math.sin(2 * math.pi * freq * tc) * math.sin(math.pi * (tc / 0.25))
        samples.append(max(-1.0, min(1.0, wind + chirp)))
    _write_wav(path, samples)

def generate_ambience_coastal(path):
    duration = 3.5
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    pink = 0.0
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        white = random.random() * 2.0 - 1.0
        pink = 0.92 * pink + 0.08 * white
        wave_cycle = math.sin(math.pi * (t / duration)) ** 3
        sub = 0.35 * math.sin(2 * math.pi * 48 * t) * wave_cycle
        surf = pink * 0.65 * wave_cycle
        samples.append(max(-1.0, min(1.0, sub + surf)))
    _write_wav(path, samples)

def generate_ambience_volcano(path):
    duration = 3.0
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    pink = 0.0
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        rumble = 0.55 * math.sin(2 * math.pi * (45.0 + 10.0 * math.sin(2 * math.pi * 0.8 * t)) * t)
        white = random.random() * 2.0 - 1.0
        pink = 0.9 * pink + 0.1 * white
        sizzle = pink * 0.25 * (0.6 + 0.4 * math.sin(2 * math.pi * 1.5 * t))
        samples.append(max(-1.0, min(1.0, rumble + sizzle)))
    _write_wav(path, samples)

def generate_ambience_tundra(path):
    duration = 3.0
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    pink = 0.0
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        white = random.random() * 2.0 - 1.0
        pink = 0.94 * pink + 0.06 * white
        whistle_freq = 420.0 + 260.0 * math.sin(2 * math.pi * 0.6 * t)
        whistle = 0.22 * math.sin(2 * math.pi * whistle_freq * t) * (0.5 + 0.5 * math.sin(2 * math.pi * 0.3 * t))
        wind = pink * 0.6
        samples.append(max(-1.0, min(1.0, wind + whistle)))
    _write_wav(path, samples)

def generate_ambience_cavern(path):
    duration = 3.2
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        drone = 0.35 * math.sin(2 * math.pi * 75 * t) * (0.7 + 0.3 * math.sin(2 * math.pi * 0.4 * t))
        drip = 0.0
        if 0.8 < t < 0.95:
            td = t - 0.8
            drip = 0.35 * math.sin(2 * math.pi * 1450 * td) * math.exp(-28.0 * td)
        elif 2.2 < t < 2.35:
            td = t - 2.2
            drip = 0.30 * math.sin(2 * math.pi * 1680 * td) * math.exp(-28.0 * td)
        samples.append(max(-1.0, min(1.0, drone + drip)))
    _write_wav(path, samples)

# ==============================================================================
# 3. REAL HUMAN VOCALIZATIONS
# ==============================================================================

def generate_voice_attack(path):
    duration = 0.42
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / duration)) ** 1.3
        pitch = 190.0 * math.exp(-2.5 * t) + 95.0
        vocal = 0.5 * math.sin(2 * math.pi * pitch * t) + 0.25 * math.sin(2 * math.pi * (pitch * 2) * t)
        noise = (random.random() * 2.0 - 1.0) * 0.2
        samples.append((vocal + noise) * env * 0.85)
    _write_wav(path, samples)

def generate_voice_climb(path):
    duration = 0.32
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / duration)) ** 1.5
        pitch = 110.0 + 40.0 * (1.0 - t / duration)
        vocal = 0.6 * math.sin(2 * math.pi * pitch * t)
        breath = (random.random() * 2.0 - 1.0) * 0.25
        samples.append((vocal + breath) * env * 0.75)
    _write_wav(path, samples)

def generate_voice_hurt(path):
    duration = 0.28
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        env = math.exp(-18.0 * t)
        pitch = 145.0 * math.exp(-10.0 * t) + 80.0
        vocal = 0.7 * math.sin(2 * math.pi * pitch * t)
        samples.append(vocal * env * 0.85)
    _write_wav(path, samples)

def generate_voice_pant(path):
    duration = 0.65
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    pink = 0.0
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / duration)) ** 2
        white = random.random() * 2.0 - 1.0
        pink = 0.82 * pink + 0.18 * white
        breath = pink * 0.5 * env
        samples.append(breath)
    _write_wav(path, samples)

# ==============================================================================
# 4. EARCONS, UI, AND UTILITY SOUNDS
# ==============================================================================

def generate_menu_move(path):
    duration = 0.04
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        env = (1.0 - t / duration) ** 2
        samples.append(0.3 * math.sin(2 * math.pi * 880.0 * t) * env)
    _write_wav(path, samples)

def generate_menu_select(path):
    duration = 0.15
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        freq = 523.25 if t < 0.07 else 659.25
        env = math.exp(-15 * (t % 0.075))
        samples.append(0.35 * math.sin(2 * math.pi * freq * t) * env)
    _write_wav(path, samples)

def generate_menu_back(path):
    duration = 0.14
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        freq = 659.25 if t < 0.07 else 440.0
        env = math.exp(-15 * (t % 0.07))
        samples.append(0.35 * math.sin(2 * math.pi * freq * t) * env)
    _write_wav(path, samples)

def generate_error_buzz(path):
    duration = 0.15
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        env = 1.0 - t / duration
        val = 0.3 if math.sin(2 * math.pi * 140.0 * t) > 0 else -0.3
        samples.append(val * env)
    _write_wav(path, samples)

def generate_heartbeat(path):
    duration = 0.45
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        s = 0.0
        if t < 0.14:
            tl = t
            env = math.exp(-22 * tl)
            s = 0.6 * math.sin(2 * math.pi * 55 * tl) * env
        elif 0.18 <= t < 0.32:
            td = t - 0.18
            env = math.exp(-26 * td)
            s = 0.45 * math.sin(2 * math.pi * 65 * td) * env
        samples.append(s)
    _write_wav(path, samples)

def generate_stomach_rumble(path):
    duration = 0.7
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / duration)) ** 1.5
        mod = math.sin(2 * math.pi * 18 * t)
        freq = 85.0 + 35.0 * mod
        s = 0.4 * math.sin(2 * math.pi * freq * t) * env
        samples.append(s + (random.random() * 2.0 - 1.0) * 0.08 * env)
    _write_wav(path, samples)

def generate_drink(path):
    duration = 0.35
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        env = (1.0 - t / duration) ** 1.8
        freq = 480.0 - 220.0 * (t / duration)
        sine = math.sin(2 * math.pi * freq * t) * 0.4
        samples.append((sine + (random.random() * 2.0 - 1.0) * 0.12) * env)
    _write_wav(path, samples)

def generate_eat(path):
    duration = 0.32
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        burst = math.sin(2 * math.pi * 12 * t) ** 4
        samples.append((random.random() * 2.0 - 1.0) * 0.45 * burst * (1.0 - t / duration))
    _write_wav(path, samples)

def generate_flint_strike(path):
    duration = 0.22
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        spark = (random.random() * 2.0 - 1.0) * 0.5 * math.exp(-28 * t)
        ring = 0.25 * math.sin(2 * math.pi * 1750 * t) * math.exp(-12 * t)
        samples.append(spark + ring)
    _write_wav(path, samples)

def generate_cosmic_boom(path):
    duration = 2.0
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        env = (1.0 - t / duration) ** 1.2
        freq = 110.0 * math.exp(-1.5 * t) + 30.0
        sine = 0.6 * math.sin(2 * math.pi * freq * t)
        noise = (random.random() * 2.0 - 1.0) * 0.25 * (1.0 - t / duration)
        samples.append((sine + noise) * env)
    _write_wav(path, samples)

def generate_climb_up(path):
    duration = 0.28
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        freq = 120.0 + 260.0 * (t / duration)
        env = math.sin(math.pi * (t / duration)) ** 1.2
        samples.append((0.35 * math.sin(2 * math.pi * freq * t) + (random.random() * 2.0 - 1.0) * 0.4) * env)
    _write_wav(path, samples)

def generate_climb_down(path):
    duration = 0.28
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        freq = 340.0 - 220.0 * (t / duration)
        env = math.sin(math.pi * (t / duration)) ** 1.2
        samples.append((0.3 * math.sin(2 * math.pi * freq * t) + (random.random() * 2.0 - 1.0) * 0.45) * env)
    _write_wav(path, samples)

def generate_turn_direction(path):
    duration = 0.07
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        samples.append((random.random() * 2.0 - 1.0) * 0.35 * ((1.0 - t / duration) ** 2))
    _write_wav(path, samples)

def generate_craft_weapon(path):
    duration = 0.4
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        clack1 = (random.random() * 2.0 - 1.0) * 0.5 * math.exp(-30 * t)
        clack2 = (random.random() * 2.0 - 1.0) * 0.5 * math.exp(-25 * max(0.0, t - 0.15)) if t >= 0.15 else 0.0
        chime = 0.25 * math.sin(2 * math.pi * 1200 * t) * math.exp(-30 * t)
        samples.append(clack1 + clack2 + chime)
    _write_wav(path, samples)

def generate_weapon_swing(path):
    duration = 0.18
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / duration)) ** 2
        freq = 420.0 - 250.0 * (t / duration)
        samples.append(((random.random() * 2.0 - 1.0) * 0.4 + math.sin(2 * math.pi * freq * t) * 0.2) * env)
    _write_wav(path, samples)

def generate_weapon_hit(path):
    duration = 0.2
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        env = math.exp(-22 * t)
        freq = 140.0 * math.exp(-15 * t)
        samples.append((0.6 * math.sin(2 * math.pi * freq * t) + (random.random() * 2.0 - 1.0) * 0.35) * env)
    _write_wav(path, samples)

def generate_predator_growl(path):
    duration = 0.85
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / duration)) ** 1.4
        mod = math.sin(2 * math.pi * 28 * t)
        freq = 75.0 + 35.0 * mod
        rumble = 0.45 * math.sin(2 * math.pi * freq * t)
        snarl = (random.random() * 2.0 - 1.0) * 0.25 * (0.5 + 0.5 * mod)
        samples.append((rumble + snarl) * env)
    _write_wav(path, samples)

def generate_mammoth_trumpet(path):
    duration = 1.1
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / duration)) ** 1.3
        pitch_slide = 180.0 + 90.0 * math.sin(math.pi * (t / duration))
        h1 = 0.5 * math.sin(2 * math.pi * pitch_slide * t)
        h2 = 0.25 * math.sin(2 * math.pi * (pitch_slide * 2) * t)
        samples.append((h1 + h2) * env)
    _write_wav(path, samples)

def generate_wolf_howl(path):
    duration = 1.2
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / duration)) ** 1.5
        freq = 280.0 + 160.0 * math.sin(math.pi * (t / duration))
        samples.append(0.5 * math.sin(2 * math.pi * freq * t) * env)
    _write_wav(path, samples)

def generate_bag_open(path):
    duration = 0.2
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / duration)) ** 1.5
        noise = (random.random() * 2.0 - 1.0) * 0.25
        chime = 0.15 * math.sin(2 * math.pi * (440 + 330 * (t / duration)) * t)
        samples.append((noise + chime) * env)
    _write_wav(path, samples)

def generate_bag_close(path):
    duration = 0.16
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        env = (1.0 - t / duration) ** 2
        noise = (random.random() * 2.0 - 1.0) * 0.35 * env
        thump = 0.3 * math.sin(2 * math.pi * 160 * t) * env
        samples.append(noise + thump)
    _write_wav(path, samples)

def generate_sonar_beep(path):
    duration = 0.08
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        samples.append(0.45 * math.sin(2 * math.pi * 1350.0 * t) * math.exp(-35 * t))
    _write_wav(path, samples)

def generate_item_found(path):
    duration = 0.28
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        if t < 0.09:
            freq = 659.25
            tl = t
        elif t < 0.18:
            freq = 880.00
            tl = t - 0.09
        else:
            freq = 1174.66
            tl = t - 0.18
        samples.append(0.4 * math.sin(2 * math.pi * freq * t) * math.exp(-18 * tl))
    _write_wav(path, samples)

def generate_travel_whoosh(path):
    duration = 0.8
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / duration)) ** 1.3
        freq = 80.0 + 180.0 * math.sin(math.pi * (t / duration))
        sub = 0.5 * math.sin(2 * math.pi * freq * t)
        noise = (random.random() * 2.0 - 1.0) * 0.35 * (1.0 - 0.5 * (t / duration))
        samples.append((sub + noise) * env)
    _write_wav(path, samples)

def generate_all_sounds(target_dir):
    """Ensures all essential sound effects, footsteps, ambiances, and voices are generated."""
    os.makedirs(target_dir, exist_ok=True)
    sound_map = {
        # Realistic Multi-Surface Footsteps (Variations)
        'footstep_dirt.wav': lambda p: generate_step_dirt(p, 10),
        'footstep_dirt_1.wav': lambda p: generate_step_dirt(p, 11),
        'footstep_dirt_2.wav': lambda p: generate_step_dirt(p, 12),
        
        'footstep_stone.wav': lambda p: generate_step_stone(p, 20),
        'footstep_stone_1.wav': lambda p: generate_step_stone(p, 21),
        'footstep_stone_2.wav': lambda p: generate_step_stone(p, 22),
        
        'footstep_grass.wav': lambda p: generate_step_grass(p, 30),
        'footstep_grass_1.wav': lambda p: generate_step_grass(p, 31),
        'footstep_grass_2.wav': lambda p: generate_step_grass(p, 32),
        
        'footstep_water.wav': lambda p: generate_step_water(p, 40),
        'footstep_water_1.wav': lambda p: generate_step_water(p, 41),
        'footstep_water_2.wav': lambda p: generate_step_water(p, 42),
        
        'footstep_sand.wav': lambda p: generate_step_sand(p, 50),
        'footstep_sand_1.wav': lambda p: generate_step_sand(p, 51),
        'footstep_sand_2.wav': lambda p: generate_step_sand(p, 52),
        
        'footstep_snow.wav': lambda p: generate_step_snow(p, 60),
        'footstep_snow_1.wav': lambda p: generate_step_snow(p, 61),
        'footstep_snow_2.wav': lambda p: generate_step_snow(p, 62),

        # 5 Map-Specific Atmospheric Ambiances
        'ambience_cradle.wav': generate_ambience_cradle,
        'ambience_coastal.wav': generate_ambience_coastal,
        'ambience_volcano.wav': generate_ambience_volcano,
        'ambience_tundra.wav': generate_ambience_tundra,
        'ambience_cavern.wav': generate_ambience_cavern,
        'wind_ambient.wav': generate_ambience_cradle,

        # Real Human Vocalizations
        'voice_attack.wav': generate_voice_attack,
        'voice_climb.wav': generate_voice_climb,
        'voice_hurt.wav': generate_voice_hurt,
        'voice_pant.wav': generate_voice_pant,

        # UI, Bag, Sonar, Crafting & Beasts
        'menu_move.wav': generate_menu_move,
        'menu_select.wav': generate_menu_select,
        'menu_back.wav': generate_menu_back,
        'error_buzz.wav': generate_error_buzz,
        'heartbeat.wav': generate_heartbeat,
        'stomach_rumble.wav': generate_stomach_rumble,
        'drink.wav': generate_drink,
        'eat.wav': generate_eat,
        'flint_strike.wav': generate_flint_strike,
        'cosmic_boom.wav': generate_cosmic_boom,
        'climb_up.wav': generate_climb_up,
        'climb_down.wav': generate_climb_down,
        'turn_direction.wav': generate_turn_direction,
        'craft_weapon.wav': generate_craft_weapon,
        'weapon_swing.wav': generate_weapon_swing,
        'weapon_hit.wav': generate_weapon_hit,
        'predator_growl.wav': generate_predator_growl,
        'mammoth_trumpet.wav': generate_mammoth_trumpet,
        'wolf_howl.wav': generate_wolf_howl,
        'bag_open.wav': generate_bag_open,
        'bag_close.wav': generate_bag_close,
        'sonar_beep.wav': generate_sonar_beep,
        'item_found.wav': generate_item_found,
        'travel_whoosh.wav': generate_travel_whoosh,
    }
    
    for filename, generator in sound_map.items():
        file_path = os.path.join(target_dir, filename)
        if not os.path.exists(file_path):
            generator(file_path)

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sounds_dir = os.path.join(script_dir, '..', 'sounds')
    print("Synthesizing realistic audio suite...")
    generate_all_sounds(sounds_dir)
    print("Realistic audio suite complete!")
