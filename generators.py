import random
from templates import (
    INDEX_TEMPLATE,
    REDIRECT_TEMPLATE,
    CONFIG_TEMPLATE,
    PALLADIUM_TEMPLATE
)

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
        'green': {
            'primary': '#064e3b',
            'secondary': '#047857',
            'accent': '#34d399',
            'text': '#a7f3d0'
        },
        'red': {
            'primary': '#7f1d1d',
            'secondary': '#991b1b',
            'accent': '#f87171',
            'text': '#fecaca'
        },
        'dark': {
            'primary': '#18181b',
            'secondary': '#27272a',
            'accent': '#a1a1aa',
            'text': '#d4d4d8'
        }
    }
    return schemes.get(theme) or random.choice(list(schemes.values()))

def generate_unique_names():
    prefixes = ['Nexus', 'Vortex', 'Cyber', 'Meta', 'Ultra', 'Hyper', 'Prime', 'Elite']
    suffixes = ['Play', 'Games', 'Zone', 'Hub', 'Verse', 'World', 'Arena', 'Space']
    
    names = []
    used_prefixes = set()
    used_suffixes = set()
    
    for _ in range(6):
        while True:
            prefix = random.choice(prefixes)
            suffix = random.choice(suffixes)
            if prefix not in used_prefixes and suffix not in used_suffixes:
                names.append(f"{prefix}{suffix}")
                used_prefixes.add(prefix)
                used_suffixes.add(suffix)
                break
    
    return names

def generate_index(theme=None):
    colors = get_color_scheme(theme)
    names = generate_unique_names()
    
    return INDEX_TEMPLATE.format(
        primary_color=colors['primary'],
        secondary_color=colors['secondary'],
        accent_color=colors['accent'],
        text_color=colors['text'],
        game1_name=names[0],
        game2_name=names[1],
        game3_name=names[2],
        game4_name=names[3],
        game5_name=names[4],
        game6_name=names[5]
    )

def generate_redirect():
    return REDIRECT_TEMPLATE

def generate_config():
    return CONFIG_TEMPLATE

def get_palladium_template():
    return PALLADIUM_TEMPLATE 