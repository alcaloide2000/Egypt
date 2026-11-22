"""Automatic part of the Spanish timeline translation: names and dates. Imported by mktl_es.py."""
import re

NAMES = [
    ("Alexander the Great", "Alejandro Magno"), ("Great Pyramid", "Gran Pirámide"), ("Great Sphinx", "Gran Esfinge"),
    ("Step Pyramid", "Pirámide escalonada"), ("Narmer Palette", "Paleta de Narmer"), ("Palermo Stone", "Piedra de Palermo"),
    ("Valley of the Kings", "Valle de los Reyes"), ("Colossi of Memnon", "Colosos de Memnón"), ("Rosetta Stone", "Piedra de Rosetta"),
    ("Tutankhamun", "Tutankamón"), ("Akhenaten", "Akenatón"), ("Nefertiti", "Nefertiti"),
    ("Khufu", "Keops"), ("Khafre", "Kefrén"), ("Menkaure", "Micerino"), ("Sneferu", "Snefru"),
    ("Thutmose", "Tutmosis"), ("Ramesses", "Ramsés"), ("Ptolemy", "Ptolomeo"), ("Senusret", "Sesostris"),
    ("Psamtik", "Psamético"), ("Necho", "Necao"), ("Cambyses", "Cambises"), ("Darius", "Darío"), ("Xerxes", "Jerjes"),
    ("Artaxerxes", "Artajerjes"), ("Merneptah", "Merenptah"), ("Twosret", "Tausert"), ("Setnakhte", "Setnajt"),
    ("Khasekhemwy", "Jasejemuy"), ("Giza", "Guiza"), ("Thebes", "Tebas"), ("Memphis", "Menfis"), ("Elephantine", "Elefantina"),
    ("Hierakonpolis", "Hieracómpolis"), ("Alexandria", "Alejandría"), ("Aswan", "Asuán"), ("Nubia", "Nubia"),
    ("Kush", "Kush"), ("Meroë", "Meroe"), ("Persian", "persa"), ("Philae", "File"), ("Sphinx", "Esfinge"),
    ("Hyksos", "hicsos"), ("Cleopatra VII", "Cleopatra VII"), ("Caesarion", "Cesarión"), ("Mark Antony", "Marco Antonio"),
    ("Octavian", "Octavio"), ("Julius Caesar", "Julio César"), ("Pompey", "Pompeyo"), ("Imhotep", "Imhotep"),
]
ROMAN = {'1': 'I', '2': 'II', '3': 'III', '4': 'IV', '5': 'V', '6': 'VI', '7': 'VII', '8': 'VIII', '9': 'IX', '10': 'X',
         '11': 'XI', '12': 'XII', '13': 'XIII', '18': 'XVIII', '19': 'XIX', '20': 'XX', '21': 'XXI', '17': 'XVII', '22': 'XXII', '23': 'XXIII', '24': 'XXIV', '25': 'XXV', '26': 'XXVI', '27': 'XXVII', '28': 'XXVIII', '29': 'XXIX', '30': 'XXX', '31': 'XXXI'}


def names(t):
    for en, es in NAMES:
        t = re.sub(r'\b' + re.escape(en) + r'\b', es, t)
    return t


def dates(t):
    # "AD 394" -> "394 d. C."; "4th c. AD" -> "s. IV d. C."
    t = re.sub(r'(\d+)(?:st|nd|rd|th) c\. AD', lambda m: f's. {ROMAN.get(m.group(1), m.group(1))} d. C.', t)
    t = re.sub(r'(\d+)(?:st|nd|rd|th) century AD', lambda m: f's. {ROMAN.get(m.group(1), m.group(1))} d. C.', t)
    t = re.sub(r'\bAD (\d[\d–\-]*)', r'\1 d. C.', t)
    t = re.sub(r'(\d[\d–\-,]*) BC\b', r'\1 a. C.', t)
    t = re.sub(r'\bc\. (?=[\d~])', 'h. ', t)
    t = re.sub(r'(\d+)(?:st|nd|rd|th) Dyn(?:asty|\.)', lambda m: f'dinastía {ROMAN.get(m.group(1), m.group(1))}', t)
    t = t.replace('–', '–')
    return t


def auto(t):
    return dates(names(t))


ENGLISH = re.compile(r"\b(the|and|of|with|to|from|by|his|her|its|in|at|for|on|as|is|was|built|reign|tomb|temple|king|queen|dies|founds|first|last|old|new|great|south|north|pyramid|until|after|before|under|son|daughter|wife|kingdom|dynasty|period|capital|city|still|active|bulls|killed|murdered|mortuary|official|royal|sun|temples|stele|campaign|battle|conquers|conquest|invades|expels|restores|moves|unifies|reunifies|statue|colossi|seat|sanctuary|chapel|court|hall|obelisk|obelisks|canal|stelae|graffiti|mercenaries|papyri|tombs|pyramids|line|ends|no|not|cult|book|books|death|born|rules|ruled|marries|exile|returns)\b", re.I)
