// KitchenHelper-AI API Client

class APIClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    // Token Management
    getToken() {
        return localStorage.getItem(CONFIG.TOKEN_KEY);
    }

    setToken(token) {
        localStorage.setItem(CONFIG.TOKEN_KEY, token);
    }

    clearToken() {
        localStorage.removeItem(CONFIG.TOKEN_KEY);
        localStorage.removeItem(CONFIG.USER_KEY);
    }

    // Generic Request Method
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const token = this.getToken();

        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...(token && { 'Authorization': `Bearer ${token}` })
            },
            ...options
        };

        try {
            const response = await fetch(url, config);

            // Handle 401 Unauthorized - redirect to login
            if (response.status === 401) {
                this.clearToken();
                window.location.href = 'index.html';
                throw new Error('Session expired. Please login again.');
            }

            // Handle 204 No Content
            if (response.status === 204) {
                return null;
            }

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || `Request failed with status ${response.status}`);
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);

            // Handle network errors (server not reachable)
            if (error instanceof TypeError && error.message.includes('fetch')) {
                const lang = localStorage.getItem('kitchenhelper_lang') || 'en';
                const message = lang === 'de'
                    ? 'Server nicht erreichbar. Bitte prüfe deine Verbindung.'
                    : 'Server not reachable. Please check your connection.';
                throw new Error(message);
            }

            throw error;
        }
    }

    // HTTP Methods
    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async patch(endpoint, data) {
        return this.request(endpoint, {
            method: 'PATCH',
            body: JSON.stringify(data)
        });
    }

    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}

// Create singleton instance
const api = new APIClient(CONFIG.API_BASE_URL);

// ==================== AUTH API ====================
api.register = (email, username, password) =>
    api.post('/auth/register', { email, username, password });

api.login = (emailOrUsername, password) =>
    api.post('/auth/login', { email_or_username: emailOrUsername, password });

// ==================== USERS API ====================
api.getMe = () => api.get('/users/me');

api.updateMe = (data) => api.patch('/users/me', data);

api.deleteMe = () => api.delete('/users/me');

// ==================== INGREDIENTS API ====================
api.getIngredients = (params = {}) => {
    const query = new URLSearchParams();
    if (params.category) query.append('category', params.category);
    if (params.expired !== undefined) query.append('expired', params.expired);
    const queryString = query.toString();
    return api.get(`/ingredients/${queryString ? '?' + queryString : ''}`);
};

api.createIngredient = (data) => api.post('/ingredients/', data);

api.updateIngredient = (id, data) => api.patch(`/ingredients/${id}`, data);

api.deleteIngredient = (id) => api.delete(`/ingredients/${id}`);

api.createBatchIngredients = (ingredients) => api.post('/ingredients/batch', { ingredients });

// ==================== RECIPES API ====================
api.generateRecipes = (data) => api.post('/recipes/generate', data);

api.getRecipeHistory = (limit = 20, offset = 0) =>
    api.get(`/recipes/history?limit=${limit}&offset=${offset}`);

api.getRecipe = (id) => api.get(`/recipes/${id}`);

api.calculatePortions = (recipeId, servings) => api.get(`/recipes/${recipeId}/portions?servings=${servings}`);

// ==================== FAVORITES API ====================
api.getFavorites = () => api.get('/favorites/');

api.addFavorite = (recipeId) => api.post('/favorites/', { recipe_id: recipeId });

api.removeFavorite = (id) => api.delete(`/favorites/${id}`);

api.checkFavorite = (recipeId) => api.get(`/favorites/check/${recipeId}`);

// ==================== DIET PROFILES API ====================
api.getProfiles = (active = null) => {
    const query = active !== null ? `?active=${active}` : '';
    return api.get(`/profiles/${query}`);
};

api.getProfileTemplates = () => api.get('/profiles/templates');

api.createProfile = (data) => api.post('/profiles/', data);

api.createProfileFromTemplate = (profileType) =>
    api.post(`/profiles/templates/${profileType}`, {});

api.updateProfile = (id, data) => api.patch(`/profiles/${id}`, data);

api.deleteProfile = (id) => api.delete(`/profiles/${id}`);

// ==================== SHOPPING LIST API ====================
api.generateShoppingList = (recipeIds = [], favoriteIds = [], scaleFactor = 1.0) =>
    api.post('/shopping-list/generate', {
        recipe_ids: recipeIds,
        favorite_ids: favoriteIds,
        scale_factor: scaleFactor
    });

api.exportShoppingListText = async (recipeIds = [], favoriteIds = [], scaleFactor = 1.0) => {
    const token = api.getToken();
    const response = await fetch(`${CONFIG.API_BASE_URL}/shopping-list/export/text`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            recipe_ids: recipeIds,
            favorite_ids: favoriteIds,
            scale_factor: scaleFactor
        })
    });
    return response.blob();
};

api.exportShoppingListJson = async (recipeIds = [], favoriteIds = [], scaleFactor = 1.0) => {
    const token = api.getToken();
    const response = await fetch(`${CONFIG.API_BASE_URL}/shopping-list/export/json`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            recipe_ids: recipeIds,
            favorite_ids: favoriteIds,
            scale_factor: scaleFactor
        })
    });
    return response.blob();
};

// ==================== SHARE API ====================
api.createShareLink = (recipeId = null, favoriteId = null, expiresHours = 168) =>
    api.post('/share/create', {
        recipe_id: recipeId,
        favorite_id: favoriteId,
        expires_hours: expiresHours
    });

api.getSharedRecipe = (shareId) => api.get(`/share/${shareId}`);

api.revokeShareLink = (shareId) => api.delete(`/share/${shareId}`);

api.getMyShareLinks = () => api.get('/share/my/links');

// ==================== NUTRITION API ====================
api.lookupNutrition = (ingredient) =>
    api.get(`/nutrition/lookup?ingredient=${encodeURIComponent(ingredient)}`);

api.bulkNutritionLookup = (ingredients) =>
    api.post('/nutrition/bulk', { ingredients });

api.calculateMealNutrition = (ingredientsString, servings = 1) =>
    api.get(`/nutrition/calculate-meal?ingredients=${encodeURIComponent(ingredientsString)}&servings=${servings}`);
