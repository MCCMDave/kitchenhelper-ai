// KitchenHelper-AI Favorites Module

const Favorites = {
    items: [],
    favoriteIds: new Set(), // Cache fuer schnelle Lookups
    expandedIds: new Set(), // Track welche Cards expanded sind

    // Load all favorites and build cache
    async load() {
        const container = document.getElementById('favorites-list');
        UI.showLoading(container);

        try {
            console.log('[Favorites] Loading favorites...');
            const response = await api.getFavorites();
            console.log('[Favorites] API Response:', response);

            // Handle both response formats: {favorites: [...]} or direct array
            if (Array.isArray(response)) {
                this.items = response;
            } else if (response && response.favorites) {
                this.items = response.favorites;
            } else {
                this.items = [];
            }

            console.log('[Favorites] Parsed items:', this.items);

            // Build favoriteIds cache for quick lookups
            this.favoriteIds.clear();
            this.items.forEach(fav => {
                if (fav.recipe && fav.recipe.id) {
                    this.favoriteIds.add(fav.recipe.id);
                }
            });
            console.log('[Favorites] Cache built with', this.favoriteIds.size, 'recipe IDs');

            this.render();
        } catch (error) {
            console.error('[Favorites] Load error:', error);
            UI.showError(container, 'Fehler beim Laden: ' + error.message);
        }
    },

    // Render favorites list
    render() {
        const container = document.getElementById('favorites-list');

        if (!this.items || this.items.length === 0) {
            UI.showEmpty(container, 'Keine Favoriten vorhanden. Füge Rezepte zu deinen Favoriten hinzu!', '⭐');
            return;
        }

        console.log('[Favorites] Rendering', this.items.length, 'items');
        container.innerHTML = this.items.map(fav => this.renderCard(fav)).join('');
    },

    // Toggle expand/collapse for a favorite card
    toggleCard(favoriteId, event) {
        // Prevent toggle when clicking remove button
        if (event && event.target.closest('.favorite-remove-btn')) {
            return;
        }

        const card = document.querySelector(`[data-favorite-id="${favoriteId}"]`);
        if (!card) return;

        if (this.expandedIds.has(favoriteId)) {
            this.expandedIds.delete(favoriteId);
            card.classList.remove('expanded');
            card.classList.add('collapsed');
        } else {
            this.expandedIds.add(favoriteId);
            card.classList.remove('collapsed');
            card.classList.add('expanded');
        }

        console.log('[Favorites] Toggle card:', favoriteId, 'expanded:', this.expandedIds.has(favoriteId));
    },

    // Render single favorite card - KOMPAKT mit expand/collapse
    renderCard(favorite) {
        console.log('[Favorites] Rendering card for:', favorite);
        const recipe = favorite.recipe;

        if (!recipe) {
            console.warn('[Favorites] No recipe data for favorite:', favorite.id);
            return `
                <div class="favorite-card collapsed" data-favorite-id="${favorite.id}">
                    <div class="favorite-header">
                        <h3 class="favorite-title">Rezept nicht verfuegbar</h3>
                        <button class="favorite-remove-btn" onclick="event.stopPropagation(); Favorites.remove(${favorite.id})" title="Entfernen">
                            ✕
                        </button>
                    </div>
                    <div class="favorite-meta-compact">ID: ${favorite.recipe_id}</div>
                </div>
            `;
        }

        // Parse ingredients und nutrition (koennen bereits Objekte oder Strings sein)
        let ingredients = recipe.ingredients || [];
        let nutrition = recipe.nutrition_per_serving || {};
        let usedIngredients = recipe.used_ingredients || [];

        // Falls noch Strings (sollte nicht mehr vorkommen nach Backend-Fix)
        if (typeof ingredients === 'string') {
            try { ingredients = JSON.parse(ingredients); } catch (e) { ingredients = []; }
        }
        if (typeof nutrition === 'string') {
            try { nutrition = JSON.parse(nutrition); } catch (e) { nutrition = {}; }
        }
        if (typeof usedIngredients === 'string') {
            try { usedIngredients = JSON.parse(usedIngredients); } catch (e) { usedIngredients = []; }
        }

        // Ingredients List HTML
        const ingredientsList = ingredients.map(ing =>
            `<li>${UI.escapeHtml(ing.amount || '')} ${UI.escapeHtml(ing.name || '')}</li>`
        ).join('');

        // Difficulty emoji
        const difficultyEmoji = recipe.difficulty <= 2 ? '⚡' : recipe.difficulty <= 3 ? '⚡⚡' : '⚡⚡⚡';

        // Check if expanded
        const isExpanded = this.expandedIds.has(favorite.id);
        const cardClass = isExpanded ? 'expanded' : 'collapsed';

        return `
            <div class="favorite-card ${cardClass}" data-favorite-id="${favorite.id}" onclick="Favorites.toggleCard(${favorite.id}, event)">
                <div class="favorite-header">
                    <h3 class="favorite-title">${UI.escapeHtml(recipe.name)}</h3>
                    <button class="favorite-remove-btn" onclick="event.stopPropagation(); Favorites.remove(${favorite.id})" title="Aus Favoriten entfernen">
                        ✕
                    </button>
                </div>

                <div class="favorite-meta-compact">
                    <span>⏱️ ${recipe.cooking_time || '?'}</span>
                    <span>${difficultyEmoji}</span>
                    <span>👥 ${recipe.servings || 2}</span>
                </div>

                <div class="favorite-expand-hint">
                    <span class="expand-icon">${isExpanded ? '▲' : '▼'}</span>
                    <span>${isExpanded ? 'Weniger' : 'Details'}</span>
                </div>

                <!-- Details (nur bei expanded sichtbar) -->
                <div class="favorite-details">
                    ${recipe.description ? `
                        <div class="favorite-description">
                            <p>${UI.escapeHtml(recipe.description)}</p>
                        </div>
                    ` : ''}

                    ${usedIngredients.length > 0 ? `
                        <div class="favorite-section">
                            <h4>Verwendete Zutaten</h4>
                            <p>${usedIngredients.map(i => UI.escapeHtml(i)).join(', ')}</p>
                        </div>
                    ` : ''}

                    ${ingredients.length > 0 ? `
                        <div class="favorite-section">
                            <h4>Alle Zutaten</h4>
                            <ul class="favorite-ingredients-list">${ingredientsList}</ul>
                        </div>
                    ` : ''}

                    ${recipe.leftover_tips ? `
                        <div class="favorite-section">
                            <h4>Reste-Tipps</h4>
                            <p style="font-style: italic;">${UI.escapeHtml(recipe.leftover_tips)}</p>
                        </div>
                    ` : ''}

                    ${nutrition && Object.keys(nutrition).length > 0 ? `
                        <div class="favorite-section">
                            <h4>Naehrwerte pro Portion</h4>
                            <div class="favorite-nutrition">
                                ${nutrition.calories ? `<div class="nutrition-item"><span class="nutrition-value">${nutrition.calories}</span><span class="nutrition-label">kcal</span></div>` : ''}
                                ${nutrition.protein ? `<div class="nutrition-item"><span class="nutrition-value">${nutrition.protein}g</span><span class="nutrition-label">Protein</span></div>` : ''}
                                ${nutrition.carbs ? `<div class="nutrition-item"><span class="nutrition-value">${nutrition.carbs}g</span><span class="nutrition-label">Carbs</span></div>` : ''}
                                ${nutrition.fat ? `<div class="nutrition-item"><span class="nutrition-value">${nutrition.fat}g</span><span class="nutrition-label">Fett</span></div>` : ''}
                                ${nutrition.ke ? `<div class="nutrition-item"><span class="nutrition-value">${nutrition.ke}</span><span class="nutrition-label">KE</span></div>` : ''}
                                ${nutrition.be && !nutrition.ke ? `<div class="nutrition-item"><span class="nutrition-value">${nutrition.be}</span><span class="nutrition-label">BE</span></div>` : ''}
                            </div>
                        </div>
                    ` : ''}

                    <div class="favorite-footer">
                        <small>Hinzugefuegt: ${UI.formatDate(favorite.added_at)}</small>
                    </div>
                </div>
            </div>
        `;
    },

    // Remove favorite
    async remove(favoriteId) {
        UI.confirm('Favorit wirklich entfernen?', async () => {
            try {
                console.log('[Favorites] Removing favorite:', favoriteId);
                await api.removeFavorite(favoriteId);

                // Update cache
                const fav = this.items.find(f => f.id === favoriteId);
                if (fav && fav.recipe) {
                    this.favoriteIds.delete(fav.recipe.id);
                }

                UI.success('Favorit entfernt!');
                await this.load();
            } catch (error) {
                console.error('[Favorites] Remove error:', error);
                UI.error('Fehler: ' + error.message);
            }
        });
    },

    // Check if recipe is favorited (quick cache lookup)
    isFavorite(recipeId) {
        return this.favoriteIds.has(recipeId);
    },

    // Toggle favorite status for a recipe
    async toggle(recipeId) {
        try {
            const isFavorite = this.favoriteIds.has(recipeId);

            if (isFavorite) {
                // Find favorite and remove
                const fav = this.items.find(f => f.recipe && f.recipe.id === recipeId);
                if (fav) {
                    console.log('[Favorites] Removing favorite for recipe:', recipeId);
                    await api.removeFavorite(fav.id);
                    this.favoriteIds.delete(recipeId);
                    this.items = this.items.filter(f => f.id !== fav.id);
                    UI.success('Aus Favoriten entfernt!');
                }
            } else {
                // Add as favorite
                console.log('[Favorites] Adding favorite for recipe:', recipeId);
                const newFav = await api.addFavorite(recipeId);
                this.favoriteIds.add(recipeId);
                this.items.unshift(newFav);
                UI.success('Zu Favoriten hinzugefuegt!');
            }

            return !isFavorite; // Return new state
        } catch (error) {
            console.error('[Favorites] Toggle error:', error);
            UI.error('Fehler: ' + error.message);
            throw error;
        }
    }
};
