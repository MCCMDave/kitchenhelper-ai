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
        'auth.password_confirm': 'Passwort bestaetigen',
        'auth.password_repeat': 'Passwort wiederholen',
        'auth.forgot_password': 'Passwort vergessen?',
        'auth.logout': 'Abmelden',
        'auth.demo_hint': 'Demo-Account: Registriere dich kostenlos!',
        'auth.subtitle': 'Dein KI-Rezeptgenerator',

        // Password Reset
        'reset.title': 'Passwort zuruecksetzen',
        'reset.step1_text': 'Gib deine E-Mail-Adresse ein, um einen Reset-Code zu erhalten.',
        'reset.request_code': 'Reset-Code anfordern',
        'reset.step2_text': 'Gib den Reset-Code und dein neues Passwort ein.',
        'reset.code': 'Reset-Code',
        'reset.code_placeholder': 'Code aus der Console/Email',
        'reset.new_password': 'Neues Passwort',
        'reset.change_password': 'Passwort aendern',
        'reset.back': 'Zurueck',
        'reset.success': 'Passwort erfolgreich geaendert!',
        'reset.success_hint': 'Du kannst dich jetzt mit deinem neuen Passwort anmelden.',
        'reset.to_login': 'Zum Login',

        // Errors
        'error.invalid_email': 'Bitte gib eine gueltige E-Mail-Adresse ein.',
        'error.password_too_short': 'Passwort muss mindestens 6 Zeichen lang sein.',
        'error.passwords_not_match': 'Die Passwoerter stimmen nicht ueberein.',
        'error.username_too_short': 'Benutzername muss mindestens 3 Zeichen lang sein.',
        'error.username_invalid': 'Benutzername darf nur Buchstaben, Zahlen, - und _ enthalten.',
        'error.login_failed': 'Anmeldung fehlgeschlagen. Bitte pruefe deine Daten.',
        'error.registration_failed': 'Registrierung fehlgeschlagen.',
        'error.email_taken': 'Diese E-Mail ist bereits registriert.',
        'error.username_taken': 'Dieser Benutzername ist bereits vergeben.',
        'error.fetch_failed': 'Verbindungsfehler. Ist der Server gestartet?',
        'error.reset_code_required': 'Bitte gib den Reset-Code ein.',

        // Dashboard Navigation
        'nav.ingredients': 'Zutaten',
        'nav.recipes': 'Rezepte',
        'nav.favorites': 'Favoriten',
        'nav.profiles': 'Profile',
        'nav.settings': 'Einstellungen',

        // Ingredients
        'ingredients.title': 'Meine Zutaten',
        'ingredients.add': 'Zutat hinzufuegen',
        'ingredients.name': 'Name',
        'ingredients.category': 'Kategorie',
        'ingredients.all_categories': 'Alle Kategorien',
        'ingredients.expiry': 'Ablaufdatum',
        'ingredients.permanent': 'Dauerhaft',
        'ingredients.edit': 'Bearbeiten',
        'ingredients.delete': 'Loeschen',
        'ingredients.expired': 'Abgelaufen',

        // Recipes
        'recipes.title': 'Rezepte generieren',
        'recipes.select_ingredients': 'Waehle deine Zutaten',
        'recipes.generate': 'Rezepte generieren',
        'recipes.generated': 'Generierte Rezepte',
        'recipes.history': 'Letzte Rezepte',
        'recipes.selected': 'Zutaten ausgewaehlt',

        // Favorites
        'favorites.title': 'Meine Favoriten',
        'favorites.empty': 'Keine Favoriten vorhanden. Fuege Rezepte zu deinen Favoriten hinzu!',
        'favorites.remove': 'Aus Favoriten entfernen',
        'favorites.details': 'Details',
        'favorites.less': 'Weniger',
        'favorites.export_pdf': 'Als PDF exportieren',
        'favorites.added': 'Hinzugefuegt',
        'favorites.used_ingredients': 'Verwendete Zutaten',
        'favorites.all_ingredients': 'Alle Zutaten',
        'favorites.leftover_tips': 'Reste-Tipps',
        'favorites.nutrition': 'Naehrwerte pro Portion',
        'favorites.confirm_remove': 'Favorit wirklich entfernen?',
        'favorites.removed': 'Favorit entfernt!',
        'favorites.pdf_creating': 'PDF wird erstellt...',
        'favorites.pdf_success': 'PDF erfolgreich heruntergeladen!',
        'favorites.pdf_error': 'Fehler beim PDF-Export',

        // Profiles
        'profiles.title': 'Ernaehrungsprofile',
        'profiles.add': 'Profil hinzufuegen',
        'profiles.all_added': 'Alle Profile bereits hinzugefuegt!',
        'profiles.new': 'Neues Ernaehrungsprofil',
        'profiles.type': 'Profil-Typ',
        'profiles.name': 'Name',
        'profiles.name_placeholder': 'z.B. Mein Diabetes Profil',
        'profiles.activate_now': 'Sofort aktivieren',
        'recipes.select_warning': 'Bitte waehle mindestens eine Zutat aus!',

        // Settings
        'settings.title': 'Einstellungen',
        'settings.profile': 'Profil bearbeiten',
        'settings.avatar_emoji': 'Avatar-Emoji',
        'settings.change_password': 'Passwort aendern',
        'settings.new_password': 'Neues Passwort',
        'settings.confirm_password': 'Passwort bestaetigen',
        'settings.account_info': 'Account-Info',
        'settings.danger_zone': 'Gefahrenzone',
        'settings.danger_warning': 'Achtung: Diese Aktion kann nicht rueckgaengig gemacht werden!',
        'settings.delete_account': 'Account loeschen',

        // Common
        'common.save': 'Speichern',
        'common.cancel': 'Abbrechen',
        'common.delete': 'Loeschen',
        'common.edit': 'Bearbeiten',
        'common.close': 'Schliessen',
        'common.loading': 'Laden...',
        'common.success': 'Erfolgreich!',
        'common.error': 'Fehler',
        'common.yes': 'Ja',
        'common.no': 'Nein',
        'common.confirm': 'Bestaetigung',
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
        'error.fetch_failed': 'Connection error. Is the server running?',
        'error.reset_code_required': 'Please enter the reset code.',

        // Dashboard Navigation
        'nav.ingredients': 'Ingredients',
        'nav.recipes': 'Recipes',
        'nav.favorites': 'Favorites',
        'nav.profiles': 'Profiles',
        'nav.settings': 'Settings',

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

        // Recipes
        'recipes.title': 'Generate Recipes',
        'recipes.select_ingredients': 'Select your ingredients',
        'recipes.generate': 'Generate Recipes',
        'recipes.generated': 'Generated Recipes',
        'recipes.history': 'Recent Recipes',
        'recipes.selected': 'ingredients selected',

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
        'profiles.title': 'Diet Profiles',
        'profiles.add': 'Add Profile',
        'profiles.all_added': 'All profiles already added!',
        'profiles.new': 'New Diet Profile',
        'profiles.type': 'Profile Type',
        'profiles.name': 'Name',
        'profiles.name_placeholder': 'e.g. My Diabetes Profile',
        'profiles.activate_now': 'Activate immediately',
        'recipes.select_warning': 'Please select at least one ingredient!',

        // Settings
        'settings.title': 'Settings',
        'settings.profile': 'Edit Profile',
        'settings.avatar_emoji': 'Avatar Emoji',
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
    }
};

const i18n = {
    currentLang: localStorage.getItem('kitchenhelper_lang') || 'en',

    init() {
        this.setLanguage(this.currentLang, false);
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

        console.log('[i18n] Language set to:', lang);
    },

    toggle() {
        const newLang = this.currentLang === 'de' ? 'en' : 'de';
        this.setLanguage(newLang);
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

        console.log('[i18n] UI updated');
    }
};

// Auto-init when DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => i18n.init());
} else {
    i18n.init();
}
