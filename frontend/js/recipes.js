// KitchenHelper-AI Recipes Module

const Recipes = {
    generatedRecipes: [],
    selectedIngredients: new Set(),

    // Load ingredient selection checkboxes
    async loadIngredientSelection() {
        const container = document.getElementById('ingredient-checkboxes');

        // Make sure ingredients are loaded
        if (!Ingredients.items || Ingredients.items.length === 0) {
            await Ingredients.load();
        }

        const items = Ingredients.getItems();

        if (!items || items.length === 0) {
            container.innerHTML = '<p style="padding: var(--spacing-md); color: var(--text-muted);">Keine Zutaten vorhanden. Füge zuerst Zutaten hinzu!</p>';
            return;
        }

        container.innerHTML = items.map(item => `
            <label class="ingredient-checkbox">
                <input type="checkbox" value="${item.id}" onchange="Recipes.toggleIngredient(${item.id})">
                <span>${UI.escapeHtml(item.name)}</span>
            </label>
        `).join('');

        this.updateSelectedCount();
    },

    // Toggle ingredient selection
    toggleIngredient(id) {
        if (this.selectedIngredients.has(id)) {
            this.selectedIngredients.delete(id);
        } else {
            this.selectedIngredients.add(id);
        }
        this.updateSelectedCount();
    },

    // Update selected count display
    updateSelectedCount() {
        const count = this.selectedIngredients.size;
        document.getElementById('selected-count').textContent = `${count} Zutat${count !== 1 ? 'en' : ''} ausgewählt`;
    },

    // Generate recipes
    async generate() {
        if (this.selectedIngredients.size === 0) {
            UI.warning('Bitte wähle mindestens eine Zutat aus!');
            return;
        }

        const container = document.getElementById('recipes-list');
        const btn = document.getElementById('generate-btn');

        btn.disabled = true;
        btn.textContent = 'Generiere...';
        UI.showLoading(container);

        try {
            // Get active diet profiles
            let dietProfiles = [];
            try {
                const profilesResponse = await api.getProfiles(true);
                dietProfiles = profilesResponse.profiles.map(p => p.profile_type);
            } catch (e) {
                // Ignore profile errors
            }

            const response = await api.generateRecipes({
                ingredient_ids: Array.from(this.selectedIngredients),
                ai_provider: 'mock',
                diet_profiles: dietProfiles,
                servings: 2
            });

            this.generatedRecipes = response.recipes || [];
            this.renderGeneratedRecipes();

            if (response.daily_count_remaining !== undefined) {
                UI.info(`Noch ${response.daily_count_remaining} Rezepte heute verfügbar`);
            }

            // Refresh user data for updated counts
            await Auth.refreshUser();
        } catch (error) {
            UI.showError(container, 'Fehler beim Generieren: ' + error.message);
        } finally {
            btn.disabled = false;
            btn.textContent = 'Rezepte generieren';
        }
    },

    // Render generated recipes
    renderGeneratedRecipes() {
        const container = document.getElementById('recipes-list');

        if (!this.generatedRecipes || this.generatedRecipes.length === 0) {
            UI.showEmpty(container, 'Keine Rezepte generiert. Wähle Zutaten und klicke auf "Generieren"!', '🍽️');
            return;
        }

        container.innerHTML = this.generatedRecipes.map(recipe => this.renderRecipeCard(recipe)).join('');
    },

    // Load recipe history
    async loadHistory() {
        const container = document.getElementById('recipe-history');
        UI.showLoading(container);

        try {
            const response = await api.getRecipeHistory(10);
            const recipes = response.recipes || [];

            if (recipes.length === 0) {
                UI.showEmpty(container, 'Noch keine Rezepte generiert.', '');
                return;
            }

            container.innerHTML = recipes.map(recipe => this.renderRecipeCard(recipe, true)).join('');
        } catch (error) {
            UI.showError(container, 'Fehler beim Laden: ' + error.message);
        }
    },

    // Render recipe card
    renderRecipeCard(recipe, fromHistory = false) {
        // Parse JSON fields if needed
        let ingredients = [];
        let nutrition = {};
        let usedIngredients = [];

        try {
            ingredients = typeof recipe.ingredients === 'string' ? JSON.parse(recipe.ingredients) : (recipe.ingredients || []);
        } catch (e) { ingredients = []; }

        try {
            nutrition = typeof recipe.nutrition_per_serving === 'string' ? JSON.parse(recipe.nutrition_per_serving) : (recipe.nutrition_per_serving || {});
        } catch (e) { nutrition = {}; }

        try {
            usedIngredients = typeof recipe.used_ingredients === 'string' ? JSON.parse(recipe.used_ingredients) : (recipe.used_ingredients || []);
        } catch (e) { usedIngredients = []; }

        const ingredientsList = ingredients.map(ing =>
            `<li>${UI.escapeHtml(ing.amount || '')} ${UI.escapeHtml(ing.name || '')}</li>`
        ).join('');

        return `
            <div class="recipe-card" data-id="${recipe.id}">
                <div class="recipe-header">
                    <div>
                        <h3 class="recipe-title">${UI.escapeHtml(recipe.name)}</h3>
                        ${fromHistory ? `<small style="opacity: 0.8;">${UI.formatDateTime(recipe.generated_at)}</small>` : ''}
                    </div>
                    <button class="favorite-btn" onclick="Recipes.toggleFavorite(${recipe.id}, this)" title="Zu Favoriten hinzufügen">
                        ⭐
                    </button>
                </div>
                <div class="recipe-body">
                    ${recipe.description ? `<p class="recipe-description">${UI.escapeHtml(recipe.description)}</p>` : ''}

                    <div class="recipe-meta">
                        <span class="recipe-meta-item">⚡ Schwierigkeit: ${UI.getDifficultyStars(recipe.difficulty || 2)}</span>
                        <span class="recipe-meta-item">⏱️ Zeit: ${recipe.cooking_time || '?'}</span>
                        <span class="recipe-meta-item">👥 Portionen: ${recipe.servings || 2}</span>
                        ${recipe.method ? `<span class="recipe-meta-item">🍳 Methode: ${recipe.method}</span>` : ''}
                    </div>

                    ${usedIngredients.length > 0 ? `
                        <div class="recipe-section">
                            <h4 class="recipe-section-title">Verwendete Zutaten</h4>
                            <p style="color: var(--text-light);">${usedIngredients.map(i => UI.escapeHtml(i)).join(', ')}</p>
                        </div>
                    ` : ''}

                    ${ingredients.length > 0 ? `
                        <div class="recipe-section">
                            <h4 class="recipe-section-title">Alle Zutaten</h4>
                            <ul class="recipe-ingredients-list">${ingredientsList}</ul>
                        </div>
                    ` : ''}

                    ${recipe.leftover_tips ? `
                        <div class="recipe-section">
                            <h4 class="recipe-section-title">Reste-Tipps</h4>
                            <p style="color: var(--text-light); font-style: italic;">${UI.escapeHtml(recipe.leftover_tips)}</p>
                        </div>
                    ` : ''}

                    ${Object.keys(nutrition).length > 0 ? `
                        <div class="recipe-section">
                            <h4 class="recipe-section-title">Nährwerte pro Portion</h4>
                            <div class="recipe-nutrition">
                                ${nutrition.calories ? `<div class="nutrition-item"><div class="nutrition-value">${nutrition.calories}</div><div class="nutrition-label">kcal</div></div>` : ''}
                                ${nutrition.protein ? `<div class="nutrition-item"><div class="nutrition-value">${nutrition.protein}g</div><div class="nutrition-label">Protein</div></div>` : ''}
                                ${nutrition.carbs ? `<div class="nutrition-item"><div class="nutrition-value">${nutrition.carbs}g</div><div class="nutrition-label">Carbs</div></div>` : ''}
                                ${nutrition.fat ? `<div class="nutrition-item"><div class="nutrition-value">${nutrition.fat}g</div><div class="nutrition-label">Fett</div></div>` : ''}
                                ${nutrition.ke ? `<div class="nutrition-item"><div class="nutrition-value">${nutrition.ke}</div><div class="nutrition-label">KE</div></div>` : ''}
                                ${nutrition.be ? `<div class="nutrition-item"><div class="nutrition-value">${nutrition.be}</div><div class="nutrition-label">BE</div></div>` : ''}
                            </div>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    },

    // Toggle favorite
    async toggleFavorite(recipeId, btn) {
        try {
            console.log('[Recipes] Adding to favorites:', recipeId);
            await api.addFavorite(recipeId);
            btn.classList.add('active');
            btn.textContent = '⭐';
            UI.success('Zu Favoriten hinzugefügt!');
        } catch (error) {
            console.error('[Recipes] Favorite error:', error);
            if (error.message.includes('already')) {
                UI.warning('Bereits in Favoriten!');
            } else if (error.message.includes('limit')) {
                UI.error('Favoriten-Limit erreicht!');
            } else {
                UI.error(error.message);
            }
        }
    }
};
