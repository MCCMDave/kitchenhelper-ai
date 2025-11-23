// KitchenHelper-AI Configuration
const CONFIG = {
    // API Settings
    API_BASE_URL: 'http://127.0.0.1:8000/api',

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
        { value: 'vegetarian', label_de: 'Vegetarisch', label_en: 'Vegetarian', emoji: '🥕' }
    ],

    // Ingredient Categories (translated)
    CATEGORIES_DE: [
        'Fisch', 'Fleisch', 'Gemüse', 'Getränke', 'Getreide', 'Gewürze',
        'Kohlenhydrate', 'Milchprodukte', 'Nüsse & Samen', 'Obst',
        'Öle & Fette', 'Saucen', 'Sonstiges'
    ],

    CATEGORIES_EN: [
        'Fish', 'Meat', 'Vegetables', 'Beverages', 'Grains', 'Spices',
        'Carbohydrates', 'Dairy', 'Nuts & Seeds', 'Fruits',
        'Oils & Fats', 'Sauces', 'Other'
    ],

    // Get categories based on current language
    getCategories() {
        const lang = localStorage.getItem('kitchenhelper_lang') || 'en';
        return lang === 'de' ? this.CATEGORIES_DE : this.CATEGORIES_EN;
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
        demo: { name: 'Demo', recipes: 3, favorites: 5, profiles: 1 },
        basic: { name: 'Basic', recipes: 50, favorites: 50, profiles: 3 },
        premium: { name: 'Premium', recipes: 'Unlimited', favorites: 'Unlimited', profiles: 'Unlimited' }
    }
};
