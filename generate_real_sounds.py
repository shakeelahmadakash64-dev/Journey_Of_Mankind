"""
Generate Ultra-Realistic Tactile Audio for Journey of Mankind:
- bag_open.wav: Authentic tactile Zipper Open (pull-tab click, 180-300 teeth/sec asymmetric shock pulses, runner cavity resonance, canvas friction, fabric release)
- bag_close.wav: Authentic tactile Zipper Close (teeth interlocking ratcheting buzz, runner drag, canvas tension, solid metal end-stop latch snap)
- door_open.wav: Prehistoric timber/thatch shelter door latch lift, deep wood hinge creak, swing open
- door_close.wav: Prehistoric timber shelter door swing, solid frame impact thud, latch lock shut
- page_turn.wav: Crisp paper/parchment textbook page flipping rustle
- shelter_enter.wav: Dry reed canopy brushing, sheltered interior entry
- shelter_exit.wav: Stepping out from reed lean-to into open wilderness
- ambience_shelter.wav: Seamless looping sheltered interior ambience (muffled wind outside, warm hearth embers)
"""

import wave
import struct
import math
import random
import os

SOUNDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sounds')

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
    print(f"Generated {filename} ({len(samples)} frames, {len(samples)/sample_rate:.2f}s)")

def generate_zipper_open(sample_rate=44100):
    """
    Generates authentic tactile zipper open sound.
    Combines metal pull-tab contact, dense asymmetric tooth release impulses (180-300 teeth/sec),
    runner cavity resonance, canvas friction, pull-tab micro-rattle, and fabric opening release.
    """
    duration = 0.42
    n_samples = int(duration * sample_rate)
    samples = [0.0] * n_samples

    # 1. Initial pull-tab touch / click (t = 0.015s)
    tab_init = int(0.015 * sample_rate)
    for j in range(int(0.008 * sample_rate)):
        dt = j / sample_rate
        click = (math.sin(2 * math.pi * 4800.0 * dt) * 0.7 + math.sin(2 * math.pi * 6400.0 * dt) * 0.3) * math.exp(-500.0 * dt)
        samples[tab_init + j] += click * 8000.0

    # 2. Dense Teeth ratcheting (t = 0.03s to 0.35s)
    zip_start = int(0.03 * sample_rate)
    zip_end = int(0.35 * sample_rate)
    zip_dur = zip_end - zip_start

    t_curr = zip_start
    while t_curr < zip_end:
        rel = (t_curr - zip_start) / zip_dur
        rate = 180.0 + 120.0 * math.sin(math.pi * rel)
        idx = int(t_curr)

        f_res = 3600.0 + 900.0 * (rel ** 0.8) + random.uniform(-120, 120)
        f_harm = f_res * 1.75
        decay = 420.0
        tooth_len = int(0.006 * sample_rate)

        for j in range(tooth_len):
            si = idx + j
            if si >= n_samples: break
            dt = j / sample_rate
            pulse = (math.sin(2 * math.pi * f_res * dt) * 0.65 + 
                     math.sin(2 * math.pi * f_harm * dt) * 0.25 + 
                     (random.random() * 2 - 1) * 0.3) * math.exp(-decay * dt)
            samples[si] += pulse * 13500.0

        f_cav = 1950.0 + random.uniform(-40, 40)
        for j in range(int(0.007 * sample_rate)):
            si = idx + j
            if si >= n_samples: break
            dt = j / sample_rate
            cav = math.sin(2 * math.pi * f_cav * dt) * math.exp(-280.0 * dt)
            samples[si] += cav * 4200.0

        step = (sample_rate / rate) * (1.0 + random.uniform(-0.05, 0.05))
        t_curr += step

    # 3. Continuous tape friction & slider hiss
    for i in range(zip_start, min(zip_end, n_samples)):
        rel = (i - zip_start) / zip_dur
        env = math.sin(math.pi * rel) ** 1.3
        fric = (random.random() * 2 - 1) * 0.65
        body = math.sin(2 * math.pi * 1400.0 * (i / sample_rate)) * 0.25
        samples[i] += (fric + body) * env * 4800.0

    # 4. Pull-tab micro-rattle jingles
    rattle_times = [0.08, 0.16, 0.24, 0.31]
    for rt in rattle_times:
        start_j = int(rt * sample_rate)
        for j in range(int(0.007 * sample_rate)):
            si = start_j + j
            if si >= n_samples: break
            dt = j / sample_rate
            jingle = math.sin(2 * math.pi * 5800.0 * dt) * math.exp(-550.0 * dt)
            samples[si] += jingle * 5000.0

    # 5. Soft cloth opening release flap (t = 0.32s to 0.41s)
    for i in range(int(0.32 * sample_rate), n_samples):
        dt = (i - int(0.32 * sample_rate)) / sample_rate
        env = math.sin(math.pi * min(1.0, dt / 0.09)) ** 1.5
        cloth = (random.random() * 2 - 1) * 0.4
        samples[i] += cloth * env * 3500.0

    for i in range(n_samples):
        if i < 150: samples[i] *= (i / 150.0)
        elif i > n_samples - 300: samples[i] *= ((n_samples - i) / 300.0)

    return samples

def generate_zipper_close(sample_rate=44100):
    """
    Generates authentic tactile zipper close sound.
    Teeth interlocking ratcheting buzz, runner drag, canvas tension, ending with a solid metal end-stop latch snap.
    """
    duration = 0.45
    n_samples = int(duration * sample_rate)
    samples = [0.0] * n_samples

    # 1. Pull start click
    tab_init = int(0.015 * sample_rate)
    for j in range(int(0.008 * sample_rate)):
        dt = j / sample_rate
        click = math.sin(2 * math.pi * 4600.0 * dt) * math.exp(-480.0 * dt)
        samples[tab_init + j] += click * 7000.0

    # 2. Teeth interlocking ratcheting buzz (t = 0.03s to 0.33s)
    zip_start = int(0.03 * sample_rate)
    zip_end = int(0.33 * sample_rate)
    zip_dur = zip_end - zip_start

    t_curr = zip_start
    while t_curr < zip_end:
        rel = (t_curr - zip_start) / zip_dur
        rate = 170.0 + 110.0 * math.sin(math.pi * rel)
        idx = int(t_curr)

        f_res = 3200.0 + 600.0 * rel + random.uniform(-100, 100)
        f_harm = f_res * 1.6
        decay = 400.0
        tooth_len = int(0.006 * sample_rate)

        for j in range(tooth_len):
            si = idx + j
            if si >= n_samples: break
            dt = j / sample_rate
            pulse = (math.sin(2 * math.pi * f_res * dt) * 0.7 + 
                     math.sin(2 * math.pi * f_harm * dt) * 0.25 + 
                     (random.random() * 2 - 1) * 0.3) * math.exp(-decay * dt)
            samples[si] += pulse * 12500.0

        f_cav = 1850.0 + random.uniform(-40, 40)
        for j in range(int(0.007 * sample_rate)):
            si = idx + j
            if si >= n_samples: break
            dt = j / sample_rate
            cav = math.sin(2 * math.pi * f_cav * dt) * math.exp(-270.0 * dt)
            samples[si] += cav * 4000.0

        step = (sample_rate / rate) * (1.0 + random.uniform(-0.05, 0.05))
        t_curr += step

    # 3. Canvas friction
    for i in range(zip_start, min(zip_end, n_samples)):
        rel = (i - zip_start) / zip_dur
        env = math.sin(math.pi * rel) ** 1.3
        fric = (random.random() * 2 - 1) * 0.6
        body = math.sin(2 * math.pi * 1250.0 * (i / sample_rate)) * 0.25
        samples[i] += (fric + body) * env * 4500.0

    # 4. Pull-tab rattles
    rattle_times = [0.09, 0.18, 0.26]
    for rt in rattle_times:
        start_j = int(rt * sample_rate)
        for j in range(int(0.007 * sample_rate)):
            si = start_j + j
            if si >= n_samples: break
            dt = j / sample_rate
            jingle = math.sin(2 * math.pi * 5600.0 * dt) * math.exp(-500.0 * dt)
            samples[si] += jingle * 4500.0

    # 5. Solid Stopper Clack / Metal Lock at t = 0.34s
    stop_start = int(0.34 * sample_rate)
    stop_len = int(0.09 * sample_rate)
    for j in range(stop_len):
        si = stop_start + j
        if si >= n_samples: break
        dt = j / sample_rate
        env_snap = math.exp(-dt * 110.0)
        env_thud = math.exp(-dt * 45.0)
        snap = (math.sin(2 * math.pi * 2600.0 * dt) * 0.6 + 
                math.sin(2 * math.pi * 4200.0 * dt) * 0.4 + 
                (random.random() * 2 - 1) * 0.4) * env_snap
        thud = math.sin(2 * math.pi * 160.0 * dt) * env_thud * 0.7
        samples[si] += (snap + thud) * 17500.0

    for i in range(n_samples):
        if i < 150: samples[i] *= (i / 150.0)
        elif i > n_samples - 300: samples[i] *= ((n_samples - i) / 300.0)

    return samples

def generate_door_open(sample_rate=44100):
    """
    Generates realistic heavy wooden/thatch shelter door opening:
    1. Latch lift click / release
    2. Deep wooden hinge creak as door swings
    3. Air draft whoosh
    """
    duration = 0.55
    n_samples = int(duration * sample_rate)
    samples = [0.0] * n_samples

    # 1. Latch lift click at t = 0.03s
    latch_start = int(0.03 * sample_rate)
    for i in range(latch_start, min(latch_start + int(0.04 * sample_rate), n_samples)):
        dt = (i - latch_start) / sample_rate
        env = math.exp(-dt * 120.0)
        click = (math.sin(2 * math.pi * 1800.0 * dt) * 0.7 + 
                 math.sin(2 * math.pi * 3200.0 * dt) * 0.4 + 
                 (random.random() * 2 - 1) * 0.4) * env
        samples[i] += click * 17000.0

    # 2. Wood hinge creak from t = 0.08s to 0.45s
    creak_start = int(0.08 * sample_rate)
    creak_len = int(0.36 * sample_rate)
    for i in range(creak_start, min(creak_start + creak_len, n_samples)):
        rel = (i - creak_start) / creak_len
        env = math.sin(math.pi * rel) ** 1.3
        f_creak = 320.0 + 140.0 * rel + 35.0 * math.sin(i * 0.04)
        harm = f_creak * 2.1
        noise = (random.random() * 2 - 1) * 0.3
        tone = math.sin(2 * math.pi * f_creak * (i / sample_rate)) * 0.7 + math.sin(2 * math.pi * harm * (i / sample_rate)) * 0.3
        samples[i] += (tone + noise) * env * 13500.0

    # 3. Air draft whoosh as door swings
    for i in range(int(0.15 * sample_rate), n_samples):
        dt = (i - int(0.15 * sample_rate)) / sample_rate
        env = math.sin(math.pi * min(1.0, dt / 0.35)) ** 2
        draft = (random.random() * 2 - 1) * 0.5 * env
        samples[i] += draft * 4500.0

    for i in range(n_samples):
        if i < 150: samples[i] *= (i / 150.0)
        elif i > n_samples - 300: samples[i] *= ((n_samples - i) / 300.0)

    return samples

def generate_door_close(sample_rate=44100):
    """
    Generates realistic heavy wooden/thatch shelter door closing:
    1. Door swing draft
    2. Solid timber door frame impact thud / slam
    3. Latch catching & locking shut
    """
    duration = 0.50
    n_samples = int(duration * sample_rate)
    samples = [0.0] * n_samples

    # 1. Door swing motion air draft (t = 0.0 to 0.22s)
    draft_len = int(0.22 * sample_rate)
    for i in range(draft_len):
        rel = i / draft_len
        env = math.sin(math.pi * rel) ** 2
        draft = (random.random() * 2 - 1) * 0.6 * env
        samples[i] += draft * 5500.0

    # 2. Solid wood door frame impact slam / thud at t = 0.21s
    slam_start = int(0.21 * sample_rate)
    slam_len = int(0.25 * sample_rate)
    for i in range(slam_start, min(slam_start + slam_len, n_samples)):
        dt = (i - slam_start) / sample_rate
        env_thud = math.exp(-dt * 35.0)
        env_slap = math.exp(-dt * 90.0)
        thud = (math.sin(2 * math.pi * 92.0 * dt) * 0.7 + math.sin(2 * math.pi * 145.0 * dt) * 0.4) * env_thud
        slap = (math.sin(2 * math.pi * 580.0 * dt) * 0.4 + (random.random() * 2 - 1) * 0.5) * env_slap
        samples[i] += (thud + slap) * 19000.0

    # 3. Latch catching & locking shut at t = 0.25s
    latch_start = int(0.25 * sample_rate)
    latch_len = int(0.12 * sample_rate)
    for i in range(latch_start, min(latch_start + latch_len, n_samples)):
        dt = (i - latch_start) / sample_rate
        env_latch = math.exp(-dt * 85.0)
        latch = (math.sin(2 * math.pi * 2200.0 * dt) * 0.6 + 
                 math.sin(2 * math.pi * 3400.0 * dt) * 0.4 + 
                 (random.random() * 2 - 1) * 0.4) * env_latch
        samples[i] += latch * 13000.0

    for i in range(n_samples):
        if i < 150: samples[i] *= (i / 150.0)
        elif i > n_samples - 300: samples[i] *= ((n_samples - i) / 300.0)

    return samples

def generate_page_turn(sample_rate=44100):
    duration = 0.42
    n_samples = int(duration * sample_rate)
    samples = [0.0] * n_samples

    for i in range(n_samples):
        t = i / sample_rate
        t_rel = i / n_samples
        env = (t_rel ** 0.6) * ((1.0 - t_rel) ** 1.4) * 4.5
        mod = 1.0 + 0.4 * math.sin(2 * math.pi * 28.0 * t)
        noise = (random.random() * 2 - 1)
        tone1 = 0.3 * math.sin(2 * math.pi * 1250.0 * t)
        tone2 = 0.2 * math.sin(2 * math.pi * 2400.0 * t)
        samples[i] = (noise + tone1 + tone2) * mod * env * 12500.0

    return samples

def generate_shelter_enter(sample_rate=44100):
    duration = 0.55
    n_samples = int(duration * sample_rate)
    samples = [0.0] * n_samples

    for i in range(n_samples):
        t = i / sample_rate
        t_rel = i / n_samples
        env = math.sin(math.pi * t_rel) ** 1.6
        brush = (random.random() * 2 - 1) * 0.8
        thatch = 0.3 * math.sin(2 * math.pi * 320.0 * t) + 0.2 * math.sin(2 * math.pi * 580.0 * t)
        samples[i] = (brush + thatch) * env * 14000.0

    step_start = int(0.18 * sample_rate)
    for i in range(step_start, min(step_start + int(0.2 * sample_rate), n_samples)):
        dt = (i - step_start) / sample_rate
        env = math.exp(-dt * 40.0)
        samples[i] += math.sin(2 * math.pi * 95.0 * dt) * env * 16000.0

    return samples

def generate_shelter_exit(sample_rate=44100):
    duration = 0.50
    n_samples = int(duration * sample_rate)
    samples = [0.0] * n_samples

    for i in range(n_samples):
        t = i / sample_rate
        t_rel = i / n_samples
        env = math.sin(math.pi * t_rel) ** 1.4
        brush = (random.random() * 2 - 1) * 0.7
        wind = 0.4 * math.sin(2 * math.pi * 220.0 * t) * (1.0 + 0.3 * math.sin(2 * math.pi * 8.0 * t))
        samples[i] = (brush + wind) * env * 13000.0

    return samples

def generate_shelter_ambience(sample_rate=44100):
    duration = 6.0
    n_samples = int(duration * sample_rate)
    base_f = 1.0 / duration
    samples = [0.0] * n_samples

    harmonics = [
        (int(55 * duration), 0.30),
        (int(75 * duration), 0.28),
        (int(105 * duration), 0.24),
        (int(145 * duration), 0.20),
        (int(190 * duration), 0.16),
        (int(240 * duration), 0.12),
        (int(310 * duration), 0.08),
        (int(390 * duration), 0.05),
    ]

    for k, amp in harmonics:
        f = k * base_f
        phase = random.random() * 2 * math.pi
        for i in range(n_samples):
            t = i / sample_rate
            mod = (1.0 + 0.35 * math.cos(2 * math.pi * (1 * base_f) * t) +
                   0.25 * math.sin(2 * math.pi * (2 * base_f) * t))
            samples[i] += math.sin(2 * math.pi * f * t + phase) * amp * mod * 5500.0

    for _ in range(30):
        k = random.randint(int(80 * duration), int(800 * duration))
        f = k * base_f
        amp = random.uniform(0.01, 0.04)
        phase = random.random() * 2 * math.pi
        k_mod = random.randint(1, 4)
        for i in range(n_samples):
            t = i / sample_rate
            mod = 1.0 + 0.35 * math.sin(2 * math.pi * (k_mod * base_f) * t)
            samples[i] += math.sin(2 * math.pi * f * t + phase) * amp * mod * 2800.0

    ember_times = [0.45, 0.90, 1.45, 2.05, 2.70, 3.35, 4.05, 4.70, 5.35]
    for et in ember_times:
        start_i = int(et * sample_rate)
        pop_len = int(0.025 * sample_rate)
        f_pop = random.uniform(1100, 2400)
        for i in range(start_i, min(start_i + pop_len, n_samples)):
            dt = (i - start_i) / sample_rate
            env = math.exp(-dt * 200.0)
            pop = (math.sin(2 * math.pi * f_pop * dt) * 0.7 + (random.random() * 2 - 1) * 0.5) * env
            samples[i] += pop * 4800.0

    creak_times = [1.7, 3.7]
    for ct in creak_times:
        start_i = int(ct * sample_rate)
        c_len = int(0.20 * sample_rate)
        for i in range(start_i, min(start_i + c_len, n_samples)):
            dt = (i - start_i) / sample_rate
            env = math.sin(math.pi * (dt / 0.20)) ** 2
            creak = (math.sin(2 * math.pi * 165.0 * dt) * 0.6 + 
                     math.sin(2 * math.pi * 210.0 * dt) * 0.4 + 
                     (random.random() * 2 - 1) * 0.3) * env
            samples[i] += creak * 3000.0

    return samples

if __name__ == '__main__':
    write_wav('bag_open.wav', generate_zipper_open())
    write_wav('bag_close.wav', generate_zipper_close())
    write_wav('door_open.wav', generate_door_open())
    write_wav('door_close.wav', generate_door_close())
    write_wav('page_turn.wav', generate_page_turn())
    write_wav('shelter_enter.wav', generate_shelter_enter())
    write_wav('shelter_exit.wav', generate_shelter_exit())
    write_wav('ambience_shelter.wav', generate_shelter_ambience())
    print("All realistic audio assets successfully created!")
