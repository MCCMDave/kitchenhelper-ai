// KitchenHelper-AI Ingredients Module

// ==================== AUTO-KATEGORIE MAPPING (500+ Zutaten) ====================
const INGREDIENT_CATEGORIES = {
    // ========== GEMÜSE ==========
    'artischocke': 'Gemüse', 'aubergine': 'Gemüse', 'avocado': 'Gemüse',
    'blumenkohl': 'Gemüse', 'bohnen': 'Gemüse', 'brokkoli': 'Gemüse', 'broccoli': 'Gemüse',
    'champignons': 'Gemüse', 'chicorée': 'Gemüse', 'chicoree': 'Gemüse', 'chinakohl': 'Gemüse',
    'erbsen': 'Gemüse', 'fenchel': 'Gemüse', 'grünkohl': 'Gemüse', 'gruenkohl': 'Gemüse',
    'gurke': 'Gemüse', 'gurken': 'Gemüse', 'karotte': 'Gemüse', 'karotten': 'Gemüse',
    'knoblauch': 'Gemüse', 'kohlrabi': 'Gemüse', 'kürbis': 'Gemüse', 'kuerbis': 'Gemüse',
    'lauch': 'Gemüse', 'mais': 'Gemüse', 'mangold': 'Gemüse',
    'möhre': 'Gemüse', 'möhren': 'Gemüse', 'moehre': 'Gemüse', 'moehren': 'Gemüse',
    'paprika': 'Gemüse', 'pastinake': 'Gemüse', 'pastinaken': 'Gemüse',
    'pilze': 'Gemüse', 'porree': 'Gemüse', 'radieschen': 'Gemüse',
    'rettich': 'Gemüse', 'romanesco': 'Gemüse', 'rosenkohl': 'Gemüse',
    'rote bete': 'Gemüse', 'rote beete': 'Gemüse', 'rotkohl': 'Gemüse',
    'rucola': 'Gemüse', 'salat': 'Gemüse', 'sauerkraut': 'Gemüse',
    'schwarzwurzel': 'Gemüse', 'sellerie': 'Gemüse', 'spargel': 'Gemüse',
    'spinat': 'Gemüse', 'spitzkohl': 'Gemüse', 'steckrübe': 'Gemüse',
    'süßkartoffel': 'Gemüse', 'suesskartoffel': 'Gemüse',
    'tomate': 'Gemüse', 'tomaten': 'Gemüse',
    'weißkohl': 'Gemüse', 'weisskohl': 'Gemüse', 'wirsing': 'Gemüse',
    'zucchini': 'Gemüse', 'zwiebel': 'Gemüse', 'zwiebeln': 'Gemüse',

    // ========== FLEISCH - Rind ==========
    'rind': 'Fleisch', 'rindfleisch': 'Fleisch', 'rindersteak': 'Fleisch',
    'rinderhüfte': 'Fleisch', 'rinderschulter': 'Fleisch', 'rinderbrust': 'Fleisch',
    'rinderfilet': 'Fleisch', 'roastbeef': 'Fleisch', 'entrecote': 'Fleisch',
    'ribeye': 'Fleisch', 'tafelspitz': 'Fleisch', 'gulasch': 'Fleisch',
    'hackfleisch': 'Fleisch', 'hack': 'Fleisch', 'rinderhack': 'Fleisch', 'tatar': 'Fleisch',

    // ========== FLEISCH - Schwein ==========
    'schwein': 'Fleisch', 'schweinefleisch': 'Fleisch', 'schweinebraten': 'Fleisch',
    'schweineschnitzel': 'Fleisch', 'schnitzel': 'Fleisch', 'schweinekotelett': 'Fleisch',
    'kotelett': 'Fleisch', 'schweinefilet': 'Fleisch', 'kasseler': 'Fleisch',
    'schweinebauch': 'Fleisch', 'bauchspeck': 'Fleisch', 'speck': 'Fleisch',
    'bacon': 'Fleisch', 'schweinehaxe': 'Fleisch', 'schweinehack': 'Fleisch',
    'bratwurst': 'Fleisch', 'wurst': 'Fleisch', 'würstchen': 'Fleisch',
    'wuerstchen': 'Fleisch', 'bockwurst': 'Fleisch', 'currywurst': 'Fleisch',

    // ========== FLEISCH - Geflügel ==========
    'hähnchen': 'Fleisch', 'haehnchen': 'Fleisch', 'huhn': 'Fleisch',
    'hähnchenbrust': 'Fleisch', 'haehnchenbrust': 'Fleisch', 'hühnerbrust': 'Fleisch',
    'hähnchenschenkel': 'Fleisch', 'hühnerkeule': 'Fleisch',
    'chicken wings': 'Fleisch', 'wings': 'Fleisch',
    'pute': 'Fleisch', 'putenbrust': 'Fleisch', 'putenschnitzel': 'Fleisch',
    'truthahn': 'Fleisch', 'ente': 'Fleisch', 'entenbrust': 'Fleisch',
    'gans': 'Fleisch', 'gänsekeule': 'Fleisch',

    // ========== FLEISCH - Wild ==========
    'wild': 'Fleisch', 'wildschwein': 'Fleisch', 'wildschweinbraten': 'Fleisch',
    'reh': 'Fleisch', 'rehkeule': 'Fleisch', 'rehbraten': 'Fleisch',
    'hirsch': 'Fleisch', 'hirschbraten': 'Fleisch', 'hirschfilet': 'Fleisch',
    'fasan': 'Fleisch', 'wachtel': 'Fleisch',

    // ========== FLEISCH - Wurst & Aufschnitt ==========
    'schinken': 'Fleisch', 'kochschinken': 'Fleisch', 'rohschinken': 'Fleisch',
    'schwarzwälder schinken': 'Fleisch', 'parmaschinken': 'Fleisch',
    'serranoschinken': 'Fleisch', 'salami': 'Fleisch', 'chorizo': 'Fleisch',
    'mortadella': 'Fleisch', 'leberwurst': 'Fleisch', 'blutwurst': 'Fleisch',
    'mettwurst': 'Fleisch', 'teewurst': 'Fleisch', 'steak': 'Fleisch',
    'lamm': 'Fleisch', 'lammfleisch': 'Fleisch', 'lammkeule': 'Fleisch',

    // ========== FISCH & MEERESFRÜCHTE ==========
    'lachs': 'Fisch', 'lachsfilet': 'Fisch', 'räucherlachs': 'Fisch',
    'thunfisch': 'Fisch', 'forelle': 'Fisch', 'regenbogenforelle': 'Fisch',
    'kabeljau': 'Fisch', 'dorsch': 'Fisch', 'seelachs': 'Fisch',
    'hering': 'Fisch', 'matjes': 'Fisch', 'makrele': 'Fisch',
    'sardine': 'Fisch', 'sardinen': 'Fisch', 'anchovis': 'Fisch',
    'pangasius': 'Fisch', 'zander': 'Fisch', 'barsch': 'Fisch',
    'dorade': 'Fisch', 'wolfsbarsch': 'Fisch', 'steinbutt': 'Fisch',
    'heilbutt': 'Fisch', 'scholle': 'Fisch', 'seezunge': 'Fisch',
    'rotbarsch': 'Fisch', 'aal': 'Fisch',
    'garnele': 'Fisch', 'garnelen': 'Fisch', 'shrimps': 'Fisch',
    'krabben': 'Fisch', 'hummer': 'Fisch', 'languste': 'Fisch',
    'tintenfisch': 'Fisch', 'calamari': 'Fisch', 'kalmar': 'Fisch', 'oktopus': 'Fisch',
    'muscheln': 'Fisch', 'miesmuscheln': 'Fisch', 'jakobsmuscheln': 'Fisch',

    // ========== MILCHPRODUKTE & KÄSE ==========
    'milch': 'Milchprodukte', 'vollmilch': 'Milchprodukte', 'frischmilch': 'Milchprodukte',
    'butter': 'Milchprodukte', 'sahne': 'Milchprodukte', 'schlagsahne': 'Milchprodukte',
    'joghurt': 'Milchprodukte', 'naturjoghurt': 'Milchprodukte', 'griechischer joghurt': 'Milchprodukte',
    'quark': 'Milchprodukte', 'magerquark': 'Milchprodukte', 'speisequark': 'Milchprodukte',
    'schmand': 'Milchprodukte', 'saure sahne': 'Milchprodukte',
    'crème fraîche': 'Milchprodukte', 'creme fraiche': 'Milchprodukte',
    'buttermilch': 'Milchprodukte', 'kefir': 'Milchprodukte',
    'käse': 'Milchprodukte', 'kaese': 'Milchprodukte',
    'frischkäse': 'Milchprodukte', 'frischkaese': 'Milchprodukte',
    'philadelphia': 'Milchprodukte', 'mascarpone': 'Milchprodukte',
    'ricotta': 'Milchprodukte', 'hüttenkäse': 'Milchprodukte',
    'camembert': 'Milchprodukte', 'brie': 'Milchprodukte',
    'mozzarella': 'Milchprodukte', 'burrata': 'Milchprodukte',
    'gouda': 'Milchprodukte', 'edamer': 'Milchprodukte', 'butterkäse': 'Milchprodukte',
    'tilsiter': 'Milchprodukte', 'leerdammer': 'Milchprodukte', 'cheddar': 'Milchprodukte',
    'parmesan': 'Milchprodukte', 'parmigiano': 'Milchprodukte',
    'pecorino': 'Milchprodukte', 'grana padano': 'Milchprodukte',
    'emmentaler': 'Milchprodukte', 'gruyère': 'Milchprodukte', 'gruyere': 'Milchprodukte',
    'bergkäse': 'Milchprodukte', 'appenzeller': 'Milchprodukte',
    'feta': 'Milchprodukte', 'schafskäse': 'Milchprodukte',
    'ziegenkäse': 'Milchprodukte', 'ziegenkaese': 'Milchprodukte',
    'halloumi': 'Milchprodukte', 'gorgonzola': 'Milchprodukte',
    'roquefort': 'Milchprodukte', 'blauschimmelkäse': 'Milchprodukte',
    'raclette': 'Milchprodukte',

    // ========== GEWÜRZE & KRÄUTER ==========
    'basilikum': 'Gewürze', 'oregano': 'Gewürze', 'thymian': 'Gewürze',
    'rosmarin': 'Gewürze', 'petersilie': 'Gewürze', 'schnittlauch': 'Gewürze',
    'dill': 'Gewürze', 'koriander': 'Gewürze', 'minze': 'Gewürze',
    'salbei': 'Gewürze', 'majoran': 'Gewürze', 'estragon': 'Gewürze',
    'bohnenkraut': 'Gewürze', 'lorbeer': 'Gewürze', 'lorbeerblätter': 'Gewürze',
    'salz': 'Gewürze', 'meersalz': 'Gewürze', 'pfeffer': 'Gewürze',
    'schwarzer pfeffer': 'Gewürze', 'weißer pfeffer': 'Gewürze',
    'cayennepfeffer': 'Gewürze', 'chili': 'Gewürze', 'chiliflocken': 'Gewürze',
    'paprikapulver': 'Gewürze', 'rosenpaprika': 'Gewürze',
    'curry': 'Gewürze', 'currypulver': 'Gewürze', 'kurkuma': 'Gewürze',
    'kreuzkümmel': 'Gewürze', 'cumin': 'Gewürze', 'kümmel': 'Gewürze',
    'zimt': 'Gewürze', 'muskat': 'Gewürze', 'muskatnuss': 'Gewürze',
    'nelken': 'Gewürze', 'gewürznelken': 'Gewürze', 'kardamom': 'Gewürze',
    'vanille': 'Gewürze', 'vanilleschote': 'Gewürze', 'anis': 'Gewürze', 'sternanis': 'Gewürze',
    'ingwer': 'Gewürze', 'safran': 'Gewürze', 'garam masala': 'Gewürze',
    'ras el hanout': 'Gewürze', 'harissa': 'Gewürze',

    // ========== KOHLENHYDRATE ==========
    'nudeln': 'Kohlenhydrate', 'pasta': 'Kohlenhydrate', 'spaghetti': 'Kohlenhydrate',
    'penne': 'Kohlenhydrate', 'fusilli': 'Kohlenhydrate', 'farfalle': 'Kohlenhydrate',
    'tagliatelle': 'Kohlenhydrate', 'fettuccine': 'Kohlenhydrate',
    'rigatoni': 'Kohlenhydrate', 'lasagneplatten': 'Kohlenhydrate',
    'gnocchi': 'Kohlenhydrate', 'tortellini': 'Kohlenhydrate', 'ravioli': 'Kohlenhydrate',
    'reis': 'Kohlenhydrate', 'basmati': 'Kohlenhydrate', 'jasminreis': 'Kohlenhydrate',
    'risottoreis': 'Kohlenhydrate', 'wildreis': 'Kohlenhydrate', 'vollkornreis': 'Kohlenhydrate',
    'kartoffel': 'Kohlenhydrate', 'kartoffeln': 'Kohlenhydrate',
    'brot': 'Kohlenhydrate', 'vollkornbrot': 'Kohlenhydrate', 'weißbrot': 'Kohlenhydrate',
    'brötchen': 'Kohlenhydrate', 'toast': 'Kohlenhydrate', 'baguette': 'Kohlenhydrate',
    'ciabatta': 'Kohlenhydrate', 'focaccia': 'Kohlenhydrate',
    'mehl': 'Kohlenhydrate', 'weizenmehl': 'Kohlenhydrate', 'dinkelmehl': 'Kohlenhydrate',
    'vollkornmehl': 'Kohlenhydrate', 'haferflocken': 'Kohlenhydrate', 'müsli': 'Kohlenhydrate',
    'couscous': 'Kohlenhydrate', 'bulgur': 'Kohlenhydrate',
    'quinoa': 'Kohlenhydrate', 'amaranth': 'Kohlenhydrate', 'hirse': 'Kohlenhydrate',
    'linsen': 'Kohlenhydrate', 'rote linsen': 'Kohlenhydrate',
    'kichererbsen': 'Kohlenhydrate', 'kidneybohnen': 'Kohlenhydrate',

    // ========== ÖLE & FETTE ==========
    'öl': 'Öle & Fette', 'oel': 'Öle & Fette',
    'olivenöl': 'Öle & Fette', 'olivenoel': 'Öle & Fette',
    'sonnenblumenöl': 'Öle & Fette', 'sonnenblumenoel': 'Öle & Fette',
    'rapsöl': 'Öle & Fette', 'rapsoel': 'Öle & Fette',
    'kokosöl': 'Öle & Fette', 'kokosoel': 'Öle & Fette',
    'sesamöl': 'Öle & Fette', 'sesamoel': 'Öle & Fette',
    'erdnussöl': 'Öle & Fette', 'walnussöl': 'Öle & Fette',
    'leinöl': 'Öle & Fette', 'kürbiskernöl': 'Öle & Fette',
    'margarine': 'Öle & Fette', 'schmalz': 'Öle & Fette', 'butterschmalz': 'Öle & Fette', 'ghee': 'Öle & Fette',

    // ========== OBST ==========
    'apfel': 'Obst', 'äpfel': 'Obst', 'aepfel': 'Obst',
    'birne': 'Obst', 'birnen': 'Obst', 'quitte': 'Obst',
    'banane': 'Obst', 'bananen': 'Obst',
    'orange': 'Obst', 'orangen': 'Obst', 'mandarine': 'Obst', 'clementine': 'Obst',
    'grapefruit': 'Obst', 'pomelo': 'Obst',
    'zitrone': 'Obst', 'zitronen': 'Obst', 'limette': 'Obst', 'limetten': 'Obst',
    'erdbeere': 'Obst', 'erdbeeren': 'Obst', 'himbeere': 'Obst', 'himbeeren': 'Obst',
    'blaubeere': 'Obst', 'blaubeeren': 'Obst', 'heidelbeeren': 'Obst',
    'brombeere': 'Obst', 'brombeeren': 'Obst', 'johannisbeeren': 'Obst',
    'kirsche': 'Obst', 'kirschen': 'Obst', 'sauerkirschen': 'Obst',
    'pfirsich': 'Obst', 'pfirsiche': 'Obst', 'nektarine': 'Obst', 'nektarinen': 'Obst',
    'aprikose': 'Obst', 'aprikosen': 'Obst', 'pflaume': 'Obst', 'pflaumen': 'Obst',
    'traube': 'Obst', 'trauben': 'Obst', 'weintrauben': 'Obst',
    'melone': 'Obst', 'wassermelone': 'Obst', 'honigmelone': 'Obst',
    'mango': 'Obst', 'papaya': 'Obst', 'ananas': 'Obst',
    'kiwi': 'Obst', 'maracuja': 'Obst', 'passionsfrucht': 'Obst',
    'granatapfel': 'Obst', 'feige': 'Obst', 'feigen': 'Obst',
    'dattel': 'Obst', 'datteln': 'Obst', 'rosinen': 'Obst',

    // ========== NÜSSE & SAMEN ==========
    'mandel': 'Nüsse & Samen', 'mandeln': 'Nüsse & Samen',
    'walnuss': 'Nüsse & Samen', 'walnüsse': 'Nüsse & Samen', 'walnuesse': 'Nüsse & Samen',
    'haselnuss': 'Nüsse & Samen', 'haselnüsse': 'Nüsse & Samen',
    'cashew': 'Nüsse & Samen', 'cashews': 'Nüsse & Samen', 'cashewnuss': 'Nüsse & Samen',
    'erdnuss': 'Nüsse & Samen', 'erdnüsse': 'Nüsse & Samen', 'erdnuesse': 'Nüsse & Samen',
    'pinienkerne': 'Nüsse & Samen', 'pistazien': 'Nüsse & Samen',
    'macadamia': 'Nüsse & Samen', 'paranuss': 'Nüsse & Samen', 'pekannuss': 'Nüsse & Samen',
    'sesam': 'Nüsse & Samen', 'sesamsamen': 'Nüsse & Samen',
    'leinsamen': 'Nüsse & Samen', 'chiasamen': 'Nüsse & Samen',
    'kürbiskerne': 'Nüsse & Samen', 'kuerbiskerne': 'Nüsse & Samen',
    'sonnenblumenkerne': 'Nüsse & Samen', 'mohn': 'Nüsse & Samen',

    // ========== SAUCEN & CONDIMENTS ==========
    'sojasauce': 'Saucen', 'tamari': 'Saucen', 'teriyaki': 'Saucen',
    'worcestersauce': 'Saucen', 'tabasco': 'Saucen', 'sriracha': 'Saucen',
    'ketchup': 'Saucen', 'senf': 'Saucen', 'dijon senf': 'Saucen',
    'mayonnaise': 'Saucen', 'remoulade': 'Saucen', 'aioli': 'Saucen',
    'pesto': 'Saucen', 'tomatensauce': 'Saucen', 'tomatenmark': 'Saucen',
    'balsamico': 'Saucen', 'essig': 'Saucen', 'weinessig': 'Saucen',
    'apfelessig': 'Saucen', 'reisessig': 'Saucen',

    // ========== GETRÄNKE ==========
    'wasser': 'Getränke', 'mineralwasser': 'Getränke',
    'saft': 'Getränke', 'orangensaft': 'Getränke', 'apfelsaft': 'Getränke',
    'wein': 'Getränke', 'rotwein': 'Getränke', 'weißwein': 'Getränke',
    'bier': 'Getränke', 'sekt': 'Getränke', 'prosecco': 'Getränke',
    'kaffee': 'Getränke', 'tee': 'Getränke',

    // ========== SONSTIGES ==========
    'zucker': 'Sonstiges', 'rohrzucker': 'Sonstiges', 'brauner zucker': 'Sonstiges',
    'puderzucker': 'Sonstiges', 'honig': 'Sonstiges', 'ahornsirup': 'Sonstiges',
    'agavendicksaft': 'Sonstiges', 'schokolade': 'Sonstiges', 'kakao': 'Sonstiges',
    'backpulver': 'Sonstiges', 'natron': 'Sonstiges', 'hefe': 'Sonstiges',
    'gelatine': 'Sonstiges', 'speisestärke': 'Sonstiges', 'maisstärke': 'Sonstiges',
    'paniermehl': 'Sonstiges', 'semmelbrösel': 'Sonstiges', 'tofu': 'Sonstiges',
    'eier': 'Sonstiges', 'ei': 'Sonstiges'
};

// ==================== AUTO-SUGGEST LISTE (Alphabetisch sortiert) ====================
const INGREDIENT_SUGGESTIONS = [
    'Aal', 'Agavendicksaft', 'Ahornsirup', 'Aioli', 'Anchovis', 'Ananas',
    'Äpfel', 'Apfelessig', 'Aprikosen', 'Artischocke', 'Aubergine', 'Avocado',
    'Bacon', 'Baguette', 'Balsamico', 'Bananen', 'Barsch', 'Basilikum',
    'Basmati', 'Bergkäse', 'Birnen', 'Blaubeeren', 'Blauschimmelkäse', 'Blumenkohl',
    'Bohnen', 'Bratwurst', 'Brie', 'Brokkoli', 'Brombeeren', 'Brot', 'Brötchen',
    'Bulgur', 'Burrata', 'Butter', 'Butterkäse', 'Buttermilch',
    'Calamari', 'Camembert', 'Cashews', 'Cayennepfeffer', 'Cheddar',
    'Chiasamen', 'Chicorée', 'Chili', 'Chinakohl', 'Chorizo', 'Ciabatta',
    'Couscous', 'Crème fraîche', 'Curry',
    'Datteln', 'Dill', 'Dijon Senf', 'Dorade', 'Dorsch',
    'Edamer', 'Eier', 'Emmentaler', 'Ente', 'Entenbrust', 'Entrecôte', 'Erbsen',
    'Erdbeeren', 'Erdnüsse', 'Erdnussöl', 'Essig', 'Estragon',
    'Farfalle', 'Fasan', 'Feigen', 'Fenchel', 'Feta', 'Fettuccine', 'Forelle',
    'Frischkäse', 'Fusilli',
    'Gans', 'Garam Masala', 'Garnelen', 'Gnocchi', 'Gorgonzola', 'Gouda',
    'Granatapfel', 'Grapefruit', 'Griechischer Joghurt', 'Grünkohl', 'Gruyère', 'Gulasch', 'Gurken',
    'Hackfleisch', 'Hähnchenbrust', 'Hähnchenschenkel', 'Halloumi', 'Haselnüsse',
    'Heidelbeeren', 'Heilbutt', 'Hering', 'Himbeeren', 'Hirsch', 'Honig', 'Honigmelone', 'Hummer',
    'Ingwer',
    'Jakobsmuscheln', 'Jasminreis', 'Johannisbeeren', 'Joghurt',
    'Kabeljau', 'Kakao', 'Kalmar', 'Kardamom', 'Karotten', 'Kartoffeln', 'Käse',
    'Kasseler', 'Kefir', 'Ketchup', 'Kichererbsen', 'Kidneybohnen', 'Kirschen',
    'Knoblauch', 'Kochschinken', 'Kohlrabi', 'Kokosöl', 'Koriander', 'Krabben',
    'Kreuzkümmel', 'Kürbis', 'Kürbiskerne',
    'Lachs', 'Lammfleisch', 'Languste', 'Lauch', 'Leberwurst', 'Leerdammer',
    'Leinsamen', 'Leinöl', 'Limetten', 'Linsen', 'Lorbeer',
    'Macadamia', 'Magerquark', 'Mais', 'Makrele', 'Mandarinen', 'Mandeln', 'Mango',
    'Mangold', 'Margarine', 'Mascarpone', 'Matjes', 'Mayonnaise', 'Meersalz', 'Mehl',
    'Melone', 'Mettwurst', 'Miesmuscheln', 'Milch', 'Minze', 'Möhren', 'Mozzarella',
    'Müsli', 'Muskat',
    'Natron', 'Nektarinen', 'Nudeln',
    'Oktopus', 'Olivenöl', 'Orangen', 'Oregano',
    'Pangasius', 'Paniermehl', 'Papaya', 'Paprika', 'Paprikapulver', 'Parmesan',
    'Parmaschinken', 'Passionsfrucht', 'Pasta', 'Pastinaken', 'Pecorino', 'Penne',
    'Petersilie', 'Pesto', 'Pfeffer', 'Pfirsiche', 'Pflaumen', 'Philadelphia',
    'Pilze', 'Pinienkerne', 'Pistazien', 'Pomelo', 'Porree', 'Puderzucker',
    'Pute', 'Putenbrust',
    'Quark', 'Quinoa', 'Quitte',
    'Raclette', 'Radieschen', 'Rapsöl', 'Räucherlachs', 'Ravioli', 'Reh',
    'Reis', 'Remoulade', 'Rettich', 'Ribeye', 'Ricotta', 'Rind', 'Rinderfilet',
    'Risottoreis', 'Roastbeef', 'Romanesco', 'Rosenkohl', 'Rosmarin', 'Rosinen',
    'Rote Bete', 'Rote Linsen', 'Rotbarsch', 'Rotkohl', 'Rotwein', 'Rucola',
    'Safran', 'Sahne', 'Salami', 'Salbei', 'Salat', 'Salz', 'Sardinen',
    'Sauerkraut', 'Saure Sahne', 'Schafskäse', 'Schinken', 'Schlagsahne', 'Schmalz',
    'Schmand', 'Schnittlauch', 'Schnitzel', 'Schokolade', 'Scholle', 'Schwarzer Pfeffer',
    'Schwarzwälder Schinken', 'Schwarzwurzel', 'Schweinefleisch', 'Seelachs',
    'Sellerie', 'Semmelbrösel', 'Senf', 'Serranoschinken', 'Sesam', 'Sesamöl', 'Shrimps',
    'Sojasauce', 'Sonnenblumenkerne', 'Sonnenblumenöl', 'Spaghetti', 'Spargel', 'Speck',
    'Speisestärke', 'Spinat', 'Sriracha', 'Steak', 'Steinbutt', 'Sternanis',
    'Süßkartoffeln',
    'Tabasco', 'Tafelspitz', 'Tagliatelle', 'Tamari', 'Tatar', 'Tee',
    'Teriyaki', 'Thunfisch', 'Thymian', 'Tilsiter', 'Tintenfisch', 'Toast', 'Tofu',
    'Tomaten', 'Tomatenmark', 'Tomatensauce', 'Tortellini', 'Trauben', 'Truthahn',
    'Vanille', 'Vollkornbrot', 'Vollkornmehl', 'Vollkornreis',
    'Wachtel', 'Walnüsse', 'Walnussöl', 'Wasser', 'Wassermelone', 'Wein', 'Weinessig',
    'Weintrauben', 'Weißkohl', 'Weißwein', 'Weizenmehl', 'Wildreis', 'Wildschwein',
    'Wings', 'Wirsing', 'Wolfsbarsch', 'Worcestersauce', 'Wurst', 'Würstchen',
    'Zander', 'Zimt', 'Zitronen', 'Zucchini', 'Zucker', 'Zwiebeln'
].sort((a, b) => a.localeCompare(b, 'de'));

// ==================== HÄUFIGE GEWÜRZE (Spice Quick-Select) ====================
const COMMON_SPICES = [
    { name_de: 'Salz', name_en: 'Salt', icon: '🧂' },
    { name_de: 'Pfeffer', name_en: 'Pepper', icon: '🌶️' },
    { name_de: 'Paprikapulver', name_en: 'Paprika Powder', icon: '🌶️' },
    { name_de: 'Oregano', name_en: 'Oregano', icon: '🌿' },
    { name_de: 'Basilikum', name_en: 'Basil', icon: '🌿' },
    { name_de: 'Thymian', name_en: 'Thyme', icon: '🌿' },
    { name_de: 'Rosmarin', name_en: 'Rosemary', icon: '🌿' },
    { name_de: 'Curry', name_en: 'Curry', icon: '🍛' },
    { name_de: 'Kurkuma', name_en: 'Turmeric', icon: '🟡' },
    { name_de: 'Zimt', name_en: 'Cinnamon', icon: '🪵' },
    { name_de: 'Muskat', name_en: 'Nutmeg', icon: '🥜' },
    { name_de: 'Knoblauchpulver', name_en: 'Garlic Powder', icon: '🧄' },
    { name_de: 'Zwiebelpulver', name_en: 'Onion Powder', icon: '🧅' },
    { name_de: 'Chili', name_en: 'Chili', icon: '🌶️' },
    { name_de: 'Kreuzkümmel', name_en: 'Cumin', icon: '🌰' },
    { name_de: 'Koriander', name_en: 'Coriander', icon: '🌿' },
    { name_de: 'Petersilie', name_en: 'Parsley', icon: '🌿' },
    { name_de: 'Dill', name_en: 'Dill', icon: '🌿' },
    { name_de: 'Schnittlauch', name_en: 'Chives', icon: '🌿' },
    { name_de: 'Lorbeerblätter', name_en: 'Bay Leaves', icon: '🍃' }
];

// ==================== KATEGORIE-EMOJIS ====================
const CATEGORY_EMOJIS = {
    // German
    'Fisch': '🐟',
    'Fleisch': '🥩',
    'Gemüse': '🥦',
    'Getränke': '🥤',
    'Getreide': '🌾',
    'Gewürze': '🌿',
    'Kohlenhydrate': '🍚',
    'Milchprodukte': '🧀',
    'Nüsse & Samen': '🥜',
    'Obst': '🍎',
    'Öle & Fette': '🫒',
    'Saucen': '🥫',
    'Sonstiges': '📦',
    // English
    'Fish': '🐟',
    'Meat': '🥩',
    'Vegetables': '🥦',
    'Beverages': '🥤',
    'Grains': '🌾',
    'Spices': '🌿',
    'Carbohydrates': '🍚',
    'Dairy': '🧀',
    'Nuts & Seeds': '🥜',
    'Fruits': '🍎',
    'Oils & Fats': '🫒',
    'Sauces': '🥫',
    'Other': '📦'
};

// ==================== HELPER FUNKTIONEN ====================
function suggestCategory(ingredientName) {
    const normalized = ingredientName.toLowerCase().trim();

    // Exakte Übereinstimmung
    if (INGREDIENT_CATEGORIES[normalized]) {
        return INGREDIENT_CATEGORIES[normalized];
    }

    // Teilübereinstimmung
    for (const [key, category] of Object.entries(INGREDIENT_CATEGORIES)) {
        if (normalized.includes(key) || key.includes(normalized)) {
            return category;
        }
    }

    return null;
}

function filterSuggestions(input) {
    const normalized = input.toLowerCase().trim();
    if (normalized.length < 2) return [];

    return INGREDIENT_SUGGESTIONS.filter(item =>
        item.toLowerCase().includes(normalized)
    ).slice(0, 5);
}

function getCategoryEmoji(category) {
    return CATEGORY_EMOJIS[category] || '📦';
}

const Ingredients = {
    items: [],
    autocompleteDropdown: null,

    // Initialize category filter dropdown
    initCategoryFilter() {
        const filter = document.getElementById('ingredient-category-filter');
        if (!filter) return;

        const categories = CONFIG.getCategories();
        const allCategoriesLabel = i18n.t('ingredients.all_categories');

        Sanitize.setHTML(filter, `<option value="">${allCategoriesLabel}</option>` +
            categories.map(c => `<option value="${Sanitize.escapeHTML(c)}">${getCategoryEmoji(c)} ${Sanitize.escapeHTML(c)}</option>`).join(''));
    },

    // Load all ingredients
    async load() {
        const container = document.getElementById('ingredients-list');
        UI.showLoading(container);

        // Update filter dropdown on load (for language changes)
        this.initCategoryFilter();

        try {
            const category = document.getElementById('ingredient-category-filter')?.value || '';
            const params = category ? { category } : {};

            console.log('[Ingredients] Loading with params:', params);
            this.items = await api.getIngredients(params);
            console.log('[Ingredients] Loaded items:', this.items);
            this.render();
        } catch (error) {
            console.error('[Ingredients] Load error:', error);
            UI.showError(container, i18n.t('error.fetch_failed'));
        }
    },

    // Render ingredients list (exclude spices)
    render() {
        const container = document.getElementById('ingredients-list');

        // Filter out spices from main list
        const nonSpiceItems = this.items.filter(item => item.category !== 'Gewürze');

        if (!nonSpiceItems || nonSpiceItems.length === 0) {
            UI.showEmpty(container, i18n.t('ingredients.empty'), '🥗');
            return;
        }

        Sanitize.setHTML(container, nonSpiceItems.map(item => this.renderCard(item)).join(''));
    },

    // Render single ingredient card
    renderCard(item) {
        const isExpired = item.expiry_date && UI.isExpired(item.expiry_date);
        const expiryClass = isExpired ? 'expired' : '';
        const emoji = getCategoryEmoji(item.category);

        return `
            <div class="ingredient-card" data-id="${item.id}">
                <div class="ingredient-header">
                    <span class="ingredient-name">
                        <span class="category-emoji">${emoji}</span>
                        ${UI.escapeHtml(item.name)}
                    </span>
                    ${item.category ? `<span class="ingredient-category">${UI.escapeHtml(item.category)}</span>` : ''}
                </div>
                <div class="ingredient-expiry ${expiryClass}">
                    ${item.is_permanent
                        ? i18n.t('ingredients.permanent')
                        : (item.expiry_date
                            ? `${i18n.t('ingredients.expires')}: ${UI.formatDate(item.expiry_date)}${isExpired ? ` (${i18n.t('ingredients.expired')}!)` : ''}`
                            : i18n.t('ingredients.no_expiry'))}
                </div>
                <div class="ingredient-actions">
                    <button class="btn btn-sm btn-ghost" onclick="Ingredients.showEditModal(${item.id})">${i18n.t('ingredients.edit')}</button>
                    <button class="btn btn-sm btn-danger" onclick="Ingredients.delete(${item.id})">${i18n.t('ingredients.delete')}</button>
                </div>
            </div>
        `;
    },

    // Show add modal with Auto-Suggest and Auto-Category
    showAddModal() {
        UI.showFormModal({
            title: i18n.t('ingredients.add'),
            fields: [
                { name: 'name', label: i18n.t('ingredients.name'), required: true, placeholder: i18n.t('ingredients.placeholder'), id: 'add-ingredient-name' },
                {
                    name: 'category',
                    label: i18n.t('ingredients.category'),
                    type: 'select',
                    id: 'add-ingredient-category',
                    options: [
                        { value: '', label: '📦 ' + (i18n.currentLang === 'de' ? 'Keine Kategorie' : 'No category') },
                        ...CONFIG.getCategories().map(c => ({ value: c, label: `${getCategoryEmoji(c)} ${c}` }))
                    ]
                },
                { name: 'expiry_date', label: i18n.t('ingredients.expiry'), type: 'date' },
                { name: 'is_permanent', label: i18n.t('ingredients.permanent') + i18n.t('ingredients.hint_permanent'), type: 'checkbox' }
            ],
            submitText: i18n.t('ingredients.btn_add'),
            onSubmit: async (data) => {
                await this.create(data);
            }
        });

        // Setup Auto-Suggest and Auto-Category after modal is created
        setTimeout(() => {
            this.setupAutocomplete();
        }, 100);
    },

    // Setup Autocomplete for ingredient name input
    setupAutocomplete() {
        const nameInput = document.querySelector('input[name="name"]');
        const categorySelect = document.querySelector('select[name="category"]');

        if (!nameInput || !categorySelect) return;

        // Create dropdown
        const wrapper = nameInput.parentElement;
        wrapper.style.position = 'relative';

        let dropdown = wrapper.querySelector('.autocomplete-dropdown');
        if (!dropdown) {
            dropdown = document.createElement('div');
            dropdown.className = 'autocomplete-dropdown';
            dropdown.style.display = 'none';
            wrapper.appendChild(dropdown);
        }

        let timeout;

        nameInput.addEventListener('input', (e) => {
            clearTimeout(timeout);

            timeout = setTimeout(() => {
                const value = e.target.value;

                // Auto-Category
                const suggestedCategory = suggestCategory(value);
                if (suggestedCategory) {
                    categorySelect.value = suggestedCategory;
                    categorySelect.style.borderColor = '#4CAF50';
                    setTimeout(() => categorySelect.style.borderColor = '', 1500);
                }

                // Auto-Suggest Dropdown
                const suggestions = filterSuggestions(value);
                if (suggestions.length > 0) {
                    Sanitize.setHTML(dropdown, suggestions.map(item =>
                        `<div class="autocomplete-item" data-value="${Sanitize.escapeHTML(item)}">${Sanitize.escapeHTML(item)}</div>`
                    ).join(''));
                    dropdown.style.display = 'block';

                    // Add click handlers
                    dropdown.querySelectorAll('.autocomplete-item').forEach(el => {
                        el.addEventListener('click', () => {
                            nameInput.value = el.dataset.value;
                            dropdown.style.display = 'none';

                            // Trigger category suggestion
                            const cat = suggestCategory(el.dataset.value);
                            if (cat) {
                                categorySelect.value = cat;
                            }
                        });
                    });
                } else {
                    dropdown.style.display = 'none';
                }
            }, 150);
        });

        // Close dropdown on click outside
        document.addEventListener('click', (e) => {
            if (!wrapper.contains(e.target)) {
                dropdown.style.display = 'none';
            }
        });
    },

    // Show edit modal
    showEditModal(id) {
        const item = this.items.find(i => i.id === id);
        if (!item) return;

        // Format date for input
        const expiryDate = item.expiry_date ? item.expiry_date.split('T')[0] : '';

        UI.showFormModal({
            title: i18n.t('ingredients.edit'),
            fields: [
                { name: 'name', label: i18n.t('ingredients.name'), required: true, value: item.name },
                {
                    name: 'category',
                    label: i18n.t('ingredients.category'),
                    type: 'select',
                    value: item.category || '',
                    options: [
                        { value: '', label: '📦 ' + i18n.t('ingredients.no_category') },
                        ...CONFIG.getCategories().map(c => ({ value: c, label: `${getCategoryEmoji(c)} ${c}` }))
                    ]
                },
                { name: 'expiry_date', label: i18n.t('ingredients.expiry'), type: 'date', value: expiryDate },
                { name: 'is_permanent', label: i18n.t('ingredients.permanent'), type: 'checkbox', value: item.is_permanent }
            ],
            submitText: i18n.t('common.save'),
            onSubmit: async (data) => {
                await this.update(id, data);
            }
        });
    },

    // Update ingredient
    async update(id, data) {
        try {
            const payload = {};
            if (data.name) payload.name = data.name;
            if (data.category !== undefined) payload.category = data.category || null;
            if (data.expiry_date !== undefined) payload.expiry_date = data.expiry_date || null;
            if (data.is_permanent !== undefined) payload.is_permanent = data.is_permanent;

            console.log('[Ingredients] Updating:', id, payload);
            await api.updateIngredient(id, payload);
            UI.success(i18n.t('ingredients.updated'));
            await this.load();
        } catch (error) {
            console.error('[Ingredients] Update error:', error);
            UI.error(i18n.t('common.error_prefix') + error.message);
        }
    },

    // Delete ingredient
    delete(id) {
        const item = this.items.find(i => i.id === id);
        const confirmMsg = i18n.currentLang === 'de'
            ? `"${item?.name || 'Zutat'}" wirklich löschen?`
            : `Really delete "${item?.name || 'ingredient'}"?`;
        UI.confirm(confirmMsg, async () => {
            try {
                await api.deleteIngredient(id);
                UI.success(i18n.t('ingredients.deleted'));
                await this.load();
            } catch (error) {
                UI.error(i18n.t('common.error_prefix') + error.message);
            }
        });
    },

    // Get items for recipe selection (exclude spices)
    getItems() {
        return this.items.filter(item => item.category !== 'Gewürze');
    },

    // Get ALL items (including spices) - for internal use
    getAllItems() {
        return this.items;
    },

    // ==================== SPICE QUICK-SELECT ====================
    showSpiceQuickSelect() {
        // Close any existing modal first
        UI.closeModal();

        const lang = i18n.currentLang;

        // Get existing spices (lowercase for comparison)
        const existingSpices = this.getAllItems()
            .filter(i => i.category === 'Gewürze')
            .map(i => ({ name: i.name.toLowerCase(), id: i.id }));
        const existingNames = new Set(existingSpices.map(s => s.name));

        const spicesHtml = COMMON_SPICES.map(spice => {
            const spiceName = lang === 'de' ? spice.name_de : spice.name_en;
            const spiceId = spiceName.toLowerCase();
            const existing = existingSpices.find(s => s.name === spiceId);
            const isOwned = existingNames.has(spiceId);

            return `
                <label class="spice-checkbox ${isOwned ? 'owned' : ''}"
                       onclick="Ingredients.toggleSpice('${spiceName}', ${existing ? existing.id : 'null'}, this)"
                       style="cursor: pointer;">
                    <span class="spice-icon">${spice.icon}</span>
                    <span class="spice-name">${spiceName}</span>
                    <span class="spice-owned" style="display: ${isOwned ? 'inline' : 'none'}">✓</span>
                    <span class="spice-add" style="display: ${isOwned ? 'none' : 'inline'}">+</span>
                </label>
            `;
        }).join('');

        const modalContent = `
            <div class="spice-quickselect">
                <p class="spice-intro">${lang === 'de'
                    ? 'Klicke auf ein Gewürz um es hinzuzufügen/zu entfernen:'
                    : 'Click on a spice to add/remove it:'}</p>
                <div class="spice-grid">${spicesHtml}</div>
            </div>
        `;

        // Wait for previous modal to close before opening new one
        setTimeout(() => {
            UI.showModal(
                lang === 'de' ? '⚡ Gewürze verwalten' : '⚡ Manage Spices',
                modalContent,
                { size: 'medium' }
            );
        }, 100);
    },

    async toggleSpice(spiceName, spiceId, labelElement) {
        try {
            if (spiceId) {
                // Remove spice
                await api.deleteIngredient(spiceId);
                const msg = i18n.currentLang === 'de'
                    ? `${spiceName} entfernt`
                    : `${spiceName} removed`;
                UI.success(msg);

                // Update UI locally without reload
                if (labelElement) {
                    labelElement.classList.remove('owned');
                    const ownedSpan = labelElement.querySelector('.spice-owned');
                    const addSpan = labelElement.querySelector('.spice-add');
                    if (ownedSpan) ownedSpan.style.display = 'none';
                    if (addSpan) addSpan.style.display = 'inline';
                    labelElement.setAttribute('onclick', `Ingredients.toggleSpice('${spiceName}', null, this)`);
                }
            } else {
                // Add spice
                const response = await api.createIngredient({
                    name: spiceName,
                    category: 'Gewürze',
                    is_permanent: true
                });
                const msg = i18n.currentLang === 'de'
                    ? `${spiceName} hinzugefügt`
                    : `${spiceName} added`;
                UI.success(msg);

                // Update UI locally without reload
                if (labelElement && response.ingredient) {
                    labelElement.classList.add('owned');
                    const ownedSpan = labelElement.querySelector('.spice-owned');
                    const addSpan = labelElement.querySelector('.spice-add');
                    if (ownedSpan) ownedSpan.style.display = 'inline';
                    if (addSpan) addSpan.style.display = 'none';
                    labelElement.setAttribute('onclick', `Ingredients.toggleSpice('${spiceName}', ${response.ingredient.id}, this)`);
                }
            }

            // Don't reload - UI is already updated locally to prevent flickering
            // await this.load();
        } catch (error) {
            UI.error(error.message);
        }
    },

    // ==================== DUPLICATE PREVENTION ====================
    async create(data) {
        try {
            const payload = {
                name: data.name,
                category: data.category || null,
                expiry_date: data.expiry_date || null,
                is_permanent: data.is_permanent || false
            };

            console.log('[Ingredients] Creating:', payload);
            await api.createIngredient(payload);
            UI.success(i18n.t('ingredients.added'));
            await this.load();
        } catch (error) {
            console.error('[Ingredients] Create error:', error);

            // Handle 409 Conflict (Duplicate)
            if (error.message && error.message.includes('already exists')) {
                this.handleDuplicate(data.name, error);
            } else {
                UI.error(i18n.t('common.error_prefix') + error.message);
            }
        }
    },

    handleDuplicate(name, error) {
        const lang = i18n.currentLang;
        const msg = lang === 'de'
            ? `"${name}" existiert bereits. Möchtest du die vorhandene Zutat bearbeiten?`
            : `"${name}" already exists. Would you like to edit the existing ingredient?`;

        // Try to extract existing_id from error
        let existingId = null;
        try {
            const detail = JSON.parse(error.message.replace('Ingredient already exists', '').trim());
            existingId = detail.existing_id;
        } catch (e) {
            // Find by name
            const existing = this.items.find(i => i.name.toLowerCase() === name.toLowerCase());
            if (existing) existingId = existing.id;
        }

        UI.confirm(msg, () => {
            UI.closeModal();
            if (existingId) {
                this.showEditModal(existingId);
            } else {
                this.load();
            }
        });
    }
};
