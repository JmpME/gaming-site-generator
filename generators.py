import random

def get_color_scheme(theme=None):
    schemes = {
        'purple': {
            'primary': '#1e1b4b',
            'secondary': '#3730a3',
            'accent': '#818cf8',
            'text': '#c7d2fe'
        },
        'blue': {
            'primary': '#1e3a8a',
            'secondary': '#1d4ed8',
            'accent': '#60a5fa',
            'text': '#bfdbfe'
        },
        'cyber': {
            'primary': '#0f172a',
            'secondary': '#1e293b',
            'accent': '#38bdf8',
            'text': '#7dd3fc'
        },
        'neon': {
            'primary': '#18181b',
            'secondary': '#27272a',
            'accent': '#22d3ee',
            'text': '#67e8f9'
        },
        'sunset': {
            'primary': '#7c2d12',
            'secondary': '#9a3412',
            'accent': '#fb923c',
            'text': '#fed7aa'
        },
        'forest': {
            'primary': '#064e3b',
            'secondary': '#065f46',
            'accent': '#34d399',
            'text': '#a7f3d0'
        },
        'cherry': {
            'primary': '#881337',
            'secondary': '#9f1239',
            'accent': '#fb7185',
            'text': '#fecdd3'
        },
        'midnight': {
            'primary': '#1e1b4b',
            'secondary': '#312e81',
            'accent': '#6366f1',
            'text': '#a5b4fc'
        },
        'aurora': {
            'primary': '#0f766e',
            'secondary': '#0d9488',
            'accent': '#2dd4bf',
            'text': '#99f6e4'
        },
        'volcano': {
            'primary': '#7f1d1d',
            'secondary': '#991b1b',
            'accent': '#f87171',
            'text': '#fecaca'
        },
        'galaxy': {
            'primary': '#2e1065',
            'secondary': '#4c1d95',
            'accent': '#a855f7',
            'text': '#e9d5ff'
        },
        'ocean': {
            'primary': '#0c4a6e',
            'secondary': '#0369a1',
            'accent': '#38bdf8',
            'text': '#bae6fd'
        }
    }
    return schemes.get(theme) or random.choice(list(schemes.values()))

def generate_unique_names():
    prefixes = ['Nexus', 'Vortex', 'Cyber', 'Meta', 'Ultra']
    suffixes = ['Play', 'Games', 'Zone', 'Hub', 'Verse']
    
    names = []
    used_prefixes = set()
    used_suffixes = set()
    
    for _ in range(4):
        while True:
            prefix = random.choice(prefixes)
            suffix = random.choice(suffixes)
            if prefix not in used_prefixes and suffix not in used_suffixes:
                names.append(f"{prefix}{suffix}")
                used_prefixes.add(prefix)
                used_suffixes.add(suffix)
                break
    
    return names 