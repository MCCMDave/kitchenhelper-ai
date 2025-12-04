// KitchenHelper-AI Profiles Module - Simplified Checkbox System

// ==================== PROFILE INFO WITH DISCLAIMERS ====================
const PROFILE_INFO = {
    diabetic: {
        emoji: '💉',
        color: '#e74c3c',
        disclaimer_de: `
            <strong>⚠️ Medizinischer Hinweis:</strong><br>
            Diese Berechnungen sind nur Richtwerte! Bitte konsultieren Sie Ihren Arzt
            oder Diabetesberater für individuelle Ernährungsempfehlungen.
            KE/BE-Werte können je nach Produkt variieren. Überprüfen Sie immer
            die Nährwertangaben auf Verpackungen und passen Sie Ihre Insulin-Dosis
            entsprechend an.
        `,
        disclaimer_en: `
            <strong>⚠️ Medical Notice:</strong><br>
            These calculations are only guidelines! Please consult your doctor
            or diabetes counselor for individual dietary recommendations.
            KE/BE values may vary depending on the product. Always check
            the nutritional information on packaging and adjust your insulin dose
            accordingly.
        `
    },
    gluten_free: {
        emoji: '🌾',
        color: '#f39c12',
        disclaimer_de: `
            <strong>ℹ️ Hinweis:</strong><br>
            Bei Zöliakie oder schwerer Glutenunverträglichkeit beachten Sie bitte
            Kreuzkontaminationen in Ihrer Küche. Prüfen Sie alle Zutaten auf
            glutenfreie Zertifizierung.
        `,
        disclaimer_en: `
            <strong>ℹ️ Notice:</strong><br>
            For celiac disease or severe gluten intolerance, please be aware of
            cross-contamination in your kitchen. Check all ingredients for
            gluten-free certification.
        `
    },
    high_protein: {
        emoji: '💪',
        color: '#9b59b6',
        disclaimer_de: null,
        disclaimer_en: null
    },
    keto: {
        emoji: '🥑',
        color: '#27ae60',
        disclaimer_de: `
            <strong>ℹ️ Hinweis:</strong><br>
            Die ketogene Diät ist nicht für jeden geeignet. Bitte sprechen Sie mit
            Ihrem Arzt, besonders bei Vorerkrankungen wie Nierenproblemen,
            Schwangerschaft oder Stillzeit.
        `,
        disclaimer_en: `
            <strong>ℹ️ Notice:</strong><br>
            The ketogenic diet is not suitable for everyone. Please consult your
            doctor, especially if you have pre-existing conditions such as kidney
            problems, pregnancy or breastfeeding.
        `
    },
    lactose_free: {
        emoji: '🥛',
        color: '#3498db',
        disclaimer_de: `
            <strong>ℹ️ Hinweis:</strong><br>
            Laktosefreie Alternativen können verwendet werden. Bei schwerer
            Laktoseintoleranz achten Sie auf versteckte Laktose in verarbeiteten Produkten.
        `,
        disclaimer_en: `
            <strong>ℹ️ Notice:</strong><br>
            Lactose-free alternatives can be used. For severe lactose intolerance,
            watch out for hidden lactose in processed products.
        `
    },
    low_carb: {
        emoji: '🥗',
        color: '#16a085',
        disclaimer_de: null,
        disclaimer_en: null
    },
    vegan: {
        emoji: '🌱',
        color: '#2ecc71',
        disclaimer_de: `
            <strong>ℹ️ Hinweis:</strong><br>
            Achten Sie auf ausreichende Versorgung mit Vitamin B12, Eisen, Calcium
            und Omega-3-Fettsäuren. Erwägen Sie Nahrungsergänzungsmittel nach
            Rücksprache mit Ihrem Arzt.
        `,
        disclaimer_en: `
            <strong>ℹ️ Notice:</strong><br>
            Make sure you get enough Vitamin B12, Iron, Calcium and Omega-3 fatty acids.
            Consider supplements after consulting your doctor.
        `
    },
    vegetarian: {
        emoji: '🥕',
        color: '#95a5a6',
        disclaimer_de: null,
        disclaimer_en: null
    },
    paleo: {
        emoji: '🦴',
        color: '#8e44ad',
        disclaimer_de: null,
        disclaimer_en: null
    },
    low_fodmap: {
        emoji: '🌾',
        color: '#d35400',
        disclaimer_de: `
            <strong>ℹ️ Hinweis:</strong><br>
            Die Low FODMAP Diät sollte idealerweise unter Anleitung eines Ernährungsberaters
            durchgeführt werden. Sie ist als temporäre Eliminationsdiät gedacht.
        `,
        disclaimer_en: `
            <strong>ℹ️ Notice:</strong><br>
            The Low FODMAP diet should ideally be followed under the guidance of a nutritionist.
            It is intended as a temporary elimination diet.
        `
    },
    kosher: {
        emoji: '✡️',
        color: '#3498db',
        disclaimer_de: null,
        disclaimer_en: null
    },
    halal: {
        emoji: '☪️',
        color: '#27ae60',
        disclaimer_de: null,
        disclaimer_en: null
    },
    histamine_free: {
        emoji: '🧪',
        color: '#e67e22',
        disclaimer_de: `
            <strong>ℹ️ Hinweis:</strong><br>
            Bei Histaminintoleranz sollten Sie mit einem Arzt oder Ernährungsberater sprechen.
            Die Verträglichkeit kann individuell variieren.
        `,
        disclaimer_en: `
            <strong>ℹ️ Notice:</strong><br>
            For histamine intolerance, consult your doctor or nutritionist.
            Tolerance can vary individually.
        `
    },
    nut_free: {
        emoji: '🚫🥜',
        color: '#c0392b',
        disclaimer_de: `
            <strong>⚠️ Allergie-Hinweis:</strong><br>
            Bei Nussallergien können bereits kleinste Mengen gefährlich sein.
            Achten Sie auf Kreuzkontamination in der Küche und prüfen Sie alle Zutaten sorgfältig.
        `,
        disclaimer_en: `
            <strong>⚠️ Allergy Notice:</strong><br>
            For nut allergies, even the smallest amounts can be dangerous.
            Watch for cross-contamination in the kitchen and check all ingredients carefully.
        `
    },
    pescatarian: {
        emoji: '🐟',
        color: '#16a085',
        disclaimer_de: null,
        disclaimer_en: null
    },
    pregnancy: {
        emoji: '🤰',
        color: '#e91e63',
        disclaimer_de: `
            <strong>⚠️ Schwangerschafts-Hinweis:</strong><br>
            Bitte sprechen Sie mit Ihrem Frauenarzt über Ihre Ernährung während der Schwangerschaft.
            Vermeiden Sie Rohmilch, rohen Fisch, rohes Fleisch und Alkohol.
        `,
        disclaimer_en: `
            <strong>⚠️ Pregnancy Notice:</strong><br>
            Please consult your gynecologist about your diet during pregnancy.
            Avoid raw milk, raw fish, raw meat and alcohol.
        `
    },
    mediterranean: {
        emoji: '🫒',
        color: '#2980b9',
        disclaimer_de: null,
        disclaimer_en: null
    }
};

const Profiles = {
    items: [],
    activeProfiles: new Set(),

    // Load all profiles
    async load() {
        const container = document.getElementById('profiles-list');
        UI.showLoading(container);

        try {
            const response = await api.getProfiles();
            this.items = response.profiles || [];

            // Update active profiles set
            this.activeProfiles.clear();
            this.items.filter(p => p.is_active).forEach(p => this.activeProfiles.add(p.profile_type));

            this.render();
            this.updateActiveProfilesBadge();
        } catch (error) {
            UI.showError(container, i18n.t('error.fetch_failed'));
        }
    },

    // Silent reload without loading indicator (for toggles)
    async silentReload() {
        try {
            const response = await api.getProfiles();
            this.items = response.profiles || [];

            // Update active profiles set
            this.activeProfiles.clear();
            this.items.filter(p => p.is_active).forEach(p => this.activeProfiles.add(p.profile_type));

            this.render();
            this.updateActiveProfilesBadge();
        } catch (error) {
            console.error('[Profiles] Silent reload error:', error);
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
            Sanitize.setHTML(badge, '');
            return;
        }

        const profileNames = activeProfiles.map(p => {
            const types = CONFIG.getProfileTypes();
            const type = types.find(t => t.value === p.profile_type);
            return type ? type.label : p.profile_type;
        }).join(', ');

        // Check if collapsed state is saved
        const isCollapsed = localStorage.getItem('profilesCollapsed') === 'true';

        // Generate mini badges for collapsed state
        const miniBadges = activeProfiles.map(p => {
            const info = PROFILE_INFO[p.profile_type] || {};
            return info.emoji || '';
        }).join('');

        Sanitize.setHTML(badge, `
            <button class="active-profiles-toggle" onclick="Profiles.toggleBadge()" title="${Sanitize.escapeHTML(isCollapsed ? 'Präferenzen einblenden' : 'Präferenzen ausblenden')}">
                ${isCollapsed ? '▶' : '▼'}
            </button>
            ${isCollapsed ? `
                <div class="active-profiles-mini-circle" onclick="Profiles.goToProfilesPage()" title="Aktive Präferenzen">
                    ${miniBadges}
                </div>
            ` : `
                <div class="active-profiles-group" onclick="Profiles.goToProfilesPage()">
                    ${activeProfiles.map(p => {
                        const info = PROFILE_INFO[p.profile_type] || {};
                        const types = CONFIG.getProfileTypes();
                        const type = types.find(t => t.value === p.profile_type);
                        const name = type ? type.label : p.profile_type;
                        return `<span class="active-profile-badge" style="background: ${Sanitize.escapeHTML(info.color || 'var(--primary)')};" data-name="${Sanitize.escapeHTML(name)}" title="${Sanitize.escapeHTML(name)}">${info.emoji || ''}</span>`;
                    }).join('')}
                </div>
            `}
        `);
    },

    // Toggle badge visibility
    toggleBadge() {
        const currentState = localStorage.getItem('profilesCollapsed') === 'true';
        const newState = !currentState;
        localStorage.setItem('profilesCollapsed', newState);

        // Re-render the badge with new state
        this.updateBadge();
    },

    // Navigate to profiles page
    goToProfilesPage() {
        // Deactivate all tabs
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        // Deactivate all sections
        document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
        // Activate profiles section
        document.getElementById('profiles-section').classList.add('active');
        // Load profiles
        this.load();
    },

    // Render profiles as checkboxes
    render() {
        const container = document.getElementById('profiles-list');
        const profileTypes = CONFIG.getProfileTypes();
        const lang = i18n.currentLang;

        // Group: existing profiles and available ones
        const existingMap = new Map(this.items.map(p => [p.profile_type, p]));

        const checkboxesHtml = profileTypes.map(type => {
            const info = PROFILE_INFO[type.value] || {};
            const existing = existingMap.get(type.value);
            const isActive = existing?.is_active || false;
            const strictMode = existing?.strict_ingredients_only || false;
            const hasDisclaimer = info.disclaimer_de || info.disclaimer_en;

            return `
                <div class="profile-checkbox-card" style="border-left: 4px solid ${info.color || 'var(--primary)'}">
                    <label class="profile-checkbox-label">
                        <input type="checkbox"
                               ${isActive ? 'checked' : ''}
                               onchange="Profiles.toggleProfile('${type.value}', this.checked)"
                               data-profile="${type.value}">
                        <span class="profile-checkbox-content">
                            <span class="profile-emoji">${info.emoji || ''}</span>
                            <span class="profile-name">${type.label}</span>
                            ${hasDisclaimer ? `
                                <button class="profile-info-btn" onclick="event.preventDefault(); Profiles.showDisclaimer('${type.value}')" title="${lang === 'de' ? 'Wichtiger Hinweis' : 'Important notice'}">
                                    ⚠️
                                </button>
                            ` : ''}
                        </span>
                    </label>
                    ${isActive ? `
                        <div class="profile-ingredient-mode" style="margin-top: var(--spacing-sm); padding-left: var(--spacing-lg);">
                            <label class="profile-mode-option">
                                <input type="radio"
                                       name="mode-${type.value}"
                                       ${strictMode ? 'checked' : ''}
                                       onchange="Profiles.updateIngredientMode('${type.value}', true)">
                                <span class="mode-label">
                                    <strong data-i18n="profiles.strict_mode">Nur vorhandene Zutaten</strong>
                                    <small data-i18n="profiles.strict_mode_hint" style="display: block; color: var(--text-muted);">KI schlägt nur Rezepte mit gespeicherten Zutaten vor</small>
                                </span>
                            </label>
                            <label class="profile-mode-option">
                                <input type="radio"
                                       name="mode-${type.value}"
                                       ${!strictMode ? 'checked' : ''}
                                       onchange="Profiles.updateIngredientMode('${type.value}', false)">
                                <span class="mode-label">
                                    <strong data-i18n="profiles.shopping_mode">Neue Zutaten zur Einkaufsliste</strong>
                                    <small data-i18n="profiles.shopping_mode_hint" style="display: block; color: var(--text-muted);">KI kann neue Zutaten vorschlagen</small>
                                </span>
                            </label>
                        </div>
                    ` : ''}
                </div>
            `;
        }).join('');

        Sanitize.setHTML(container, `
            <div class="profiles-intro">
                <p>${lang === 'de'
                    ? 'Wähle deine Ernährungsprofile. Diese werden bei der Rezeptgenerierung berücksichtigt.'
                    : 'Select your diet profiles. These will be considered when generating recipes.'}</p>
            </div>
            <div class="profiles-checkbox-grid">
                ${checkboxesHtml}
            </div>
        `);
    },

    // Toggle profile on/off
    async toggleProfile(profileType, isActive) {
        const info = PROFILE_INFO[profileType];
        const lang = i18n.currentLang;

        // If activating and has disclaimer - ALWAYS show it, even if shown before
        if (isActive && info && (info.disclaimer_de || info.disclaimer_en)) {
            const disclaimer = lang === 'de' ? info.disclaimer_de : info.disclaimer_en;
            const types = CONFIG.getProfileTypes();
            const type = types.find(t => t.value === profileType);
            const typeName = type ? type.label : profileType;

            const confirmed = await UI.confirmHtml(
                `<h3>${info.emoji} ${typeName}</h3>
                 <div class="profile-disclaimer warning" style="margin: var(--spacing-md) 0;">
                     ${disclaimer}
                 </div>
                 <p><strong>${lang === 'de' ? 'Profil aktivieren?' : 'Activate profile?'}</strong></p>`,
                lang === 'de' ? 'Ja, aktivieren' : 'Yes, activate',
                lang === 'de' ? 'Abbrechen' : 'Cancel'
            );

            if (!confirmed) {
                // Reset checkbox
                const checkbox = document.querySelector(`input[data-profile="${profileType}"]`);
                if (checkbox) checkbox.checked = false;
                return;
            }
        }

        try {
            const existing = this.items.find(p => p.profile_type === profileType);

            if (existing) {
                // Update existing profile
                await api.updateProfile(existing.id, { is_active: isActive });
            } else if (isActive) {
                // Create new profile
                const types = CONFIG.getProfileTypes();
                const type = types.find(t => t.value === profileType);
                await api.createProfile({
                    profile_type: profileType,
                    name: type ? type.label : profileType,
                    is_active: true,
                    settings: {}
                });
            }

            UI.success(isActive
                ? i18n.t('profiles.activated')
                : i18n.t('profiles.deactivated'));

            await this.silentReload();
        } catch (error) {
            UI.error(error.message);
            await this.load(); // Reload to reset checkboxes
        }
    },

    // Update ingredient mode (strict vs. shopping list)
    async updateIngredientMode(profileType, strictMode) {
        try {
            const existing = this.items.find(p => p.profile_type === profileType);
            if (!existing) {
                UI.error('Profile not found');
                return;
            }

            await api.updateProfile(existing.id, {
                strict_ingredients_only: strictMode
            });

            // Silent reload to update state
            await this.silentReload();
        } catch (error) {
            UI.error(error.message);
            await this.load();
        }
    },

    // Show disclaimer popup for a profile
    showDisclaimer(profileType) {
        const info = PROFILE_INFO[profileType];
        if (!info) return;

        const lang = i18n.currentLang;
        const disclaimer = lang === 'de' ? info.disclaimer_de : info.disclaimer_en;

        if (!disclaimer) return;

        const types = CONFIG.getProfileTypes();
        const type = types.find(t => t.value === profileType);
        const typeName = type ? type.label : profileType;

        UI.showModal(
            `${info.emoji} ${typeName}`,
            `<div class="profile-disclaimer-content">
                <div class="profile-disclaimer warning">
                    ${disclaimer}
                </div>
            </div>`,
            { size: 'medium' }
        );
    },

    // Legacy method for compatibility - now just toggles
    showAddModal() {
        // Show info that profiles are now checkboxes
        const lang = i18n.currentLang;
        UI.info(lang === 'de'
            ? 'Aktiviere Profile durch Anklicken der Checkboxen'
            : 'Activate profiles by clicking the checkboxes');
    },

    // Legacy edit modal - show disclaimer instead
    showEditModal(id) {
        const profile = this.items.find(p => p.id === id);
        if (profile) {
            this.showDisclaimer(profile.profile_type);
        }
    },

    // Delete is now just deactivation
    delete(id) {
        const profile = this.items.find(p => p.id === id);
        if (profile) {
            this.toggleProfile(profile.profile_type, false);
        }
    }
};
