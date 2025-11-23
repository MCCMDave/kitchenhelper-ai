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

    // Diet Profile Types - Alphabetisch sortiert
    PROFILE_TYPES: [
        { value: 'diabetic', label: 'Diabetiker', emoji: '💉' },
        { value: 'gluten_free', label: 'Glutenfrei', emoji: '🌾' },
        { value: 'high_protein', label: 'High Protein', emoji: '💪' },
        { value: 'keto', label: 'Keto', emoji: '🥑' },
        { value: 'lactose_free', label: 'Laktosefrei', emoji: '🥛' },
        { value: 'low_carb', label: 'Low Carb', emoji: '🥗' },
        { value: 'vegan', label: 'Vegan', emoji: '🌱' },
        { value: 'vegetarian', label: 'Vegetarisch', emoji: '🥕' }
    ].sort((a, b) => a.label.localeCompare(b.label, 'de')),

    // Ingredient Categories - Alphabetisch sortiert
    CATEGORIES: [
        'Fisch',
        'Fleisch',
        'Gemüse',
        'Getränke',
        'Getreide',
        'Gewürze',
        'Kohlenhydrate',
        'Milchprodukte',
        'Nüsse & Samen',
        'Obst',
        'Öle & Fette',
        'Saucen',
        'Sonstiges'
    ].sort((a, b) => a.localeCompare(b, 'de')),

    // Subscription Tiers
    TIERS: {
        demo: { name: 'Demo', recipes: 3, favorites: 5, profiles: 1 },
        basic: { name: 'Basic', recipes: 50, favorites: 50, profiles: 3 },
        premium: { name: 'Premium', recipes: 'Unbegrenzt', favorites: 'Unbegrenzt', profiles: 'Unbegrenzt' }
    }
};
