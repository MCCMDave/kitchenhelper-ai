// KitchenHelper-AI Favorites Module

const Favorites = {
    items: [],
    filteredItems: [], // For search results
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

            this.filteredItems = this.items; // Initialize filtered items
            this.render();
        } catch (error) {
            console.error('[Favorites] Load error:', error);
            UI.showError(container, 'Error loading: ' + error.message);
        }
    },

    // Search favorites
    search(query) {
        const searchQuery = query.toLowerCase().trim();

        if (!searchQuery) {
            this.filteredItems = this.items;
        } else {
            this.filteredItems = this.items.filter(fav => {
                const recipe = fav.recipe;
                if (!recipe) return false;

                // Search in recipe name
                if (recipe.name && recipe.name.toLowerCase().includes(searchQuery)) {
                    return true;
                }

                // Search in ingredients
                if (recipe.ingredients) {
                    const ingredients = typeof recipe.ingredients === 'string'
                        ? JSON.parse(recipe.ingredients)
                        : recipe.ingredients;

                    const hasIngredient = ingredients.some(ing =>
                        ing.name && ing.name.toLowerCase().includes(searchQuery)
                    );
                    if (hasIngredient) return true;
                }

                // Search in description
                if (recipe.description && recipe.description.toLowerCase().includes(searchQuery)) {
                    return true;
                }

                return false;
            });
        }

        this.render();
    },

    // Render favorites list as compact cards
    render() {
        const container = document.getElementById('favorites-list');

        const itemsToRender = this.filteredItems || this.items;

        if (!itemsToRender || itemsToRender.length === 0) {
            const searchInput = document.getElementById('favorites-search');
            const isSearching = searchInput && searchInput.value.trim();
            const message = isSearching ? i18n.t('favorites.no_results') : i18n.t('favorites.empty');
            UI.showEmpty(container, message, '⭐');
            return;
        }

        console.log('[Favorites] Rendering', itemsToRender.length, 'items');
        Sanitize.setHTML(container, itemsToRender.map(fav => this.renderCard(fav)).join(''));
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
                    <button class="btn btn-secondary" onclick="Favorites.shareRecipe(${favorite.id})">
                        🔗 ${i18n.t('favorites.share')}
                    </button>
                    <button class="btn btn-secondary" onclick="Favorites.exportShoppingList([${favorite.id}])">
                        🛒 ${i18n.t('favorites.shopping_list')}
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

            const response = await fetch(
                `${CONFIG.API_BASE_URL}/recipes/${recipeId}/export/pdf`,
                {
                    method: 'GET',
                    credentials: 'include'  // httpOnly cookie auth
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

    // Share recipe - create share link
    async shareRecipe(favoriteId) {
        try {
            UI.info(i18n.t('favorites.creating_link'));

            const result = await api.createShareLink(null, favoriteId, 168); // 7 days

            // Show share modal
            const shareUrl = window.location.origin + result.share_url;
            const expiresAt = new Date(result.expires_at).toLocaleDateString();

            const modalContent = `
                <div class="share-modal-content">
                    <p>${i18n.t('favorites.share_text')}</p>

                    <div class="share-url-container">
                        <input type="text" class="form-control share-url-input" value="${shareUrl}" readonly id="share-url-input">
                        <button class="btn btn-primary" onclick="Favorites.copyShareUrl()">
                            📋 ${i18n.t('favorites.copy')}
                        </button>
                    </div>

                    <p class="share-expiry">
                        ${i18n.t('favorites.link_valid_until')} ${expiresAt}
                    </p>

                    <div class="share-buttons">
                        <button class="btn btn-secondary" onclick="Favorites.shareViaWhatsApp('${shareUrl}')">
                            💬 WhatsApp
                        </button>
                        <button class="btn btn-secondary" onclick="Favorites.shareViaEmail('${shareUrl}', '${result.recipe_name}')">
                            ✉️ Email
                        </button>
                    </div>
                </div>
            `;

            UI.showModal(
                '🔗 ' + i18n.t('favorites.share_recipe'),
                modalContent,
                { size: 'medium' }
            );

        } catch (error) {
            console.error('[Favorites] Share error:', error);
            UI.error('Error: ' + error.message);
        }
    },

    // Copy share URL to clipboard
    copyShareUrl() {
        const input = document.getElementById('share-url-input');
        input.select();
        document.execCommand('copy');

        UI.success(i18n.t('favorites.link_copied'));
    },

    // Share via WhatsApp
    shareViaWhatsApp(url) {
        const text = encodeURIComponent(`Check out this recipe: ${url}`);
        window.open(`https://wa.me/?text=${text}`, '_blank');
    },

    // Share via Email
    shareViaEmail(url, recipeName) {
        const lang = i18n.currentLang;

        const subjectText = lang === 'de'
            ? `Rezept: ${recipeName}`
            : `Recipe: ${recipeName}`;

        const bodyText = lang === 'de'
            ? `Hallo!\n\nIch möchte dieses Rezept mit dir teilen:\n\n${recipeName}\n${url}\n\nViel Spaß beim Kochen!\n\nErstellt mit KitchenHelper-AI`
            : `Hi!\n\nI wanted to share this recipe with you:\n\n${recipeName}\n${url}\n\nEnjoy cooking!\n\nCreated with KitchenHelper-AI`;

        const subject = encodeURIComponent(subjectText);
        const body = encodeURIComponent(bodyText);

        // Use window.open instead of window.location to avoid navigation issues
        const mailtoLink = `mailto:?subject=${subject}&body=${body}`;
        const mailWindow = window.open(mailtoLink, '_self');

        // Fallback if popup blocker
        if (!mailWindow) {
            window.location.href = mailtoLink;
        }
    },

    // Export shopping list for favorites
    async exportShoppingList(favoriteIds) {
        try {
            UI.info(i18n.t('favorites.creating_list'));

            const blob = await api.exportShoppingListText([], favoriteIds, 1.0);

            // Download file
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'shopping_list.txt';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            UI.success(i18n.t('favorites.list_created'));

        } catch (error) {
            console.error('[Favorites] Shopping list error:', error);
            UI.error(i18n.t('common.error_prefix') + error.message);
        }
    },

    // Export shopping list for ALL favorites
    async exportAllShoppingList() {
        const favoriteIds = this.items.map(f => f.id);
        if (favoriteIds.length === 0) {
            UI.warning(i18n.t('favorites.no_favorites'));
            return;
        }
        await this.exportShoppingList(favoriteIds);
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
