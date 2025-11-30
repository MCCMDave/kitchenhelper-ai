// KitchenHelper-AI Internationalization (i18n) Module

const translations = {
    de: {
        // Auth
        'auth.login': 'Anmelden',
        'auth.register': 'Registrieren',
        'auth.email_or_username': 'E-Mail oder Benutzername',
        'auth.username': 'Benutzername',
        'auth.username_hint': '3-20 Zeichen, nur Buchstaben, Zahlen, - und _',
        'auth.email': 'E-Mail-Adresse',
        'auth.password': 'Passwort',
        'auth.password_min': 'Mind. 6 Zeichen',
        'auth.password_confirm': 'Passwort bestätigen',
        'auth.password_repeat': 'Passwort wiederholen',
        'auth.forgot_password': 'Passwort vergessen?',
        'auth.logout': 'Abmelden',
        'auth.demo_hint': 'Demo-Account: Registriere dich kostenlos!',
        'auth.subtitle': 'Dein KI-Rezeptgenerator',

        // Password Reset
        'reset.title': 'Passwort zurücksetzen',
        'reset.step1_text': 'Gib deine E-Mail-Adresse ein, um einen Reset-Code zu erhalten.',
        'reset.request_code': 'Reset-Code anfordern',
        'reset.step2_text': 'Gib den Reset-Code und dein neues Passwort ein.',
        'reset.code': 'Reset-Code',
        'reset.code_placeholder': 'Code aus der Console/Email',
        'reset.new_password': 'Neues Passwort',
        'reset.change_password': 'Passwort ändern',
        'reset.back': 'Zurück',
        'reset.success': 'Passwort erfolgreich geändert!',
        'reset.success_hint': 'Du kannst dich jetzt mit deinem neuen Passwort anmelden.',
        'reset.to_login': 'Zum Login',

        // Errors
        'error.invalid_email': 'Bitte gib eine gültige E-Mail-Adresse ein.',
        'error.password_too_short': 'Passwort muss mindestens 6 Zeichen lang sein.',
        'error.passwords_not_match': 'Die Passwörter stimmen nicht überein.',
        'error.username_too_short': 'Benutzername muss mindestens 3 Zeichen lang sein.',
        'error.username_invalid': 'Benutzername darf nur Buchstaben, Zahlen, - und _ enthalten.',
        'error.login_failed': 'Anmeldung fehlgeschlagen. Bitte prüfe deine Daten.',
        'error.registration_failed': 'Registrierung fehlgeschlagen.',
        'error.email_taken': 'Diese E-Mail ist bereits registriert.',
        'error.username_taken': 'Dieser Benutzername ist bereits vergeben.',
        'error.fetch_failed': 'Server nicht erreichbar. Bitte prüfe deine Verbindung.',
        'error.reset_code_required': 'Bitte gib den Reset-Code ein.',

        // Dashboard Navigation
        'nav.ingredients': 'Zutaten',
        'nav.recipes': 'Rezepte',
        'nav.scanner': 'Scanner',
        'nav.favorites': 'Favoriten',
        'nav.profiles': 'Präferenzen',
        'nav.settings': 'Einstellungen',
        'nav.pro_model': 'Pro Model',

        // Pro Model
        'pro.title': 'Pro Model Features',
        'pro.what_is_pro': 'Was ist KitchenHelper-AI Pro?',
        'pro.description': 'Upgrade auf Pro und schalte erweiterte KI-Features mit besserer Rezeptqualität und mehr Personalisierung frei.',
        'pro.free_tier': 'Free Tier',
        'pro.free_basic_recipes': 'Basis-Rezeptgenerierung',
        'pro.free_ingredients': 'Zutatenverwaltung',
        'pro.free_profiles': 'Bis zu 3 Ernährungsprofile',
        'pro.free_favorites': 'Lieblingsrezepte',
        'pro.free_model': 'Nutzt: llama3.2:3b (kleineres Modell)',
        'pro.free_limit': 'Limitierte tägliche Anfragen',
        'pro.pro_tier': 'Pro Tier',
        'pro.pro_advanced': 'Erweiterte Rezeptgenerierung',
        'pro.pro_model': 'Nutzt: llama3.3:70b (Premium-Modell)',
        'pro.pro_quality': 'Bessere Rezeptqualität & Kreativität',
        'pro.pro_unlimited': 'Unbegrenzte tägliche Anfragen',
        'pro.pro_profiles': 'Unbegrenzte Ernährungsprofile',
        'pro.pro_priority': 'Prioritäts-Support',
        'pro.pro_encryption': 'End-to-End Datenverschlüsselung',
        'pro.cancel_anytime': 'Jederzeit kündbar',
        'pro.upgrade_now': 'Jetzt upgraden',
        'pro.current_tier': 'Aktueller Plan:',
        'pro.faq': 'Häufige Fragen',
        'pro.faq_payment': 'Welche Zahlungsmethoden werden akzeptiert?',
        'pro.faq_payment_answer': 'Wir akzeptieren Kreditkarten, PayPal und SEPA-Lastschrift.',
        'pro.faq_cancel': 'Kann ich jederzeit kündigen?',
        'pro.faq_cancel_answer': 'Ja, du kannst dein Abo jederzeit in den Einstellungen kündigen. Es läuft bis zum Ende des bezahlten Zeitraums.',
        'pro.faq_difference': 'Was ist der Unterschied zwischen den Modellen?',
        'pro.faq_difference_answer': 'Das Pro-Modell (llama3.3:70b) ist deutlich größer und intelligenter. Es erstellt kreativere Rezepte, berücksichtigt Präferenzen besser und liefert detailliertere Anweisungen.',
        'pro.already_pro': 'Bereits Pro-Mitglied',
        'pro.login_required': 'Bitte melde dich an, um Pro zu abonnieren.',
        'pro.already_subscribed': 'Du bist bereits Pro-Mitglied!',
        'pro.confirm_subscribe': 'Möchtest du wirklich auf Pro upgraden für €4.99/Monat?',
        'pro.processing': 'Verarbeite...',
        'pro.upgrade_success': 'Erfolgreich auf Pro upgegradet! 🎉',
        'pro.upgrade_error': 'Upgrade fehlgeschlagen',
        'pro.not_subscribed': 'Du hast kein aktives Pro-Abo.',
        'pro.confirm_cancel': 'Möchtest du dein Pro-Abo wirklich kündigen?',
        'pro.cancel_success': 'Abo erfolgreich gekündigt.',
        'pro.cancel_error': 'Kündigung fehlgeschlagen',

        // Ingredients
        'ingredients.title': 'Meine Zutaten',
        'ingredients.add': 'Zutat hinzufügen',
        'ingredients.name': 'Name',
        'ingredients.category': 'Kategorie',
        'ingredients.all_categories': 'Alle Kategorien',
        'ingredients.expiry': 'Ablaufdatum',
        'ingredients.permanent': 'Dauerhaft',
        'ingredients.edit': 'Bearbeiten',
        'ingredients.delete': 'Löschen',
        'ingredients.expired': 'Abgelaufen',
        'ingredients.spices': 'Gewürze',

        // Recipes
        'recipes.title': 'Rezepte generieren',
        'recipes.select_ingredients': 'Wähle deine Zutaten',
        'recipes.generate': 'Rezepte generieren',
        'recipes.generated': 'Generierte Rezepte',
        'recipes.history': 'Letzte Rezepte',
        'recipes.selected': 'Zutaten ausgewählt',
        'recipes.difficulty': 'Schwierigkeit',
        'recipes.time': 'Zeit',
        'recipes.servings': 'Portionen',
        'recipes.method': 'Methode',
        'recipes.used_ingredients': 'Verwendete Zutaten',
        'recipes.all_ingredients': 'Alle Zutaten',
        'recipes.leftover_tips': 'Reste-Tipps',
        'recipes.nutrition': 'Nährwerte pro Portion',
        'recipes.add_favorite': 'Zu Favoriten hinzufügen',
        'recipes.added_favorite': 'Zu Favoriten hinzugefügt!',
        'recipes.already_favorite': 'Bereits in Favoriten!',
        'recipes.favorite_limit': 'Favoriten-Limit erreicht!',
        'recipes.remaining': 'Noch {count} Rezepte heute verfügbar',
        'recipes.portions': 'Portionen',
        'recipes.adjust_portions': 'Portionen anpassen',

        // Favorites
        'favorites.title': 'Meine Favoriten',
        'favorites.empty': 'Keine Favoriten vorhanden. Füge Rezepte zu deinen Favoriten hinzu!',
        'favorites.remove': 'Aus Favoriten entfernen',
        'favorites.details': 'Details',
        'favorites.less': 'Weniger',
        'favorites.export_pdf': 'Als PDF exportieren',
        'favorites.added': 'Hinzugefügt',
        'favorites.used_ingredients': 'Verwendete Zutaten',
        'favorites.all_ingredients': 'Alle Zutaten',
        'favorites.leftover_tips': 'Reste-Tipps',
        'favorites.nutrition': 'Nährwerte pro Portion',
        'favorites.confirm_remove': 'Favorit wirklich entfernen?',
        'favorites.removed': 'Favorit entfernt!',
        'favorites.pdf_creating': 'PDF wird erstellt...',
        'favorites.pdf_success': 'PDF erfolgreich heruntergeladen!',
        'favorites.pdf_error': 'Fehler beim PDF-Export',

        // Profiles
        'profiles.title': 'Ernährungspräferenzen',
        'profiles.add': 'Präferenz hinzufügen',
        'profiles.all_added': 'Alle Präferenzen bereits hinzugefügt!',
        'profiles.new': 'Neue Ernährungspräferenz',
        'profiles.type': 'Präferenz-Typ',
        'profiles.name': 'Name',
        'profiles.name_placeholder': 'z.B. Mein Diabetes Profil',
        'profiles.activate_now': 'Sofort aktivieren',
        'profiles.active': 'Aktiv',
        'profiles.inactive': 'Inaktiv',
        'profiles.no_settings': 'Keine besonderen Einstellungen',
        'profiles.unit': 'Einheit',
        'profiles.daily_carb_limit': 'Tägliches Carb-Limit (g)',
        'profiles.confirm_delete': '"{name}" wirklich löschen?',
        'profiles.created': 'Präferenz erstellt!',
        'profiles.updated': 'Präferenz aktualisiert!',
        'profiles.deleted': 'Präferenz gelöscht!',
        'profiles.activated': 'Präferenz aktiviert!',
        'profiles.deactivated': 'Präferenz deaktiviert!',
        'profiles.strict_mode': 'Strikte Zutatenliste',
        'profiles.strict_mode_hint': 'Nur Rezepte mit vorhandenen Zutaten',
        'profiles.shopping_mode': 'Flexibler Modus',
        'profiles.shopping_mode_hint': 'Neue Zutaten werden vorgeschlagen',
        'recipes.select_warning': 'Bitte wähle mindestens eine Zutat aus!',
        'recipes.no_generated': 'Keine Rezepte generiert. Wähle Zutaten und klicke auf "Generieren"!',
        'recipes.no_history': 'Noch keine Rezepte generiert.',
        'recipes.error_generating': 'Fehler beim Generieren',
        'recipes.error_loading': 'Fehler beim Laden',
        'recipes.fat': 'Fett',
        'recipes.only_available': 'Nur vorhandene Zutaten',
        'recipes.allow_new': 'Neue Zutaten erlauben',

        // Favorites extended
        'favorites.share': 'Teilen',
        'favorites.shopping_list': 'Einkaufsliste',
        'favorites.link_copied': 'Link kopiert!',
        'favorites.no_favorites': 'Keine Favoriten vorhanden',
        'favorites.creating_link': 'Erstelle Link...',
        'favorites.creating_list': 'Erstelle Einkaufsliste...',
        'favorites.list_created': 'Einkaufsliste erstellt!',
        'favorites.share_text': 'Teile dieses Rezept mit anderen:',
        'favorites.link_valid_until': 'Link gültig bis:',
        'favorites.copy': 'Kopieren',
        'favorites.share_recipe': 'Rezept teilen',
        'favorites.search_placeholder': 'Favoriten durchsuchen...',
        'favorites.no_results': 'Keine Favoriten gefunden',

        // Ingredients extended
        'ingredients.empty': 'Keine Zutaten vorhanden. Füge deine erste Zutat hinzu!',
        'ingredients.expires': 'Ablauf',
        'ingredients.no_expiry': 'Kein Ablaufdatum',
        'ingredients.placeholder': 'z.B. Tomaten',
        'ingredients.no_category': 'Keine Kategorie',
        'ingredients.hint_permanent': ' (z.B. Gewürze)',
        'ingredients.btn_add': 'Hinzufügen',
        'ingredients.updated': 'Zutat aktualisiert!',
        'ingredients.deleted': 'Zutat gelöscht!',
        'ingredients.added': 'Zutat hinzugefügt!',
        'ingredients.no_spices_selected': 'Keine Gewürze ausgewählt',

        // User Menu
        'user.emoji_updated': 'Emoji aktualisiert!',
        'user.emoji_error': 'Fehler beim Aktualisieren des Emojis',

        // Shopping List
        'shopping.title': 'Einkaufsliste',
        'shopping.generate': 'Liste erstellen',
        'shopping.empty': 'Keine Rezepte ausgewählt',
        'shopping.items': 'Artikel',
        'shopping.checked': 'erledigt',

        // Scanner
        'scanner.title': 'Lebensmittelscanner',
        'scanner.mode_barcode': 'Barcode-Scanner',
        'scanner.mode_ocr': 'OCR (Zutatenliste)',
        'scanner.barcode_title': 'Produkt-Barcode scannen',
        'scanner.barcode_hint': 'Richte deine Kamera auf einen Produkt-Barcode, um Zutatenlisten zu erhalten',
        'scanner.ocr_title': 'Zutatenliste scannen',
        'scanner.ocr_hint': 'Fotografiere Zutatenlisten auf Verpackungen, um sie zu extrahieren',
        'scanner.start_scan': 'Scan starten',
        'scanner.stop_scan': 'Scan stoppen',
        'scanner.capture': 'Aufnehmen',
        'scanner.loading_product': 'Lade Produktdaten...',
        'scanner.error_loading_product': 'Fehler beim Laden des Produkts',
        'scanner.unknown_product': 'Unbekanntes Produkt',
        'scanner.brands': 'Marken',
        'scanner.categories': 'Kategorien',
        'scanner.ingredients': 'Zutaten',
        'scanner.add_ingredients': 'Zutaten hinzufügen',
        'scanner.scan_another': 'Weiteren Code scannen',
        'scanner.no_ingredients': 'Keine Zutaten gefunden',
        'scanner.select_ingredients': 'Zutaten auswählen',
        'scanner.select_ingredients_hint': 'Wähle die Zutaten aus, die du zu deinem Inventar hinzufügen möchtest:',
        'scanner.no_ingredients_selected': 'Bitte wähle mindestens eine Zutat aus',
        'scanner.processing_ocr': 'Verarbeite OCR...',
        'scanner.no_ingredients_found': 'Keine Zutaten gefunden',
        'scanner.ocr_error': 'OCR-Fehler',

        // Common extended
        'common.error_prefix': 'Fehler: ',
        'common.add': 'Hinzufügen',

        // Settings
        'settings.title': 'Einstellungen',
        'settings.profile': 'Profil bearbeiten',
        'settings.avatar_emoji': 'Avatar-Emoji',
        'settings.color_scheme': 'Farbschema',
        'settings.color_scheme_hint': 'Wähle ein Farbschema, das zu deinen Vorlieben passt',
        'settings.theme_light': 'Hell',
        'settings.theme_dark': 'Dunkel',
        'settings.theme_sepia': 'Sepia',
        'settings.theme_ocean-light': 'Ozean Hell',
        'settings.theme_ocean-dark': 'Ozean Dunkel',
        'settings.theme_forest-light': 'Wald Hell',
        'settings.theme_forest-dark': 'Wald Dunkel',
        'settings.theme_sunset-light': 'Sonnenuntergang Hell',
        'settings.theme_sunset-dark': 'Sonnenuntergang Dunkel',
        'settings.theme_nord': 'Nord',
        'settings.theme_solarized': 'Solarized',
        'settings.theme_dracula': 'Dracula',
        'settings.change_password': 'Passwort ändern',
        'settings.new_password': 'Neues Passwort',
        'settings.confirm_password': 'Passwort bestätigen',
        'settings.account_info': 'Account-Info',
        'settings.danger_zone': 'Gefahrenzone',
        'settings.danger_warning': 'Achtung: Diese Aktion kann nicht rückgängig gemacht werden!',
        'settings.delete_account': 'Account löschen',

        // Common
        'common.save': 'Speichern',
        'common.cancel': 'Abbrechen',
        'common.delete': 'Löschen',
        'common.edit': 'Bearbeiten',
        'common.close': 'Schließen',
        'common.loading': 'Laden...',
        'common.success': 'Erfolgreich!',
        'common.error': 'Fehler',
        'common.yes': 'Ja',
        'common.no': 'Nein',
        'common.confirm': 'Bestätigung',
    },

    en: {
        // Auth
        'auth.login': 'Login',
        'auth.register': 'Sign Up',
        'auth.email_or_username': 'Email or Username',
        'auth.username': 'Username',
        'auth.username_hint': '3-20 characters, letters, numbers, - and _ only',
        'auth.email': 'Email Address',
        'auth.password': 'Password',
        'auth.password_min': 'Min. 6 characters',
        'auth.password_confirm': 'Confirm Password',
        'auth.password_repeat': 'Repeat password',
        'auth.forgot_password': 'Forgot password?',
        'auth.logout': 'Logout',
        'auth.demo_hint': 'Demo account: Sign up for free!',
        'auth.subtitle': 'Your AI Recipe Generator',

        // Password Reset
        'reset.title': 'Reset Password',
        'reset.step1_text': 'Enter your email address to receive a reset code.',
        'reset.request_code': 'Request Reset Code',
        'reset.step2_text': 'Enter the reset code and your new password.',
        'reset.code': 'Reset Code',
        'reset.code_placeholder': 'Code from Console/Email',
        'reset.new_password': 'New Password',
        'reset.change_password': 'Change Password',
        'reset.back': 'Back',
        'reset.success': 'Password changed successfully!',
        'reset.success_hint': 'You can now log in with your new password.',
        'reset.to_login': 'Go to Login',

        // Errors
        'error.invalid_email': 'Please enter a valid email address.',
        'error.password_too_short': 'Password must be at least 6 characters.',
        'error.passwords_not_match': 'Passwords do not match.',
        'error.username_too_short': 'Username must be at least 3 characters.',
        'error.username_invalid': 'Username can only contain letters, numbers, - and _.',
        'error.login_failed': 'Login failed. Please check your credentials.',
        'error.registration_failed': 'Registration failed.',
        'error.email_taken': 'This email is already registered.',
        'error.username_taken': 'This username is already taken.',
        'error.fetch_failed': 'Server unreachable. Please check your connection.',
        'error.reset_code_required': 'Please enter the reset code.',

        // Dashboard Navigation
        'nav.ingredients': 'Ingredients',
        'nav.recipes': 'Recipes',
        'nav.scanner': 'Scanner',
        'nav.favorites': 'Favorites',
        'nav.profiles': 'Preferences',
        'nav.settings': 'Settings',
        'nav.pro_model': 'Pro Model',

        // Pro Model
        'pro.title': 'Pro Model Features',
        'pro.what_is_pro': 'What is KitchenHelper-AI Pro?',
        'pro.description': 'Upgrade to Pro and unlock advanced AI features with better recipe quality and more personalization.',
        'pro.free_tier': 'Free Tier',
        'pro.free_basic_recipes': 'Basic recipe generation',
        'pro.free_ingredients': 'Ingredient management',
        'pro.free_profiles': 'Up to 3 dietary profiles',
        'pro.free_favorites': 'Favorite recipes',
        'pro.free_model': 'Uses: llama3.2:3b (smaller model)',
        'pro.free_limit': 'Limited daily requests',
        'pro.pro_tier': 'Pro Tier',
        'pro.pro_advanced': 'Advanced recipe generation',
        'pro.pro_model': 'Uses: llama3.3:70b (premium model)',
        'pro.pro_quality': 'Better recipe quality & creativity',
        'pro.pro_unlimited': 'Unlimited daily requests',
        'pro.pro_profiles': 'Unlimited dietary profiles',
        'pro.pro_priority': 'Priority support',
        'pro.pro_encryption': 'End-to-end data encryption',
        'pro.cancel_anytime': 'Cancel anytime',
        'pro.upgrade_now': 'Upgrade Now',
        'pro.current_tier': 'Current Plan:',
        'pro.faq': 'Frequently Asked Questions',
        'pro.faq_payment': 'Which payment methods are accepted?',
        'pro.faq_payment_answer': 'We accept credit cards, PayPal, and SEPA direct debit.',
        'pro.faq_cancel': 'Can I cancel anytime?',
        'pro.faq_cancel_answer': 'Yes, you can cancel your subscription anytime in settings. It will run until the end of the paid period.',
        'pro.faq_difference': 'What is the difference between the models?',
        'pro.faq_difference_answer': 'The Pro model (llama3.3:70b) is significantly larger and more intelligent. It creates more creative recipes, better considers preferences, and provides more detailed instructions.',
        'pro.already_pro': 'Already Pro Member',
        'pro.login_required': 'Please log in to subscribe to Pro.',
        'pro.already_subscribed': 'You are already a Pro member!',
        'pro.confirm_subscribe': 'Do you really want to upgrade to Pro for €4.99/month?',
        'pro.processing': 'Processing...',
        'pro.upgrade_success': 'Successfully upgraded to Pro! 🎉',
        'pro.upgrade_error': 'Upgrade failed',
        'pro.not_subscribed': 'You don\'t have an active Pro subscription.',
        'pro.confirm_cancel': 'Do you really want to cancel your Pro subscription?',
        'pro.cancel_success': 'Subscription successfully cancelled.',
        'pro.cancel_error': 'Cancellation failed',

        // Ingredients
        'ingredients.title': 'My Ingredients',
        'ingredients.add': 'Add Ingredient',
        'ingredients.name': 'Name',
        'ingredients.category': 'Category',
        'ingredients.all_categories': 'All Categories',
        'ingredients.expiry': 'Expiry Date',
        'ingredients.permanent': 'Permanent',
        'ingredients.edit': 'Edit',
        'ingredients.delete': 'Delete',
        'ingredients.expired': 'Expired',
        'ingredients.spices': 'Spices',

        // Recipes
        'recipes.title': 'Generate Recipes',
        'recipes.select_ingredients': 'Select your ingredients',
        'recipes.generate': 'Generate Recipes',
        'recipes.generated': 'Generated Recipes',
        'recipes.history': 'Recent Recipes',
        'recipes.selected': 'ingredients selected',
        'recipes.difficulty': 'Difficulty',
        'recipes.time': 'Time',
        'recipes.servings': 'Servings',
        'recipes.method': 'Method',
        'recipes.used_ingredients': 'Used Ingredients',
        'recipes.all_ingredients': 'All Ingredients',
        'recipes.leftover_tips': 'Leftover Tips',
        'recipes.nutrition': 'Nutrition per Serving',
        'recipes.add_favorite': 'Add to favorites',
        'recipes.added_favorite': 'Added to favorites!',
        'recipes.already_favorite': 'Already in favorites!',
        'recipes.favorite_limit': 'Favorite limit reached!',
        'recipes.remaining': '{count} recipes remaining today',
        'recipes.portions': 'Servings',
        'recipes.adjust_portions': 'Adjust Servings',
        'recipes.select_warning': 'Please select at least one ingredient!',
        'recipes.no_generated': 'No recipes generated. Select ingredients and click "Generate"!',
        'recipes.no_history': 'No recipes generated yet.',
        'recipes.error_generating': 'Error generating',
        'recipes.error_loading': 'Error loading',
        'recipes.fat': 'Fat',
        'recipes.only_available': 'Existing Ingredients Only',
        'recipes.allow_new': 'Allow New Ingredients',

        // Favorites
        'favorites.title': 'My Favorites',
        'favorites.empty': 'No favorites yet. Add recipes to your favorites!',
        'favorites.remove': 'Remove from favorites',
        'favorites.details': 'Details',
        'favorites.less': 'Less',
        'favorites.export_pdf': 'Export as PDF',
        'favorites.added': 'Added',
        'favorites.used_ingredients': 'Used Ingredients',
        'favorites.all_ingredients': 'All Ingredients',
        'favorites.leftover_tips': 'Leftover Tips',
        'favorites.nutrition': 'Nutrition per Serving',
        'favorites.confirm_remove': 'Really remove this favorite?',
        'favorites.removed': 'Favorite removed!',
        'favorites.pdf_creating': 'Creating PDF...',
        'favorites.pdf_success': 'PDF downloaded successfully!',
        'favorites.pdf_error': 'Error exporting PDF',

        // Profiles
        'profiles.title': 'Dietary Preferences',
        'profiles.add': 'Add Preference',
        'profiles.all_added': 'All preferences already added!',
        'profiles.new': 'New Dietary Preference',
        'profiles.type': 'Preference Type',
        'profiles.name': 'Name',
        'profiles.name_placeholder': 'e.g. My Diabetes Profile',
        'profiles.activate_now': 'Activate immediately',
        'profiles.active': 'Active',
        'profiles.inactive': 'Inactive',
        'profiles.no_settings': 'No special settings',
        'profiles.unit': 'Unit',
        'profiles.daily_carb_limit': 'Daily Carb Limit (g)',
        'profiles.confirm_delete': 'Really delete "{name}"?',
        'profiles.created': 'Preference created!',
        'profiles.updated': 'Preference updated!',
        'profiles.deleted': 'Preference deleted!',
        'profiles.activated': 'Preference activated!',
        'profiles.deactivated': 'Preference deactivated!',
        'profiles.strict_mode': 'Strict Ingredient List',
        'profiles.strict_mode_hint': 'Only recipes with existing ingredients',
        'profiles.shopping_mode': 'Flexible Mode',
        'profiles.shopping_mode_hint': 'New ingredients will be suggested',
        'recipes.select_warning': 'Please select at least one ingredient!',
        'recipes.no_generated': 'No recipes generated. Select ingredients and click "Generate"!',
        'recipes.no_history': 'No recipes generated yet.',
        'recipes.error_generating': 'Error generating',
        'recipes.error_loading': 'Error loading',
        'recipes.fat': 'Fat',

        // Favorites extended
        'favorites.share': 'Share',
        'favorites.shopping_list': 'Shopping List',
        'favorites.link_copied': 'Link copied!',
        'favorites.no_favorites': 'No favorites available',
        'favorites.creating_link': 'Creating link...',
        'favorites.creating_list': 'Creating shopping list...',
        'favorites.list_created': 'Shopping list created!',
        'favorites.share_text': 'Share this recipe with others:',
        'favorites.link_valid_until': 'Link valid until:',
        'favorites.copy': 'Copy',
        'favorites.share_recipe': 'Share Recipe',
        'favorites.search_placeholder': 'Search favorites...',
        'favorites.no_results': 'No favorites found',

        // Ingredients extended
        'ingredients.empty': 'No ingredients yet. Add your first ingredient!',
        'ingredients.expires': 'Expires',
        'ingredients.no_expiry': 'No expiry date',
        'ingredients.placeholder': 'e.g. Tomatoes',
        'ingredients.no_category': 'No category',
        'ingredients.hint_permanent': ' (e.g. Spices)',
        'ingredients.btn_add': 'Add',
        'ingredients.updated': 'Ingredient updated!',
        'ingredients.deleted': 'Ingredient deleted!',
        'ingredients.added': 'Ingredient added!',
        'ingredients.no_spices_selected': 'No spices selected',

        // User Menu
        'user.emoji_updated': 'Emoji updated!',
        'user.emoji_error': 'Error updating emoji',

        // Shopping List
        'shopping.title': 'Shopping List',
        'shopping.generate': 'Create List',
        'shopping.empty': 'No recipes selected',
        'shopping.items': 'Items',
        'shopping.checked': 'done',

        // Scanner
        'scanner.title': 'Food Scanner',
        'scanner.mode_barcode': 'Barcode Scanner',
        'scanner.mode_ocr': 'OCR (Ingredient List)',
        'scanner.barcode_title': 'Scan Product Barcode',
        'scanner.barcode_hint': 'Point your camera at a product barcode to get ingredient information',
        'scanner.ocr_title': 'Scan Ingredient List',
        'scanner.ocr_hint': 'Take a photo of ingredient lists on packaging to extract them',
        'scanner.start_scan': 'Start Scan',
        'scanner.stop_scan': 'Stop Scan',
        'scanner.capture': 'Capture',
        'scanner.loading_product': 'Loading product data...',
        'scanner.error_loading_product': 'Error loading product',
        'scanner.unknown_product': 'Unknown product',
        'scanner.brands': 'Brands',
        'scanner.categories': 'Categories',
        'scanner.ingredients': 'Ingredients',
        'scanner.add_ingredients': 'Add Ingredients',
        'scanner.scan_another': 'Scan Another',
        'scanner.no_ingredients': 'No ingredients found',
        'scanner.select_ingredients': 'Select Ingredients',
        'scanner.select_ingredients_hint': 'Select the ingredients you want to add to your inventory:',
        'scanner.no_ingredients_selected': 'Please select at least one ingredient',
        'scanner.processing_ocr': 'Processing OCR...',
        'scanner.no_ingredients_found': 'No ingredients found',
        'scanner.ocr_error': 'OCR error',

        // Common extended
        'common.error_prefix': 'Error: ',
        'common.add': 'Add',

        // Settings
        'settings.title': 'Settings',
        'settings.profile': 'Edit Profile',
        'settings.avatar_emoji': 'Avatar Emoji',
        'settings.color_scheme': 'Color Scheme',
        'settings.color_scheme_hint': 'Choose a color scheme that suits your preference',
        'settings.theme_light': 'Light',
        'settings.theme_dark': 'Dark',
        'settings.theme_sepia': 'Sepia',
        'settings.theme_ocean-light': 'Ocean Light',
        'settings.theme_ocean-dark': 'Ocean Dark',
        'settings.theme_forest-light': 'Forest Light',
        'settings.theme_forest-dark': 'Forest Dark',
        'settings.theme_sunset-light': 'Sunset Light',
        'settings.theme_sunset-dark': 'Sunset Dark',
        'settings.theme_nord': 'Nord',
        'settings.theme_solarized': 'Solarized',
        'settings.theme_dracula': 'Dracula',
        'settings.change_password': 'Change Password',
        'settings.new_password': 'New Password',
        'settings.confirm_password': 'Confirm Password',
        'settings.account_info': 'Account Info',
        'settings.danger_zone': 'Danger Zone',
        'settings.danger_warning': 'Warning: This action cannot be undone!',
        'settings.delete_account': 'Delete Account',

        // Common
        'common.save': 'Save',
        'common.cancel': 'Cancel',
        'common.delete': 'Delete',
        'common.edit': 'Edit',
        'common.close': 'Close',
        'common.loading': 'Loading...',
        'common.success': 'Success!',
        'common.error': 'Error',
        'common.yes': 'Yes',
        'common.no': 'No',
        'common.confirm': 'Confirm',
    },

    fr: {


    },

    es: {


    },

    it: {


    },

    pt: {


    },

    sv: {


    },

    no: {


    },

    da: {


    },

    nl: {


    }
};

const i18n = {
    currentLang: localStorage.getItem('kitchenhelper_lang') || 'en',

    init() {
        this.setLanguage(this.currentLang, false);

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.lang-menu')) {
                this.closeDropdown();
            }
        });

        console.log('[i18n] Initialized with language:', this.currentLang);
    },

    t(key) {
        return translations[this.currentLang][key] || translations['de'][key] || key;
    },

    setLanguage(lang, updateUI = true) {
        if (!translations[lang]) {
            console.warn('[i18n] Unknown language:', lang);
            return;
        }

        this.currentLang = lang;
        localStorage.setItem('kitchenhelper_lang', lang);
        document.documentElement.setAttribute('lang', lang);

        if (updateUI) {
            this.updateUI();
        }

        // Update language toggle button
        const langText = document.querySelector('.lang-toggle-text');
        if (langText) {
            langText.textContent = lang.toUpperCase();
        }

        // Close dropdown after selection
        this.closeDropdown();

        console.log('[i18n] Language set to:', lang);
    },

    toggleDropdown(event) {
        event.stopPropagation();
        const dropdown = document.getElementById('lang-dropdown');
        dropdown.classList.toggle('show');
    },

    closeDropdown() {
        const dropdown = document.getElementById('lang-dropdown');
        dropdown.classList.remove('show');
    },

    // Keep old toggle function for backwards compatibility
    toggle() {
        this.toggleDropdown(new Event('click'));
    },

    updateUI() {
        // Update all elements with data-i18n attribute
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            const text = this.t(key);

            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                if (el.hasAttribute('placeholder')) {
                    el.placeholder = text;
                }
            } else {
                el.textContent = text;
            }
        });

        // Update elements with data-i18n-placeholder
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            el.placeholder = this.t(key);
        });

        // Re-render active modules to update dynamic content
        if (typeof Ingredients !== 'undefined' && Ingredients.items && Ingredients.items.length > 0) {
            Ingredients.render();
        }

        if (typeof Recipes !== 'undefined' && Recipes.generatedRecipes && Recipes.generatedRecipes.length > 0) {
            Recipes.renderGeneratedRecipes();
        }

        if (typeof Favorites !== 'undefined' && Favorites.items && Favorites.items.length > 0) {
            Favorites.render();
        }

        if (typeof Profiles !== 'undefined' && Profiles.items) {
            Profiles.render();
        }

        // Update ingredient selection checkboxes if on recipes tab
        if (typeof Recipes !== 'undefined' && document.getElementById('ingredient-checkboxes')) {
            Recipes.loadIngredientSelection();
        }

        console.log('[i18n] UI updated');
    }
};

// Auto-init when DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => i18n.init());
} else {
    i18n.init();
}
