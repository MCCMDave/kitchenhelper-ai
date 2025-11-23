// KitchenHelper-AI Profiles Module

// ==================== PROFILE INFO MIT DISCLAIMERN ====================
const PROFILE_INFO = {
    diabetic: {
        name: 'Diabetiker',
        emoji: '💉',
        description: 'Kohlenhydrat-bewusste Rezepte mit BE/KE-Berechnung',
        disclaimer: `
            <div class="profile-disclaimer warning">
                <strong>⚠️ Medizinischer Hinweis:</strong><br>
                Diese Berechnungen sind nur Richtwerte! Bitte konsultieren Sie Ihren Arzt
                oder Diabetesberater für individuelle Ernährungsempfehlungen.
                KE/BE-Werte können je nach Produkt variieren. Überprüfen Sie immer
                die Nährwertangaben auf Verpackungen und passen Sie Ihre Insulin-Dosis
                entsprechend an.
            </div>
        `,
        color: '#e74c3c',
        settings: {
            unit: 'KE',
            daily_carb_limit: 180
        }
    },

    gluten_free: {
        name: 'Glutenfrei',
        emoji: '🌾',
        description: 'Rezepte ohne Weizen, Roggen, Gerste, Dinkel',
        disclaimer: `
            <div class="profile-disclaimer info">
                <strong>ℹ️ Hinweis:</strong><br>
                Bei Zöliakie oder schwerer Glutenunverträglichkeit beachten Sie bitte
                Kreuzkontaminationen in Ihrer Küche. Prüfen Sie alle Zutaten auf
                glutenfreie Zertifizierung. Im Zweifelsfall konsultieren Sie einen
                Ernährungsberater.
            </div>
        `,
        color: '#f39c12'
    },

    high_protein: {
        name: 'High Protein',
        emoji: '💪',
        description: 'Proteinreiche Rezepte für Muskelaufbau',
        disclaimer: null,
        color: '#9b59b6'
    },

    keto: {
        name: 'Keto',
        emoji: '🥑',
        description: 'Sehr kohlenhydratarm (<20g/Tag), fettreich',
        disclaimer: `
            <div class="profile-disclaimer info">
                <strong>ℹ️ Hinweis:</strong><br>
                Die ketogene Diät ist nicht für jeden geeignet. Bitte sprechen Sie mit
                Ihrem Arzt, besonders bei Vorerkrankungen wie Nierenproblemen,
                Schwangerschaft oder Stillzeit.
            </div>
        `,
        color: '#27ae60'
    },

    lactose_free: {
        name: 'Laktosefrei',
        emoji: '🥛',
        description: 'Rezepte ohne Milchzucker',
        disclaimer: `
            <div class="profile-disclaimer info">
                <strong>ℹ️ Hinweis:</strong><br>
                Laktosefreie Alternativen (Laktase-Tabletten, laktosefreie Milch)
                können verwendet werden. Bei schwerer Laktoseintoleranz achten Sie
                auf versteckte Laktose in verarbeiteten Produkten.
            </div>
        `,
        color: '#3498db'
    },

    low_carb: {
        name: 'Low Carb',
        emoji: '🥗',
        description: 'Reduzierte Kohlenhydrate (<100g/Tag)',
        disclaimer: null,
        color: '#16a085'
    },

    vegan: {
        name: 'Vegan',
        emoji: '🌱',
        description: 'Komplett pflanzlich, keine tierischen Produkte',
        disclaimer: `
            <div class="profile-disclaimer info">
                <strong>ℹ️ Hinweis:</strong><br>
                Achten Sie auf ausreichende Versorgung mit Vitamin B12, Eisen, Calcium
                und Omega-3-Fettsäuren. Erwägen Sie Nahrungsergänzungsmittel nach
                Rücksprache mit Ihrem Arzt.
            </div>
        `,
        color: '#2ecc71'
    },

    vegetarian: {
        name: 'Vegetarisch',
        emoji: '🥕',
        description: 'Ohne Fleisch und Fisch',
        disclaimer: null,
        color: '#95a5a6'
    }
};

const Profiles = {
    items: [],

    // Load all profiles
    async load() {
        const container = document.getElementById('profiles-list');
        UI.showLoading(container);

        try {
            const response = await api.getProfiles();
            this.items = response.profiles || [];
            this.render();
            this.updateActiveProfilesBadge();
        } catch (error) {
            UI.showError(container, 'Fehler beim Laden: ' + error.message);
        }
    },

    // Get active profiles
    getActiveProfiles() {
        return this.items.filter(p => p.is_active);
    },

    // Update active profiles badge in header
    updateActiveProfilesBadge() {
        const badge = document.getElementById('active-profiles');
        if (!badge) return;

        const activeProfiles = this.getActiveProfiles();

        if (activeProfiles.length === 0) {
            badge.innerHTML = '';
            return;
        }

        badge.innerHTML = `
            <div class="active-profiles-group" title="Aktive Profile: ${activeProfiles.map(p => PROFILE_INFO[p.profile_type]?.name || p.profile_type).join(', ')}">
                ${activeProfiles.map(p => {
                    const info = PROFILE_INFO[p.profile_type] || {};
                    return `<span class="active-profile-badge" style="background: ${info.color || 'var(--primary)'};">${info.emoji || ''}</span>`;
                }).join('')}
            </div>
        `;
    },

    // Render profiles list
    render() {
        const container = document.getElementById('profiles-list');

        if (!this.items || this.items.length === 0) {
            UI.showEmpty(container, 'Keine Ernährungsprofile vorhanden. Erstelle dein erstes Profil!', '👤');
            return;
        }

        container.innerHTML = this.items.map(profile => this.renderCard(profile)).join('');
    },

    // Render single profile card
    renderCard(profile) {
        const info = PROFILE_INFO[profile.profile_type] || {};
        const settings = profile.settings || {};
        const settingsText = this.formatSettings(profile.profile_type, settings);
        const hasDisclaimer = info.disclaimer;

        return `
            <div class="profile-card ${!profile.is_active ? 'inactive' : ''}"
                 data-id="${profile.id}"
                 style="border-left-color: ${info.color || 'var(--primary)'}">
                <div class="profile-header">
                    <span class="profile-name">
                        ${info.emoji || ''} ${UI.escapeHtml(profile.name)}
                    </span>
                    <span class="badge ${profile.is_active ? 'badge-success' : 'badge-secondary'}">
                        ${info.name || profile.profile_type}
                    </span>
                </div>
                ${info.description ? `<p class="profile-description">${info.description}</p>` : ''}
                ${hasDisclaimer ? info.disclaimer : ''}
                <div class="profile-settings">
                    ${settingsText || 'Keine besonderen Einstellungen'}
                </div>
                <div class="profile-actions">
                    <label class="toggle">
                        <input type="checkbox" ${profile.is_active ? 'checked' : ''} onchange="Profiles.toggleActive(${profile.id}, this.checked)">
                        <span class="toggle-slider"></span>
                        <span>${profile.is_active ? 'Aktiv' : 'Inaktiv'}</span>
                    </label>
                    <div style="display: flex; gap: var(--spacing-sm);">
                        <button class="btn btn-sm btn-ghost" onclick="Profiles.showEditModal(${profile.id})">Bearbeiten</button>
                        <button class="btn btn-sm btn-danger" onclick="Profiles.delete(${profile.id})">Löschen</button>
                    </div>
                </div>
            </div>
        `;
    },

    // Format settings for display
    formatSettings(type, settings) {
        const parts = [];

        if (settings.unit) parts.push(`Einheit: ${settings.unit}`);
        if (settings.daily_carb_limit) parts.push(`Max. Carbs: ${settings.daily_carb_limit}g/Tag`);
        if (settings.carbs_per_meal) parts.push(`Pro Mahlzeit: ${settings.carbs_per_meal}g`);
        if (settings.daily_fat_min) parts.push(`Min. Fett: ${settings.daily_fat_min}g/Tag`);
        if (settings.daily_protein) parts.push(`Protein: ${settings.daily_protein}g/Tag`);
        if (settings.daily_protein_min) parts.push(`Min. Protein: ${settings.daily_protein_min}g/Tag`);
        if (settings.exclude_ingredients && settings.exclude_ingredients.length > 0) {
            parts.push(`Ausgeschlossen: ${settings.exclude_ingredients.join(', ')}`);
        }

        return parts.join(' | ');
    },

    // Show add modal
    showAddModal() {
        // Filter out already existing profile types
        const existingTypes = this.items.map(p => p.profile_type);
        const availableTypes = CONFIG.getProfileTypes().filter(
            t => !existingTypes.includes(t.value)
        );

        if (availableTypes.length === 0) {
            UI.warning(i18n.t('profiles.all_added') || 'All profiles already added!');
            return;
        }

        UI.showFormModal({
            title: i18n.t('profiles.new') || 'New Diet Profile',
            fields: [
                {
                    name: 'profile_type',
                    label: i18n.t('profiles.type') || 'Profile Type',
                    type: 'select',
                    required: true,
                    options: availableTypes.map(t => ({
                        value: t.value,
                        label: `${t.emoji} ${t.label}`
                    }))
                },
                {
                    name: 'name',
                    label: i18n.t('profiles.name') || 'Name',
                    required: true,
                    placeholder: i18n.t('profiles.name_placeholder') || 'e.g. My Diabetes Profile'
                },
                {
                    name: 'is_active',
                    label: i18n.t('profiles.activate_now') || 'Activate immediately',
                    type: 'checkbox',
                    value: true
                }
            ],
            submitText: i18n.t('common.save') || 'Create',
            onSubmit: async (data) => {
                await this.createWithDisclaimer(data);
            }
        });
    },

    // Create with disclaimer confirmation for critical profiles
    async createWithDisclaimer(data) {
        const info = PROFILE_INFO[data.profile_type];

        // Show disclaimer before creating if exists
        if (info && info.disclaimer) {
            const confirmed = await UI.confirmHtml(
                `<h3>${info.emoji} ${info.name}</h3>
                 <p style="margin: var(--spacing-md) 0;">${info.description}</p>
                 ${info.disclaimer}
                 <p style="margin-top: var(--spacing-md);"><strong>Profil trotzdem hinzufügen?</strong></p>`,
                'Ja, hinzufügen',
                'Abbrechen'
            );

            if (!confirmed) return;
        }

        await this.create(data);
    },

    // Show edit modal
    showEditModal(id) {
        const profile = this.items.find(p => p.id === id);
        if (!profile) return;

        const settings = profile.settings || {};

        // Build dynamic fields based on profile type
        const fields = [
            {
                name: 'name',
                label: 'Name',
                required: true,
                value: profile.name
            },
            {
                name: 'is_active',
                label: 'Aktiv',
                type: 'checkbox',
                value: profile.is_active
            }
        ];

        // Add type-specific settings
        if (profile.profile_type === 'diabetic') {
            fields.push({
                name: 'unit',
                label: 'Einheit',
                type: 'select',
                value: settings.unit || 'KE',
                options: [
                    { value: 'KE', label: 'KE (Kohlenhydrat-Einheiten)' },
                    { value: 'BE', label: 'BE (Broteinheiten)' }
                ]
            });
            fields.push({
                name: 'daily_carb_limit',
                label: 'Tägliches Carb-Limit (g)',
                type: 'number',
                value: settings.daily_carb_limit || 180,
                placeholder: 'z.B. 180'
            });
        } else if (profile.profile_type === 'keto') {
            fields.push({
                name: 'daily_carb_limit',
                label: 'Tägliches Carb-Limit (g)',
                type: 'number',
                value: settings.daily_carb_limit || 50,
                placeholder: 'z.B. 50'
            });
            fields.push({
                name: 'daily_fat_min',
                label: 'Min. Fett pro Tag (g)',
                type: 'number',
                value: settings.daily_fat_min || 150,
                placeholder: 'z.B. 150'
            });
        } else if (profile.profile_type === 'low_carb') {
            fields.push({
                name: 'daily_carb_limit',
                label: 'Tägliches Carb-Limit (g)',
                type: 'number',
                value: settings.daily_carb_limit || 100,
                placeholder: 'z.B. 100'
            });
        } else if (profile.profile_type === 'high_protein') {
            fields.push({
                name: 'daily_protein_min',
                label: 'Min. Protein pro Tag (g)',
                type: 'number',
                value: settings.daily_protein_min || 150,
                placeholder: 'z.B. 150'
            });
        }

        UI.showFormModal({
            title: 'Profil bearbeiten',
            fields,
            submitText: 'Speichern',
            onSubmit: async (data) => {
                await this.update(id, profile.profile_type, data);
            }
        });
    },

    // Create profile
    async create(data) {
        try {
            const payload = {
                profile_type: data.profile_type,
                name: data.name,
                is_active: data.is_active || false,
                settings: {}
            };

            await api.createProfile(payload);
            UI.success('Profil erstellt!');
            await this.load();
        } catch (error) {
            UI.error('Fehler: ' + error.message);
        }
    },

    // Update profile
    async update(id, profileType, data) {
        try {
            const payload = {
                name: data.name,
                is_active: data.is_active
            };

            // Build settings based on type
            const settings = {};
            if (profileType === 'diabetic') {
                if (data.unit) settings.unit = data.unit;
                if (data.daily_carb_limit) settings.daily_carb_limit = parseInt(data.daily_carb_limit);
            } else if (profileType === 'keto') {
                if (data.daily_carb_limit) settings.daily_carb_limit = parseInt(data.daily_carb_limit);
                if (data.daily_fat_min) settings.daily_fat_min = parseInt(data.daily_fat_min);
            } else if (profileType === 'low_carb') {
                if (data.daily_carb_limit) settings.daily_carb_limit = parseInt(data.daily_carb_limit);
            } else if (profileType === 'high_protein') {
                if (data.daily_protein_min) settings.daily_protein_min = parseInt(data.daily_protein_min);
            }

            if (Object.keys(settings).length > 0) {
                payload.settings = settings;
            }

            await api.updateProfile(id, payload);
            UI.success('Profil aktualisiert!');
            await this.load();
        } catch (error) {
            UI.error('Fehler: ' + error.message);
        }
    },

    // Toggle active status
    async toggleActive(id, isActive) {
        try {
            await api.updateProfile(id, { is_active: isActive });
            UI.success(isActive ? 'Profil aktiviert!' : 'Profil deaktiviert!');
            await this.load();
        } catch (error) {
            UI.error('Fehler: ' + error.message);
            await this.load(); // Reload to reset checkbox
        }
    },

    // Delete profile
    delete(id) {
        const profile = this.items.find(p => p.id === id);
        UI.confirm(`"${profile?.name || 'Profil'}" wirklich löschen?`, async () => {
            try {
                await api.deleteProfile(id);
                UI.success('Profil gelöscht!');
                await this.load();
            } catch (error) {
                UI.error('Fehler: ' + error.message);
            }
        });
    }
};
