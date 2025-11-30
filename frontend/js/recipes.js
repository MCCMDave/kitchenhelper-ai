// KitchenHelper-AI Recipes Module

const Recipes = {
    generatedRecipes: [],
    selectedIngredients: new Set(),
    strictIngredientsMode: false,

    // Load ingredient selection checkboxes
    async loadIngredientSelection() {
        const container = document.getElementById('ingredient-checkboxes');

        // Make sure ingredients are loaded
        if (!Ingredients.items || Ingredients.items.length === 0) {
            await Ingredients.load();
        }

        const items = Ingredients.getItems();

        if (!items || items.length === 0) {
            container.innerHTML = `<p style="padding: var(--spacing-md); color: var(--text-muted);">${i18n.t('ingredients.empty')}</p>`;
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
        document.getElementById('selected-count').textContent = `${count} ${i18n.t('recipes.selected')}`;
    },

    // Generate recipes with streaming (if available)
    async generate() {
        if (this.selectedIngredients.size === 0) {
            UI.warning(i18n.t('recipes.select_warning') || 'Please select at least one ingredient!');
            return;
        }

        const container = document.getElementById('recipes-list');
        const btn = document.getElementById('generate-btn');

        btn.disabled = true;
        btn.textContent = 'Generiere...';

        // Check if streaming is supported (only for AI provider with Ollama)
        const useStreaming = false; // TODO: Enable when ready to test (set to true)

        if (useStreaming) {
            this.generateWithStreaming();
        } else {
            this.generateClassic();
        }
    },

    // Classic generation (current method)
    async generateClassic() {
        const container = document.getElementById('recipes-list');
        const btn = document.getElementById('generate-btn');

        // Enhanced loading message with Pro promotion
        const loadingMsg = i18n.currentLang === 'de'
            ? '🤖 AI generiert Rezept... Dies kann 30-60s dauern.<br><small style="opacity: 0.7;">💡 Mit Pro-Modell: 10x schneller (2-3s)</small>'
            : '🤖 AI generating recipe... This may take 30-60s.<br><small style="opacity: 0.7;">💡 With Pro Model: 10x faster (2-3s)</small>';

        container.innerHTML = `
            <div style="text-align: center; padding: var(--spacing-xl); color: var(--text-muted);">
                <div class="spinner"></div>
                <p style="margin-top: var(--spacing-md);">${loadingMsg}</p>
            </div>
        `;

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
                servings: 2,
                language: i18n.currentLang
            });

            this.generatedRecipes = response.recipes || [];
            this.renderGeneratedRecipes();

            if (response.daily_count_remaining !== undefined) {
                const msg = i18n.currentLang === 'de'
                    ? `Noch ${response.daily_count_remaining} Rezepte heute verfügbar`
                    : `${response.daily_count_remaining} recipes remaining today`;
                UI.info(msg);
            }

            // Refresh user data for updated counts
            await Auth.refreshUser();
        } catch (error) {
            UI.showError(container, i18n.t('recipes.error_generating') + ': ' + error.message);
        } finally {
            const btn = document.getElementById('generate-btn');
            btn.disabled = false;
            btn.textContent = i18n.t('recipes.generate');
        }
    },

    // Streaming generation (like ChatGPT - text appears word by word)
    async generateWithStreaming() {
        const container = document.getElementById('recipes-list');
        const btn = document.getElementById('generate-btn');

        // Show streaming UI
        const streamingMsg = i18n.currentLang === 'de'
            ? '🤖 AI schreibt Rezept...'
            : '🤖 AI writing recipe...';

        container.innerHTML = `
            <div style="padding: var(--spacing-xl);">
                <div style="display: flex; align-items: center; gap: var(--spacing-sm); margin-bottom: var(--spacing-md); color: var(--text-muted);">
                    <div class="spinner" style="width: 20px; height: 20px;"></div>
                    <span>${streamingMsg}</span>
                </div>
                <div id="streaming-output" style="
                    font-family: monospace;
                    white-space: pre-wrap;
                    background: var(--bg-secondary);
                    padding: var(--spacing-md);
                    border-radius: var(--radius-md);
                    min-height: 200px;
                    color: var(--text-light);
                "></div>
            </div>
        `;

        const outputDiv = document.getElementById('streaming-output');

        try {
            // Get active diet profiles
            let dietProfiles = [];
            try {
                const profilesResponse = await api.getProfiles(true);
                dietProfiles = profilesResponse.profiles.map(p => p.profile_type);
            } catch (e) {
                // Ignore
            }

            // Connect to SSE stream
            const token = localStorage.getItem('token');
            const url = `${api.API_BASE_URL}/recipes/generate/stream`;

            const eventSource = new EventSource(url, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            let fullText = '';

            eventSource.onmessage = (event) => {
                const data = JSON.parse(event.data);

                if (data.error) {
                    eventSource.close();
                    UI.error(data.error);
                    btn.disabled = false;
                    btn.textContent = i18n.t('recipes.generate');
                    return;
                }

                if (data.done) {
                    eventSource.close();

                    // Parse final JSON and display recipes
                    try {
                        // Extract JSON from fullText
                        let jsonText = fullText;
                        if (fullText.includes('```json')) {
                            jsonText = fullText.split('```json')[1].split('```')[0].trim();
                        } else if (fullText.includes('```')) {
                            jsonText = fullText.split('```')[1].split('```')[0].trim();
                        }

                        const recipes = JSON.parse(jsonText);
                        this.generatedRecipes = recipes;
                        this.renderGeneratedRecipes();

                        UI.success(i18n.currentLang === 'de' ? 'Rezept fertig!' : 'Recipe complete!');
                    } catch (e) {
                        console.error('Parse error:', e);
                        UI.error('Failed to parse recipe');
                    }

                    btn.disabled = false;
                    btn.textContent = i18n.t('recipes.generate');
                    return;
                }

                if (data.token) {
                    fullText += data.token;
                    outputDiv.textContent = fullText;

                    // Auto-scroll to bottom
                    outputDiv.scrollTop = outputDiv.scrollHeight;
                }
            };

            eventSource.onerror = (error) => {
                console.error('SSE error:', error);
                eventSource.close();
                UI.error('Streaming failed');
                btn.disabled = false;
                btn.textContent = i18n.t('recipes.generate');
            };

        } catch (error) {
            console.error('Streaming error:', error);
            UI.error(error.message);
            btn.disabled = false;
            btn.textContent = i18n.t('recipes.generate');
        }
    },

    // Render generated recipes
    renderGeneratedRecipes() {
        const container = document.getElementById('recipes-list');

        if (!this.generatedRecipes || this.generatedRecipes.length === 0) {
                UI.showEmpty(container, i18n.t('recipes.no_generated'), '🍽️');
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
                UI.showEmpty(container, i18n.t('recipes.no_history'), '');
                return;
            }

            container.innerHTML = recipes.map(recipe => this.renderRecipeCard(recipe, true)).join('');
        } catch (error) {
            UI.showError(container, i18n.t('recipes.error_loading') + ': ' + error.message);
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

        // Get translated labels
        const difficultyLabel = i18n.t('recipes.difficulty');
        const timeLabel = i18n.t('recipes.time');
        const servingsLabel = i18n.t('recipes.servings');
        const methodLabel = i18n.t('recipes.method');
        const usedIngredientsLabel = i18n.t('recipes.used_ingredients');
        const allIngredientsLabel = i18n.t('recipes.all_ingredients');
        const leftoverTipsLabel = i18n.t('recipes.leftover_tips');
        const nutritionLabel = i18n.t('recipes.nutrition');
        const addFavoriteLabel = i18n.t('recipes.add_favorite');
        const fatLabel = i18n.t('recipes.fat');

        return `
            <div class="recipe-card" data-id="${recipe.id}">
                <div class="recipe-header">
                    <div>
                        <h3 class="recipe-title">${UI.escapeHtml(recipe.name)}</h3>
                        ${fromHistory ? `<small style="opacity: 0.8;">${UI.formatDateTime(recipe.generated_at)}</small>` : ''}
                    </div>
                    <button class="favorite-btn" onclick="Recipes.toggleFavorite(${recipe.id}, this)" title="${addFavoriteLabel}">
                        ⭐
                    </button>
                </div>
                <div class="recipe-body">
                    ${recipe.description ? `<p class="recipe-description">${UI.escapeHtml(recipe.description)}</p>` : ''}

                    <div class="recipe-meta">
                        <span class="recipe-meta-item">⚡ ${difficultyLabel}: ${UI.getDifficultyStars(recipe.difficulty || 2)}</span>
                        <span class="recipe-meta-item">⏱️ ${timeLabel}: ${recipe.cooking_time || '?'}</span>
                        <span class="recipe-meta-item">
                            👥 ${servingsLabel}:
                            <span id="servings-${recipe.id}">${recipe.servings || 2}</span>
                            <button class="btn-icon" onclick="Recipes.showPortionCalculator(${recipe.id})" title="${i18n.t('recipes.adjust_portions')}">⚙️</button>
                        </span>
                        ${recipe.method ? `<span class="recipe-meta-item">🍳 ${methodLabel}: ${recipe.method}</span>` : ''}
                    </div>

                    ${usedIngredients.length > 0 ? `
                        <div class="recipe-section">
                            <h4 class="recipe-section-title">${usedIngredientsLabel}</h4>
                            <p style="color: var(--text-light);">${usedIngredients.map(i => UI.escapeHtml(i)).join(', ')}</p>
                        </div>
                    ` : ''}

                    ${ingredients.length > 0 ? `
                        <div class="recipe-section">
                            <h4 class="recipe-section-title">${allIngredientsLabel}</h4>
                            <ul class="recipe-ingredients-list">${ingredientsList}</ul>
                        </div>
                    ` : ''}

                    ${recipe.leftover_tips ? `
                        <div class="recipe-section">
                            <h4 class="recipe-section-title">${leftoverTipsLabel}</h4>
                            <p style="color: var(--text-light); font-style: italic;">${UI.escapeHtml(recipe.leftover_tips)}</p>
                        </div>
                    ` : ''}

                    ${Object.keys(nutrition).length > 0 ? `
                        <div class="recipe-section">
                            <h4 class="recipe-section-title">${nutritionLabel}</h4>
                            <div class="recipe-nutrition">
                                ${nutrition.calories ? `<div class="nutrition-item"><div class="nutrition-value">${nutrition.calories}</div><div class="nutrition-label">kcal</div></div>` : ''}
                                ${nutrition.protein ? `<div class="nutrition-item"><div class="nutrition-value">${nutrition.protein}g</div><div class="nutrition-label">Protein</div></div>` : ''}
                                ${nutrition.carbs ? `<div class="nutrition-item"><div class="nutrition-value">${nutrition.carbs}g</div><div class="nutrition-label">Carbs</div></div>` : ''}
                                ${nutrition.fat ? `<div class="nutrition-item"><div class="nutrition-value">${nutrition.fat}g</div><div class="nutrition-label">${fatLabel}</div></div>` : ''}
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
            UI.success(i18n.t('recipes.added_favorite'));
        } catch (error) {
            console.error('[Recipes] Favorite error:', error);
            if (error.message.includes('already')) {
                UI.warning(i18n.t('recipes.already_favorite'));
            } else if (error.message.includes('limit')) {
                UI.error(i18n.t('recipes.favorite_limit'));
            } else {
                UI.error(error.message);
            }
        }
    },

    // Show portion calculator
    showPortionCalculator(recipeId) {
        const recipe = this.generatedRecipes.find(r => r.id === recipeId) ||
                      this.historyRecipes?.find(r => r.id === recipeId);

        if (!recipe) {
            UI.error('Recipe not found');
            return;
        }

        const currentServings = recipe.servings || 2;
        const options = [1, 2, 4, 6, 8, 10];

        const content = `
            <div style="padding: var(--spacing-lg);">
                <h3>${i18n.t('recipes.adjust_portions')}</h3>
                <p style="margin: var(--spacing-md) 0; color: var(--text-muted);">
                    ${i18n.currentLang === 'de' ? 'Aktuell' : 'Current'}: ${currentServings} ${i18n.t('recipes.portions')}
                </p>
                <div style="display: flex; gap: var(--spacing-sm); flex-wrap: wrap; margin: var(--spacing-lg) 0;">
                    ${options.map(n => `
                        <button class="btn ${n === currentServings ? 'btn-primary' : 'btn-outline'}"
                                onclick="Recipes.adjustPortions(${recipeId}, ${n})"
                                style="min-width: 60px;">
                            ${n}
                        </button>
                    `).join('')}
                </div>
            </div>
        `;

        UI.showModal(content);
    },

    // Adjust portions
    async adjustPortions(recipeId, servings) {
        try {
            UI.closeModal();
            UI.info(i18n.currentLang === 'de' ? 'Berechne Portionen...' : 'Calculating portions...');

            const adjustedRecipe = await api.calculatePortions(recipeId, servings);

            // Update the recipe in memory
            const idx = this.generatedRecipes.findIndex(r => r.id === recipeId);
            if (idx !== -1) {
                this.generatedRecipes[idx] = adjustedRecipe;
                this.renderGeneratedRecipes();
            }

            UI.success(i18n.currentLang === 'de'
                ? `Portionen angepasst: ${servings}`
                : `Servings adjusted: ${servings}`);
        } catch (error) {
            console.error('[Recipes] Portion calculation error:', error);
            UI.error(error.message);
        }
    },

    // Toggle strict ingredients mode
    toggleStrictMode(enabled) {
        this.strictIngredientsMode = enabled;
        localStorage.setItem('strictIngredientsMode', enabled);

        const msg = i18n.currentLang === 'de'
            ? (enabled ? 'Nur vorhandene Zutaten aktiviert' : 'Alle Zutaten aktiviert')
            : (enabled ? 'Only available ingredients enabled' : 'All ingredients enabled');
        UI.success(msg);
    },

    // Load strict mode state
    loadStrictMode() {
        const saved = localStorage.getItem('strictIngredientsMode');
        this.strictIngredientsMode = saved === 'true';
        const toggle = document.getElementById('strict-ingredients-toggle');
        if (toggle) {
            toggle.checked = this.strictIngredientsMode;
        }
    }
};
