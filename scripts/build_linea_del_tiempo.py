"""Spanish copy of the standalone timeline: artifacts/ancient-egypt-timeline.html -> artifacts/linea-del-tiempo.html.

Run: python scripts/build_linea_del_tiempo.py. Strings in M are translated by hand; names and dates go through tl_auto.py;
the long screen-reader description lives in linea-del-tiempo-desc.es.txt and must be retranslated when tlDesc changes.
After a rebuild, check the chart for label overlaps (Spanish dates are longer) and republish."""
import re, html, sys
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from tl_auto import auto

SRC = os.path.join(ROOT, 'artifacts', 'ancient-egypt-timeline.html')
OUT = os.path.join(ROOT, 'artifacts', 'linea-del-tiempo.html')
EN_URL = 'https://claude.ai/artifact/TjdxykKbk3kF99VG1U344M'

M = {
 'Ancient Egypt History Main Points: map, cards and tour ↗': 'Página principal (en inglés): mapa, fichas y viaje ↗',
 'Upper & Lower Egypt · 3500–200 BC': 'Alto y Bajo Egipto · 3500–200 a. C.',
 'Three Thousand Years, One River': 'Tres mil años, un río',
 'The same sites and rulers, placed in time instead of space — from Predynastic Hierakonpolis to Ptolemaic Philae, with a crowded quarter-millennium of pyramid-building in between. The axis breaks where centuries pass with nothing here to show.':
  'Los mismos lugares y gobernantes, colocados en el tiempo en vez de en el espacio: de la Hieracómpolis predinástica a la File ptolemaica, con un cuarto de milenio repleto de pirámides en medio. El eje se corta donde pasan siglos sin nada que mostrar aquí.',
 'Timeline of ancient Egyptian and Kushite sites, 3500 BC to the 4th century AD': 'Línea del tiempo de lugares del antiguo Egipto y de Kush, del 3500 a. C. al siglo IV d. C.',
 'Timeline of ancient Egyptian monuments, 3500 to 200 BC': 'Línea del tiempo de monumentos del antiguo Egipto, del 3500 al 200 a. C.',
 'PREDYNASTIC': 'PREDINÁSTICO',
 'EARLY DYNASTIC & OLD KINGDOM': 'DINÁSTICO TEMPRANO Y REINO ANTIGUO',
 'MIDDLE KINGDOM': 'REINO MEDIO',
 'NEW KINGDOM': 'REINO NUEVO',
 'PTOLEMAIC': 'PTOLEMAICO',
 'PERSIAN': 'PERSA',
 '30TH DYN.': 'DIN. XXX',
 'Abydos — royal tombs': 'Abidos: tumbas reales',
 'Painted Tomb, c. 3500–3200 BC': 'Tumba pintada, h. 3500–3200 a. C.',
 'Djoser, c. 2670–2650 BC: the Step Pyramid at Saqqara': 'Djoser, h. 2670–2650 a. C.: la Pirámide escalonada de Saqqara',
 'Sneferu, c. 2613–2589 BC: Meidum and Dahshur': 'Snefru, h. 2613–2589 a. C.: Meidum y Dahshur',
 "Khufu's Great Pyramid at Giza, c. 2580–2560 BC": 'La Gran Pirámide de Keops en Guiza, h. 2580–2560 a. C.',
 'Khafre, c. 2558–2532 BC: the Second Pyramid and the Great Sphinx': 'Kefrén, h. 2558–2532 a. C.: la segunda pirámide y la Gran Esfinge',
 "Shepseskaf, c. 2503–2498 BC: the Mastabat al-Fir'aun, no pyramid": "Shepseskaf, h. 2503–2498 a. C.: la Mastabat al-Fir'aun, sin pirámide",
 'Old Kingdom pyramids': 'Pirámides del Reino Antiguo',
 'Meidum 2600 · Dahshur 2600–2570': 'Meidum 2600 · Dahshur 2600–2570',
 'Shepseskaf c. 2500 — no pyramid, reign ends the line': 'Shepseskaf h. 2500: sin pirámide, cierra la dinastía',
 'Mastaba of Ti, official (not royal), mid-5th Dyn.': 'Mastaba de Ti, un noble, mediados de la din. V',
 'Khufu dies': 'Muere Keops',
 'Sun Temples, c. 2490–2445 BC': 'Templos solares, h. 2490–2445',
 'Pepi I, c. 2321–2287 BC: pyramid at South Saqqara, whose name became Memphis': 'Pepi I, h. 2321–2287 a. C.: pirámide en Saqqara Sur, cuyo nombre se convirtió en Menfis',
 'Pepi II, c. 2278–2184 BC: the longest reign of the Old Kingdom, then the collapse': 'Pepi II, h. 2278–2184 a. C.: el reinado más largo del Reino Antiguo, y luego el hundimiento',
 "Saqqara's last pyramids, c. 2375–2167": 'Últimas pirámides de Saqqara, 2375–2167',
 'Mentuhotep II, c. 2055–2004 BC: reunifies Egypt; temple at Deir el-Bahari': 'Mentuhotep II, h. 2055–2004 a. C.: reunifica Egipto; templo en Deir el-Bahari',
 'Reunifies Egypt, c. 2055–2004 BC': 'Reunifica Egipto, h. 2055–2004 a. C.',
 'Hatshepsut, c. 1479–1458 BC: Deir el-Bahari, the Punt expedition and the Karnak obelisks': 'Hatshepsut, h. 1479–1458 a. C.: Deir el-Bahari, la expedición al Punt y los obeliscos de Karnak',
 "Amenhotep III, c. 1391–1353 BC: the Colossi of Memnon, Luxor Temple and Karnak's Third Pylon": 'Amenhotep III, h. 1391–1353 a. C.: los Colosos de Memnón, el templo de Luxor y el tercer pilono de Karnak',
 'Isis temple, 285 BC': 'Templo de Isis, 285',
 'Serapeum still active': 'Serapeum aún en uso',
 'Apis bulls, since c. 1390 BC': 'Toros Apis, desde h. 1390 a. C.',
 '116–107 and 88–81 BC': '116–107 y 88–81 a. C.',
 'killed 80 BC': 'asesinado en 80 a. C.',
 '80–58 and 55–51 BC': '80–58 y 55–51 a. C.',
 'murdered 145 BC': 'asesinado en 145 a. C.',
 'Meroë Pyramids': 'Pirámides de Meroe',
 'Kingdom of Kush, Sudan': 'Reino de Kush, Sudán',
 'Broken axis — years are to scale within each segment, not across the gaps between them. Scroll sideways to move through time.':
  'Eje cortado: los años están a escala dentro de cada tramo, no entre los huecos. Desliza hacia los lados para moverte en el tiempo.',
 'Painted Tomb (Hierakonpolis)': 'Tumba pintada (Hieracómpolis)',
 'Gebtu, colossi of Min': 'Gebtu, colosos de Min',
 'Step-to-true pyramids': 'De la pirámide escalonada a la verdadera',
 'Sneferu, Meidum and Dahshur, c. 2613–2589 BC': 'Snefru, Meidum y Dahshur, h. 2613–2589 a. C.',
 'Khafre, Second Pyramid and Sphinx, c. 2558–2532 BC': 'Kefrén, segunda pirámide y Esfinge, h. 2558–2532 a. C.',
 'Abusir, Sun Temple': 'Abusir, templo solar',
 'Pepi II, the longest reign, c. 2278–2184 BC': 'Pepi II, el reinado más largo, h. 2278–2184 a. C.',
 'Mentuhotep I (uncertain)': 'Mentuhotep I (dudoso)',
 'Middle Kingdom, c. 2055–1650 BC (shaded)': 'Reino Medio, h. 2055–1650 a. C. (sombreado)',
 'Mentuhotep II, reunifies Egypt, c. 2055–2004 BC': 'Mentuhotep II, reunifica Egipto, h. 2055–2004 a. C.',
 'Ahmose I (last pyramid)': 'Ahmose I (última pirámide)',
 'Cleopatra VII (Ptolemaic)': 'Cleopatra VII (ptolemaica)',
 'What the axis leaves out': 'Lo que el eje deja fuera',
 'Seven sites carry a second date that has nothing to do with when they were built — when the modern world found or moved them. Too recent to plot on a BC axis, so they\'re listed here instead.':
  'Siete lugares tienen una segunda fecha que no tiene nada que ver con su construcción: cuando el mundo moderno los encontró o los trasladó. Son demasiado recientes para un eje antes de Cristo, así que van aquí.',
 "Dendera's round zodiac ceiling cut out and shipped to Paris; a plaster cast stands in its place today.": 'El techo del zodiaco redondo de Dendera se recorta y se envía a París; hoy ocupa su lugar una copia de yeso.',
 "Nubkheperre Intef's gilded coffin pulled from his tomb by robbers, later bought by the British Museum.": 'Los ladrones sacan de su tumba el ataúd dorado de Nubkheperre Intef, que luego compra el Museo Británico.',
 'Palermo Stone surfaces in a private purchase in Sicily — its Egyptian findspot never recorded.': 'La Piedra de Palermo aparece en una compra privada en Sicilia; nunca se anotó dónde se encontró en Egipto.',
 'Narmer Palette excavated at Hierakonpolis, in the Main Deposit of the Temple of Horus.': 'Se excava la Paleta de Narmer en Hieracómpolis, en el Depósito Principal del templo de Horus.',
 "Abu Simbel's temples cut into 1,000+ blocks and rebuilt on higher ground, escaping Lake Nasser.": 'Los templos de Abu Simbel se cortan en más de 1.000 bloques y se reconstruyen más arriba, a salvo del lago Nasser.',
 "Philae's Temple of Isis dismantled and moved to Agilkia Island, escaping the Aswan High Dam.": 'El templo de Isis de File se desmonta y se traslada a la isla de Agilkia, a salvo de la Presa Alta de Asuán.',
 "Thutmose II's tomb found in the Western Wadis and confirmed — the first new royal tomb since 1922.": 'Se encuentra y se confirma la tumba de Tutmosis II en los uadis occidentales: la primera tumba real nueva desde 1922.',
 'Reading the cluster': 'Cómo leer el grupo',
 "Nearly everything between Djoser and Khufu happens inside 110 years. Saqqara's Step Pyramid, the small pyramid on Elephantine, Meidum, both pyramids at Dahshur, and the Great Pyramid itself — five separate building projects, one long apprenticeship in getting a pyramid's angle right, ending at Giza.":
  'Casi todo lo que pasa entre Djoser y Keops cabe en 110 años. La Pirámide escalonada de Saqqara, la pequeña pirámide de Elefantina, Meidum, las dos pirámides de Dahshur y la propia Gran Pirámide: cinco obras distintas, un largo aprendizaje para acertar con el ángulo de una pirámide, que termina en Guiza.',
 'Each linked name opens its card on the main page.': 'Cada nombre enlazado abre su ficha en la página principal (en inglés).',
 'Fort + Gisr el-Mudir, c. 2690 BC': 'Fuerte y Gisr el-Mudir, h. 2690 a. C.',
 'inscribed c. 2400 BC': 'grabada h. 2400',
 'Jump to the Fort of Khasekhemwy card': 'Ir a la ficha del fuerte de Jasejemuy',
 'Jump to the Khufu and Giza card': 'Ir a la ficha de Keops y Guiza',
 'Jump to the Pepi I and Pepi II card': 'Ir a la ficha de Pepi I y Pepi II',
 'Predynastic – 2nd Dyn. (~3400–2686 BC)': 'Predinástico – dinastía II (~3400–2686 a. C.)',
 'Userkaf c. 2494 — 5th Dynasty founder, Saqqara': 'Userkaf h. 2494, dinastía V',
 'possibly legendary, c. 2135 BC': '¿legendario?, h. 2135',
 "Khasekhemwy's enclosures": 'Recintos de Jasejemuy',
 'c. 2503–2498 BC': 'h. 2503–2498',
 '1525–1504 BC': '1525–1504',
 '1458–1425 BC': '1458–1425',
 'c. 2558–2532 BC': 'h. 2558–2532',
 '336–332 BC': '336–332',
 'c. 2112–2063 BC': 'h. 2112–2063',
}

# the long screen-reader description
M_DESC_EN = None  # filled from the source
M_DESC_ES = open(os.path.join(HERE, 'linea-del-tiempo-desc.es.txt')).read().strip()


def tr(t):
    raw = html.unescape(t)
    core = raw.strip()
    if not core:
        return t
    if core in M:
        out = M[core]
    elif M_DESC_EN and core == M_DESC_EN:
        out = M_DESC_ES
    else:
        m = re.fullmatch(r'Jump to the (.+) card', core)
        out = f'Ir a la ficha de {auto(m.group(1))}' if m else auto(core)
    lead = raw[:len(raw) - len(raw.lstrip())]; trail = raw[len(raw.rstrip()):]
    return html.escape(lead + out + trail, quote=False)


s = open(SRC).read()
i = s.index('</style>')
head, body = s[:i], s[i:]
M_DESC_EN = html.unescape(re.search(r'<desc id="tlDesc">(.*?)</desc>', body, re.S).group(1)).strip()
scripts = []
body = re.sub(r'<script.*?</script>', lambda m: scripts.append(m.group(0)) or f'@@SCRIPT{len(scripts) - 1}@@', body, flags=re.S)
# keep CSS inside later <style> blocks untouched
styles = []
body = re.sub(r'<style>.*?</style>', lambda m: styles.append(m.group(0)) or f'@@STYLE{len(styles) - 1}@@', body, flags=re.S)
body = re.sub(r'>([^<>]+)<', lambda m: '>' + tr(m.group(1)) + '<', body)
body = re.sub(r'(aria-label|title)="([^"]+)"', lambda m: f'{m.group(1)}="{html.escape(html.unescape(tr(m.group(2))), quote=True)}"', body)
for k, st in enumerate(styles):
    body = body.replace(f'@@STYLE{k}@@', st)
for k, sc in enumerate(scripts):
    body = body.replace(f'@@SCRIPT{k}@@', sc)
head = re.sub(r'<title>.*?</title>', '<title>Línea del tiempo del antiguo Egipto</title>', head)
# language link under the back link
body = body.replace('Página principal (en inglés): mapa, fichas y viaje ↗</a>',
                    f'Página principal (en inglés): mapa, fichas y viaje ↗</a>\n  <a class="tl-back" style="margin-left: 1.2rem;" href="{EN_URL}" target="_blank" rel="noopener noreferrer" hreflang="en">English version ↗</a>', 1)
# the English page links to this Spanish copy; drop that self-link here
body = re.sub(r'\n\s*<a class="tl-back"[^>]*hreflang="es">[^<]*</a>', '', body)
out = (head + body).replace('<html lang="en"', '<html lang="es"')
open(OUT, 'w').write(out)
print('ok')
