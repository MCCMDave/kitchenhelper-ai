// KitchenHelper-AI Configuration
const CONFIG = {
    // API Settings - Auto-detect environment with HTTPS enforcement
    API_BASE_URL: (() => {
        // Check if accessing via Tailscale, Pi IP, or localhost
        const hostname = window.location.hostname;

        // SECURITY: Enforce HTTPS for production domains
        if (hostname.includes('.de') || hostname.includes('cloudflare')) {
            // Production: ALWAYS use HTTPS via Cloudflare
            return 'https://api.kitchenhelper-ai.de/api';
        } else if (hostname === '100.103.86.47') {
            // Tailscale IP: Use local Pi backend (httpOnly cookies work same-site)
            return 'http://192.168.2.54:8000/api';
        } else if (hostname === '192.168.2.54') {
            // Local network IP: Use local Pi backend (httpOnly cookies work same-site)
            return 'http://192.168.2.54:8000/api';
        } else {
            // Localhost development: Use local backend
            return 'http://127.0.0.1:8000/api';
        }
    })(),

    // LocalStorage Keys
    TOKEN_KEY: 'kitchenhelper_token',
    USER_KEY: 'kitchenhelper_user',

    // App Settings
    APP_NAME: 'KitchenHelper-AI',
    APP_VERSION: '1.0.0',

    // Diet Profile Types (value is key, labels are translated)
    PROFILE_TYPES: [
        { value: 'diabetic', label_de: 'Diabetiker', label_en: 'Diabetic', emoji: '💉' },
        { value: 'gluten_free', label_de: 'Glutenfrei', label_en: 'Gluten-free', emoji: '🌾' },
        { value: 'high_protein', label_de: 'High Protein', label_en: 'High Protein', emoji: '💪' },
        { value: 'keto', label_de: 'Keto', label_en: 'Keto', emoji: '🥑' },
        { value: 'lactose_free', label_de: 'Laktosefrei', label_en: 'Lactose-free', emoji: '🥛' },
        { value: 'low_carb', label_de: 'Low Carb', label_en: 'Low Carb', emoji: '🥗' },
        { value: 'vegan', label_de: 'Vegan', label_en: 'Vegan', emoji: '🌱' },
        { value: 'vegetarian', label_de: 'Vegetarisch', label_en: 'Vegetarian', emoji: '🥕' },
        // Additional dietary preferences
        { value: 'paleo', label_de: 'Paleo', label_en: 'Paleo', emoji: '🦴' },
        { value: 'low_fodmap', label_de: 'Low FODMAP', label_en: 'Low FODMAP', emoji: '🌾' },
        { value: 'kosher', label_de: 'Koscher', label_en: 'Kosher', emoji: '✡️' },
        { value: 'halal', label_de: 'Halal', label_en: 'Halal', emoji: '☪️' },
        { value: 'histamine_free', label_de: 'Histaminarm', label_en: 'Low Histamine', emoji: '🧪' },
        { value: 'nut_free', label_de: 'Nussfrei', label_en: 'Nut-free', emoji: '🚫🥜' },
        { value: 'pescatarian', label_de: 'Pescetarisch', label_en: 'Pescatarian', emoji: '🐟' },
        { value: 'pregnancy', label_de: 'Schwangerschaft', label_en: 'Pregnancy', emoji: '🤰' },
        { value: 'mediterranean', label_de: 'Mittelmeer', label_en: 'Mediterranean', emoji: '🫒' }
    ],

    // Ingredient Categories (translated) - sorted alphabetically per language
    CATEGORIES_DE: [
        'Fisch', 'Fleisch', 'Gemüse', 'Getränke', 'Getreide', 'Gewürze',
        'Kohlenhydrate', 'Milchprodukte', 'Nüsse & Samen', 'Obst',
        'Öle & Fette', 'Saucen', 'Sonstiges'
    ].sort((a, b) => a.localeCompare(b, 'de')),

    CATEGORIES_EN: [
        'Beverages', 'Carbohydrates', 'Dairy', 'Fish', 'Fruits', 'Grains',
        'Meat', 'Nuts & Seeds', 'Oils & Fats', 'Other', 'Sauces', 'Spices',
        'Vegetables'
    ],

    // Category mapping DE -> EN for backend storage
    CATEGORY_MAP_DE_EN: {
        'Fisch': 'Fish', 'Fleisch': 'Meat', 'Gemüse': 'Vegetables',
        'Getränke': 'Beverages', 'Getreide': 'Grains', 'Gewürze': 'Spices',
        'Kohlenhydrate': 'Carbohydrates', 'Milchprodukte': 'Dairy',
        'Nüsse & Samen': 'Nuts & Seeds', 'Obst': 'Fruits',
        'Öle & Fette': 'Oils & Fats', 'Saucen': 'Sauces', 'Sonstiges': 'Other'
    },

    // Category mapping EN -> DE for display
    CATEGORY_MAP_EN_DE: {
        'Fish': 'Fisch', 'Meat': 'Fleisch', 'Vegetables': 'Gemüse',
        'Beverages': 'Getränke', 'Grains': 'Getreide', 'Spices': 'Gewürze',
        'Carbohydrates': 'Kohlenhydrate', 'Dairy': 'Milchprodukte',
        'Nuts & Seeds': 'Nüsse & Samen', 'Fruits': 'Obst',
        'Oils & Fats': 'Öle & Fette', 'Sauces': 'Saucen', 'Other': 'Sonstiges'
    },

    // Get categories based on current language (sorted alphabetically)
    getCategories() {
        const lang = localStorage.getItem('kitchenhelper_lang') || 'en';
        return lang === 'de' ? this.CATEGORIES_DE : this.CATEGORIES_EN;
    },

    // Translate category to current language for display
    translateCategory(category) {
        const lang = localStorage.getItem('kitchenhelper_lang') || 'en';
        if (lang === 'de') {
            return this.CATEGORY_MAP_EN_DE[category] || category;
        }
        return this.CATEGORY_MAP_DE_EN[category] || category;
    },

    // Get profile types with translated labels
    getProfileTypes() {
        const lang = localStorage.getItem('kitchenhelper_lang') || 'en';
        return this.PROFILE_TYPES.map(p => ({
            value: p.value,
            label: lang === 'de' ? p.label_de : p.label_en,
            emoji: p.emoji
        })).sort((a, b) => a.label.localeCompare(b.label));
    },

    // Legacy: CATEGORIES getter for backwards compatibility
    get CATEGORIES() {
        return this.getCategories();
    },

    // Subscription Tiers
    TIERS: {
        demo: { name: 'Demo', recipes: 3, favorites: 5, profiles: 3 },
        basic: { name: 'Basic', recipes: 50, favorites: 50, profiles: 5 },
        premium: { name: 'Premium', recipes: 'Unlimited', favorites: 'Unlimited', profiles: 'Unlimited' }
    }
};
