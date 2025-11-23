// KitchenHelper-AI Favorites Module

const Favorites = {
    items: [],
    favoriteIds: new Set(), // Cache for quick lookups

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
            UI.showError(container, 'Error loading: ' + error.message);
        }
    },

    // Render favorites list as compact cards
    render() {
        const container = document.getElementById('favorites-list');

        if (!this.items || this.items.length === 0) {
            UI.showEmpty(container, i18n.t('favorites.empty'), '⭐');
            return;
        }

        console.log('[Favorites] Rendering', this.items.length, 'items');
        container.innerHTML = this.items.map(fav => this.renderCard(fav)).join('');
    },

    // Render compact favorite card (click opens modal)
    renderCard(favorite) {
        const recipe = favorite.recipe;

        if (!recipe) {
            return `
                <div class="favorite-card" data-favorite-id="${favorite.id}">
                    <div class="favorite-header">
                        <h3 class="favorite-title">Recipe unavailable</h3>
                        <button class="favorite-remove-btn" onclick="event.stopPropagation(); Favorites.remove(${favorite.id})" title="Remove">
                            ✕
                        </button>
                    </div>
                    <div class="favorite-meta-compact">ID: ${favorite.recipe_id}</div>
                </div>
            `;
        }

        // Difficulty display
        const difficultyEmoji = recipe.difficulty <= 2 ? '⚡' : recipe.difficulty <= 3 ? '⚡⚡' : '⚡⚡⚡';

        return `
            <div class="favorite-card" data-favorite-id="${favorite.id}" onclick="Favorites.showModal(${favorite.id})">
                <div class="favorite-header">
                    <h3 class="favorite-title">${UI.escapeHtml(recipe.name)}</h3>
                    <button class="favorite-remove-btn" onclick="event.stopPropagation(); Favorites.remove(${favorite.id})" title="${i18n.t('favorites.remove')}">
                        ✕
                    </button>
                </div>

                <div class="favorite-meta-compact">
                    <span>⏱️ ${recipe.cooking_time || '?'}</span>
                    <span>${difficultyEmoji}</span>
                    <span>👥 ${recipe.servings || 2}</span>
                </div>

                <div class="favorite-expand-hint">
                    <span>📖 ${i18n.t('favorites.details')}</span>
                </div>
            </div>
        `;
    },

    // Show favorite details in modal
    showModal(favoriteId) {
        const favorite = this.items.find(f => f.id === favoriteId);
        if (!favorite || !favorite.recipe) {
            UI.error('Recipe not found');
            return;
        }

        const recipe = favorite.recipe;

        // Parse data
        let ingredients = recipe.ingredients || [];
        let nutrition = recipe.nutrition_per_serving || {};
        let usedIngredients = recipe.used_ingredients || [];

        if (typeof ingredients === 'string') {
            try { ingredients = JSON.parse(ingredients); } catch (e) { ingredients = []; }
        }
        if (typeof nutrition === 'string') {
            try { nutrition = JSON.parse(nutrition); } catch (e) { nutrition = {}; }
        }
        if (typeof usedIngredients === 'string') {
            try { usedIngredients = JSON.parse(usedIngredients); } catch (e) { usedIngredients = []; }
        }

        // Build modal content
        const modalContent = `
            <div class="favorite-modal-content">
                ${recipe.description ? `
                    <p class="favorite-modal-description">${UI.escapeHtml(recipe.description)}</p>
                ` : ''}

                <div class="favorite-modal-meta">
                    <div class="meta-item">
                        <span class="meta-icon">⏱️</span>
                        <span>${recipe.cooking_time || '-'}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-icon">📊</span>
                        <span>${'⭐'.repeat(recipe.difficulty || 1)}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-icon">👥</span>
                        <span>${recipe.servings || 2} servings</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-icon">🍳</span>
                        <span>${recipe.method || '-'}</span>
                    </div>
                </div>

                ${usedIngredients.length > 0 ? `
                    <div class="favorite-modal-section">
                        <h4>${i18n.t('favorites.used_ingredients')}</h4>
                        <p class="used-ingredients-list">${usedIngredients.map(i => UI.escapeHtml(i)).join(', ')}</p>
                    </div>
                ` : ''}

                ${ingredients.length > 0 ? `
                    <div class="favorite-modal-section">
                        <h4>${i18n.t('favorites.all_ingredients')}</h4>
                        <ul class="ingredients-list">
                            ${ingredients.map(ing => `<li>${UI.escapeHtml(ing.amount || '')} ${UI.escapeHtml(ing.name || '')}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}

                ${recipe.leftover_tips ? `
                    <div class="favorite-modal-section">
                        <h4>${i18n.t('favorites.leftover_tips')}</h4>
                        <p class="leftover-tips">${UI.escapeHtml(recipe.leftover_tips)}</p>
                    </div>
                ` : ''}

                ${nutrition && Object.keys(nutrition).length > 0 ? `
                    <div class="favorite-modal-section">
                        <h4>${i18n.t('favorites.nutrition')}</h4>
                        <div class="nutrition-grid">
                            ${nutrition.calories ? `<div class="nutrition-item"><span class="nutrition-value">${nutrition.calories}</span><span class="nutrition-label">kcal</span></div>` : ''}
                            ${nutrition.protein ? `<div class="nutrition-item"><span class="nutrition-value">${nutrition.protein}g</span><span class="nutrition-label">Protein</span></div>` : ''}
                            ${nutrition.carbs ? `<div class="nutrition-item"><span class="nutrition-value">${nutrition.carbs}g</span><span class="nutrition-label">Carbs</span></div>` : ''}
                            ${nutrition.fat ? `<div class="nutrition-item"><span class="nutrition-value">${nutrition.fat}g</span><span class="nutrition-label">Fat</span></div>` : ''}
                            ${nutrition.ke ? `<div class="nutrition-item"><span class="nutrition-value">${nutrition.ke}</span><span class="nutrition-label">KE</span></div>` : ''}
                            ${nutrition.be && !nutrition.ke ? `<div class="nutrition-item"><span class="nutrition-value">${nutrition.be}</span><span class="nutrition-label">BE</span></div>` : ''}
                        </div>
                    </div>
                ` : ''}

                <div class="favorite-modal-footer">
                    <small>${i18n.t('favorites.added')}: ${UI.formatDate(favorite.added_at)}</small>
                </div>

                <div class="favorite-modal-actions">
                    <button class="btn btn-primary" onclick="Favorites.exportPDF(${recipe.id})">
                        📄 ${i18n.t('favorites.export_pdf')}
                    </button>
                    <button class="btn btn-danger" onclick="Favorites.removeAndCloseModal(${favorite.id})">
                        ❌ ${i18n.t('favorites.remove')}
                    </button>
                </div>
            </div>
        `;

        UI.showModal(recipe.name, modalContent, { size: 'large' });
    },

    // Export recipe as PDF
    async exportPDF(recipeId) {
        try {
            console.log('[Favorites] Exporting recipe:', recipeId);
            UI.info(i18n.t('favorites.pdf_creating'));

            const token = api.getToken();
            const response = await fetch(
                `${CONFIG.API_BASE_URL}/recipes/${recipeId}/export/pdf`,
                {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            );

            if (!response.ok) {
                throw new Error('PDF Export failed');
            }

            // Get blob
            const blob = await response.blob();

            // Extract filename from header
            const contentDisposition = response.headers.get('Content-Disposition');
            let filename = 'recipe.pdf';
            if (contentDisposition) {
                const matches = /filename="(.+)"/.exec(contentDisposition);
                if (matches) {
                    filename = matches[1];
                }
            }

            // Create download link
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();

            // Cleanup
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            UI.success(i18n.t('favorites.pdf_success'));
            console.log('[Favorites] PDF exported successfully');

        } catch (error) {
            console.error('[Favorites] Export error:', error);
            UI.error(i18n.t('favorites.pdf_error') + ': ' + error.message);
        }
    },

    // Remove favorite and close modal
    async removeAndCloseModal(favoriteId) {
        UI.closeModal();
        await this.remove(favoriteId);
    },

    // Remove favorite (no confirmation)
    async remove(favoriteId) {
        try {
            console.log('[Favorites] Removing favorite:', favoriteId);
            await api.removeFavorite(favoriteId);

            // Update cache
            const fav = this.items.find(f => f.id === favoriteId);
            if (fav && fav.recipe) {
                this.favoriteIds.delete(fav.recipe.id);
            }

            UI.success(i18n.t('favorites.removed'));
            await this.load();
        } catch (error) {
            console.error('[Favorites] Remove error:', error);
            UI.error('Error: ' + error.message);
        }
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
                    UI.success(i18n.t('favorites.removed'));
                }
            } else {
                // Add as favorite
                console.log('[Favorites] Adding favorite for recipe:', recipeId);
                const newFav = await api.addFavorite(recipeId);
                this.favoriteIds.add(recipeId);
                this.items.unshift(newFav);
                UI.success('Added to favorites!');
            }

            return !isFavorite; // Return new state
        } catch (error) {
            console.error('[Favorites] Toggle error:', error);
            UI.error('Error: ' + error.message);
            throw error;
        }
    }
};
