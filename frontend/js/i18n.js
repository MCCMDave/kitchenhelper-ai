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
        // Auth
        'auth.login': 'Connexion',
        'auth.register': 'S\'inscrire',
        'auth.email_or_username': 'E-mail ou nom d\'utilisateur',
        'auth.username': 'Nom d\'utilisateur',
        'auth.email': 'Adresse e-mail',
        'auth.password': 'Mot de passe',
        'auth.password_min': 'Min. 6 caractères',
        'auth.password_confirm': 'Confirmer le mot de passe',
        'auth.forgot_password': 'Mot de passe oublié?',
        'auth.logout': 'Déconnexion',
        'auth.subtitle': 'Votre générateur de recettes IA',

        // Navigation
        'nav.ingredients': 'Mes ingrédients',
        'nav.recipes': 'Générer des recettes',
        'nav.favorites': 'Mes favoris',
        'nav.scanner': 'Scanner',
        'nav.profiles': 'Préférences alimentaires',
        'nav.settings': 'Paramètres',

        // Common
        'common.save': 'Enregistrer',
        'common.cancel': 'Annuler',
        'common.delete': 'Supprimer',
        'common.edit': 'Modifier',
        'common.add': 'Ajouter',
        'common.close': 'Fermer',
        'common.loading': 'Chargement...',
        'common.search': 'Rechercher',
        'common.filter': 'Filtrer',
        'common.success': 'Succès!',
        'common.error': 'Erreur',
        'common.yes': 'Oui',
        'common.no': 'Non',

        // Ingredients
        'ingredients.title': 'Mes ingrédients',
        'ingredients.add': 'Ajouter un ingrédient',
        'ingredients.name': 'Nom',
        'ingredients.category': 'Catégorie',
        'ingredients.expiry': 'Date d\'expiration',
        'ingredients.permanent': 'Permanent',

        // Recipes
        'recipes.title': 'Générer des recettes',
        'recipes.generate': 'Générer des recettes',
        'recipes.only_available': 'Ingrédients existants uniquement',
        'recipes.servings': 'Portions',

        // Profiles
        'profiles.title': 'Préférences alimentaires',
        'profiles.strict_mode': 'Liste d\'ingrédients stricte',
        'profiles.strict_mode_hint': 'Seulement des recettes avec ingrédients existants',
        'profiles.shopping_mode': 'Mode flexible',
        'profiles.shopping_mode_hint': 'De nouveaux ingrédients seront suggérés',

        // Settings
        'settings.title': 'Paramètres',
        'settings.language': 'Langue',
        'settings.theme': 'Thème',
        'settings.account': 'Compte',
    },

    es: {
        // Auth
        'auth.login': 'Iniciar sesión',
        'auth.register': 'Registrarse',
        'auth.email_or_username': 'Correo electrónico o nombre de usuario',
        'auth.username': 'Nombre de usuario',
        'auth.email': 'Dirección de correo electrónico',
        'auth.password': 'Contraseña',
        'auth.password_min': 'Mín. 6 caracteres',
        'auth.password_confirm': 'Confirmar contraseña',
        'auth.forgot_password': '¿Olvidaste tu contraseña?',
        'auth.logout': 'Cerrar sesión',
        'auth.subtitle': 'Tu generador de recetas con IA',

        // Navigation
        'nav.ingredients': 'Mis ingredientes',
        'nav.recipes': 'Generar recetas',
        'nav.favorites': 'Mis favoritos',
        'nav.scanner': 'Escáner',
        'nav.profiles': 'Preferencias dietéticas',
        'nav.settings': 'Ajustes',

        // Common
        'common.save': 'Guardar',
        'common.cancel': 'Cancelar',
        'common.delete': 'Eliminar',
        'common.edit': 'Editar',
        'common.add': 'Añadir',
        'common.close': 'Cerrar',
        'common.loading': 'Cargando...',
        'common.search': 'Buscar',
        'common.filter': 'Filtrar',
        'common.success': '¡Éxito!',
        'common.error': 'Error',
        'common.yes': 'Sí',
        'common.no': 'No',

        // Ingredients
        'ingredients.title': 'Mis ingredientes',
        'ingredients.add': 'Añadir ingrediente',
        'ingredients.name': 'Nombre',
        'ingredients.category': 'Categoría',
        'ingredients.expiry': 'Fecha de caducidad',
        'ingredients.permanent': 'Permanente',

        // Recipes
        'recipes.title': 'Generar recetas',
        'recipes.generate': 'Generar recetas',
        'recipes.only_available': 'Solo ingredientes existentes',
        'recipes.servings': 'Porciones',

        // Profiles
        'profiles.title': 'Preferencias dietéticas',
        'profiles.strict_mode': 'Lista de ingredientes estricta',
        'profiles.strict_mode_hint': 'Solo recetas con ingredientes existentes',
        'profiles.shopping_mode': 'Modo flexible',
        'profiles.shopping_mode_hint': 'Se sugerirán nuevos ingredientes',

        // Settings
        'settings.title': 'Ajustes',
        'settings.language': 'Idioma',
        'settings.theme': 'Tema',
        'settings.account': 'Cuenta',
    },

    it: {
        // Auth
        'auth.login': 'Accedi',
        'auth.register': 'Registrati',
        'auth.email_or_username': 'Email o nome utente',
        'auth.username': 'Nome utente',
        'auth.email': 'Indirizzo email',
        'auth.password': 'Password',
        'auth.password_min': 'Min. 6 caratteri',
        'auth.password_confirm': 'Conferma password',
        'auth.forgot_password': 'Password dimenticata?',
        'auth.logout': 'Esci',
        'auth.subtitle': 'Il tuo generatore di ricette AI',

        // Navigation
        'nav.ingredients': 'I miei ingredienti',
        'nav.recipes': 'Genera ricette',
        'nav.favorites': 'I miei preferiti',
        'nav.scanner': 'Scanner',
        'nav.profiles': 'Preferenze dietetiche',
        'nav.settings': 'Impostazioni',

        // Common
        'common.save': 'Salva',
        'common.cancel': 'Annulla',
        'common.delete': 'Elimina',
        'common.edit': 'Modifica',
        'common.add': 'Aggiungi',
        'common.close': 'Chiudi',
        'common.loading': 'Caricamento...',
        'common.search': 'Cerca',
        'common.filter': 'Filtra',
        'common.success': 'Successo!',
        'common.error': 'Errore',
        'common.yes': 'Sì',
        'common.no': 'No',

        // Ingredients
        'ingredients.title': 'I miei ingredienti',
        'ingredients.add': 'Aggiungi ingrediente',
        'ingredients.name': 'Nome',
        'ingredients.category': 'Categoria',
        'ingredients.expiry': 'Data di scadenza',
        'ingredients.permanent': 'Permanente',

        // Recipes
        'recipes.title': 'Genera ricette',
        'recipes.generate': 'Genera ricette',
        'recipes.only_available': 'Solo ingredienti esistenti',
        'recipes.servings': 'Porzioni',

        // Profiles
        'profiles.title': 'Preferenze dietetiche',
        'profiles.strict_mode': 'Lista ingredienti rigorosa',
        'profiles.strict_mode_hint': 'Solo ricette con ingredienti esistenti',
        'profiles.shopping_mode': 'Modalità flessibile',
        'profiles.shopping_mode_hint': 'Verranno suggeriti nuovi ingredienti',

        // Settings
        'settings.title': 'Impostazioni',
        'settings.language': 'Lingua',
        'settings.theme': 'Tema',
        'settings.account': 'Account',
    },

    pt: {
        // Auth
        'auth.login': 'Entrar',
        'auth.register': 'Registar',
        'auth.email_or_username': 'Email ou nome de utilizador',
        'auth.username': 'Nome de utilizador',
        'auth.email': 'Endereço de email',
        'auth.password': 'Palavra-passe',
        'auth.password_min': 'Mín. 6 caracteres',
        'auth.password_confirm': 'Confirmar palavra-passe',
        'auth.forgot_password': 'Esqueceu a palavra-passe?',
        'auth.logout': 'Sair',
        'auth.subtitle': 'O seu gerador de receitas AI',

        // Navigation
        'nav.ingredients': 'Os meus ingredientes',
        'nav.recipes': 'Gerar receitas',
        'nav.favorites': 'Os meus favoritos',
        'nav.scanner': 'Scanner',
        'nav.profiles': 'Preferências dietéticas',
        'nav.settings': 'Definições',

        // Common
        'common.save': 'Guardar',
        'common.cancel': 'Cancelar',
        'common.delete': 'Eliminar',
        'common.edit': 'Editar',
        'common.add': 'Adicionar',
        'common.close': 'Fechar',
        'common.loading': 'A carregar...',
        'common.search': 'Pesquisar',
        'common.filter': 'Filtrar',
        'common.success': 'Sucesso!',
        'common.error': 'Erro',
        'common.yes': 'Sim',
        'common.no': 'Não',

        // Ingredients
        'ingredients.title': 'Os meus ingredientes',
        'ingredients.add': 'Adicionar ingrediente',
        'ingredients.name': 'Nome',
        'ingredients.category': 'Categoria',
        'ingredients.expiry': 'Data de validade',
        'ingredients.permanent': 'Permanente',

        // Recipes
        'recipes.title': 'Gerar receitas',
        'recipes.generate': 'Gerar receitas',
        'recipes.only_available': 'Apenas ingredientes existentes',
        'recipes.servings': 'Doses',

        // Profiles
        'profiles.title': 'Preferências dietéticas',
        'profiles.strict_mode': 'Lista de ingredientes rigorosa',
        'profiles.strict_mode_hint': 'Apenas receitas com ingredientes existentes',
        'profiles.shopping_mode': 'Modo flexível',
        'profiles.shopping_mode_hint': 'Novos ingredientes serão sugeridos',

        // Settings
        'settings.title': 'Definições',
        'settings.language': 'Idioma',
        'settings.theme': 'Tema',
        'settings.account': 'Conta',
    },

    sv: {
        // Auth
        'auth.login': 'Logga in',
        'auth.register': 'Registrera',
        'auth.email_or_username': 'E-post eller användarnamn',
        'auth.username': 'Användarnamn',
        'auth.email': 'E-postadress',
        'auth.password': 'Lösenord',
        'auth.password_min': 'Min. 6 tecken',
        'auth.password_confirm': 'Bekräfta lösenord',
        'auth.forgot_password': 'Glömt lösenord?',
        'auth.logout': 'Logga ut',
        'auth.subtitle': 'Din AI-receptgenerator',

        // Navigation
        'nav.ingredients': 'Mina ingredienser',
        'nav.recipes': 'Generera recept',
        'nav.favorites': 'Mina favoriter',
        'nav.scanner': 'Skanner',
        'nav.profiles': 'Dietpreferenser',
        'nav.settings': 'Inställningar',

        // Common
        'common.save': 'Spara',
        'common.cancel': 'Avbryt',
        'common.delete': 'Ta bort',
        'common.edit': 'Redigera',
        'common.add': 'Lägg till',
        'common.close': 'Stäng',
        'common.loading': 'Laddar...',
        'common.search': 'Sök',
        'common.filter': 'Filtrera',
        'common.success': 'Lyckades!',
        'common.error': 'Fel',
        'common.yes': 'Ja',
        'common.no': 'Nej',

        // Ingredients
        'ingredients.title': 'Mina ingredienser',
        'ingredients.add': 'Lägg till ingrediens',
        'ingredients.name': 'Namn',
        'ingredients.category': 'Kategori',
        'ingredients.expiry': 'Utgångsdatum',
        'ingredients.permanent': 'Permanent',

        // Recipes
        'recipes.title': 'Generera recept',
        'recipes.generate': 'Generera recept',
        'recipes.only_available': 'Endast befintliga ingredienser',
        'recipes.servings': 'Portioner',

        // Profiles
        'profiles.title': 'Dietpreferenser',
        'profiles.strict_mode': 'Strikt ingredienslista',
        'profiles.strict_mode_hint': 'Endast recept med befintliga ingredienser',
        'profiles.shopping_mode': 'Flexibelt läge',
        'profiles.shopping_mode_hint': 'Nya ingredienser kommer föreslås',

        // Settings
        'settings.title': 'Inställningar',
        'settings.language': 'Språk',
        'settings.theme': 'Tema',
        'settings.account': 'Konto',
    },

    no: {
        // Auth
        'auth.login': 'Logg inn',
        'auth.register': 'Registrer deg',
        'auth.email_or_username': 'E-post eller brukernavn',
        'auth.username': 'Brukernavn',
        'auth.email': 'E-postadresse',
        'auth.password': 'Passord',
        'auth.password_min': 'Min. 6 tegn',
        'auth.password_confirm': 'Bekreft passord',
        'auth.forgot_password': 'Glemt passord?',
        'auth.logout': 'Logg ut',
        'auth.subtitle': 'Din AI-oppskriftsgenerator',

        // Navigation
        'nav.ingredients': 'Mine ingredienser',
        'nav.recipes': 'Generer oppskrifter',
        'nav.favorites': 'Mine favoritter',
        'nav.scanner': 'Skanner',
        'nav.profiles': 'Kostpreferanser',
        'nav.settings': 'Innstillinger',

        // Common
        'common.save': 'Lagre',
        'common.cancel': 'Avbryt',
        'common.delete': 'Slett',
        'common.edit': 'Rediger',
        'common.add': 'Legg til',
        'common.close': 'Lukk',
        'common.loading': 'Laster...',
        'common.search': 'Søk',
        'common.filter': 'Filtrer',
        'common.success': 'Suksess!',
        'common.error': 'Feil',
        'common.yes': 'Ja',
        'common.no': 'Nei',

        // Ingredients
        'ingredients.title': 'Mine ingredienser',
        'ingredients.add': 'Legg til ingrediens',
        'ingredients.name': 'Navn',
        'ingredients.category': 'Kategori',
        'ingredients.expiry': 'Utløpsdato',
        'ingredients.permanent': 'Permanent',

        // Recipes
        'recipes.title': 'Generer oppskrifter',
        'recipes.generate': 'Generer oppskrifter',
        'recipes.only_available': 'Kun eksisterende ingredienser',
        'recipes.servings': 'Porsjoner',

        // Profiles
        'profiles.title': 'Kostpreferanser',
        'profiles.strict_mode': 'Streng ingrediensliste',
        'profiles.strict_mode_hint': 'Kun oppskrifter med eksisterende ingredienser',
        'profiles.shopping_mode': 'Fleksibel modus',
        'profiles.shopping_mode_hint': 'Nye ingredienser vil bli foreslått',

        // Settings
        'settings.title': 'Innstillinger',
        'settings.language': 'Språk',
        'settings.theme': 'Tema',
        'settings.account': 'Konto',
    },

    da: {
        // Auth
        'auth.login': 'Log ind',
        'auth.register': 'Tilmeld',
        'auth.email_or_username': 'E-mail eller brugernavn',
        'auth.username': 'Brugernavn',
        'auth.email': 'E-mailadresse',
        'auth.password': 'Adgangskode',
        'auth.password_min': 'Min. 6 tegn',
        'auth.password_confirm': 'Bekræft adgangskode',
        'auth.forgot_password': 'Glemt adgangskode?',
        'auth.logout': 'Log ud',
        'auth.subtitle': 'Din AI-opskriftsgenerator',

        // Navigation
        'nav.ingredients': 'Mine ingredienser',
        'nav.recipes': 'Generer opskrifter',
        'nav.favorites': 'Mine favoritter',
        'nav.scanner': 'Scanner',
        'nav.profiles': 'Kostpræferencer',
        'nav.settings': 'Indstillinger',

        // Common
        'common.save': 'Gem',
        'common.cancel': 'Annuller',
        'common.delete': 'Slet',
        'common.edit': 'Rediger',
        'common.add': 'Tilføj',
        'common.close': 'Luk',
        'common.loading': 'Indlæser...',
        'common.search': 'Søg',
        'common.filter': 'Filtrer',
        'common.success': 'Succes!',
        'common.error': 'Fejl',
        'common.yes': 'Ja',
        'common.no': 'Nej',

        // Ingredients
        'ingredients.title': 'Mine ingredienser',
        'ingredients.add': 'Tilføj ingrediens',
        'ingredients.name': 'Navn',
        'ingredients.category': 'Kategori',
        'ingredients.expiry': 'Udløbsdato',
        'ingredients.permanent': 'Permanent',

        // Recipes
        'recipes.title': 'Generer opskrifter',
        'recipes.generate': 'Generer opskrifter',
        'recipes.only_available': 'Kun eksisterende ingredienser',
        'recipes.servings': 'Portioner',

        // Profiles
        'profiles.title': 'Kostpræferencer',
        'profiles.strict_mode': 'Streng ingrediensliste',
        'profiles.strict_mode_hint': 'Kun opskrifter med eksisterende ingredienser',
        'profiles.shopping_mode': 'Fleksibel tilstand',
        'profiles.shopping_mode_hint': 'Nye ingredienser vil blive foreslået',

        // Settings
        'settings.title': 'Indstillinger',
        'settings.language': 'Sprog',
        'settings.theme': 'Tema',
        'settings.account': 'Konto',
    },

    nl: {
        // Auth
        'auth.login': 'Inloggen',
        'auth.register': 'Registreren',
        'auth.email_or_username': 'E-mail of gebruikersnaam',
        'auth.username': 'Gebruikersnaam',
        'auth.email': 'E-mailadres',
        'auth.password': 'Wachtwoord',
        'auth.password_min': 'Min. 6 tekens',
        'auth.password_confirm': 'Bevestig wachtwoord',
        'auth.forgot_password': 'Wachtwoord vergeten?',
        'auth.logout': 'Uitloggen',
        'auth.subtitle': 'Jouw AI-receptengenerator',

        // Navigation
        'nav.ingredients': 'Mijn ingrediënten',
        'nav.recipes': 'Recepten genereren',
        'nav.favorites': 'Mijn favorieten',
        'nav.scanner': 'Scanner',
        'nav.profiles': 'Dieetvoorkeuren',
        'nav.settings': 'Instellingen',

        // Common
        'common.save': 'Opslaan',
        'common.cancel': 'Annuleren',
        'common.delete': 'Verwijderen',
        'common.edit': 'Bewerken',
        'common.add': 'Toevoegen',
        'common.close': 'Sluiten',
        'common.loading': 'Laden...',
        'common.search': 'Zoeken',
        'common.filter': 'Filteren',
        'common.success': 'Succes!',
        'common.error': 'Fout',
        'common.yes': 'Ja',
        'common.no': 'Nee',

        // Ingredients
        'ingredients.title': 'Mijn ingrediënten',
        'ingredients.add': 'Ingrediënt toevoegen',
        'ingredients.name': 'Naam',
        'ingredients.category': 'Categorie',
        'ingredients.expiry': 'Vervaldatum',
        'ingredients.permanent': 'Permanent',

        // Recipes
        'recipes.title': 'Recepten genereren',
        'recipes.generate': 'Recepten genereren',
        'recipes.only_available': 'Alleen bestaande ingrediënten',
        'recipes.servings': 'Porties',

        // Profiles
        'profiles.title': 'Dieetvoorkeuren',
        'profiles.strict_mode': 'Strikte ingrediëntenlijst',
        'profiles.strict_mode_hint': 'Alleen recepten met bestaande ingrediënten',
        'profiles.shopping_mode': 'Flexibele modus',
        'profiles.shopping_mode_hint': 'Nieuwe ingrediënten worden voorgesteld',

        // Settings
        'settings.title': 'Instellingen',
        'settings.language': 'Taal',
        'settings.theme': 'Thema',
        'settings.account': 'Account',
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
