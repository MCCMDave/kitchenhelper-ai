/**
 * Tier Manager - Frontend Tier-Checks für Feature-Gating
 *
 * Synchronisiert mit Backend Tier-System:
 * - FREE: Basis-Features (langsame Generierung, 10 Favoriten, Basis-Nährwerte)
 * - BASIC: 6x schneller, GI/GL, unbegrenzte Favoriten
 * - PREMIUM: 25x schneller, Meal-Planning, Carb-Budget
 * - PRO: 38x schneller, API, Teams, White-Label
 * - BUSINESS: SLA, Priority Support, Invoice Billing
 */

class TierManager {
    constructor() {
        this.currentTier = 'free';
        this.isAdmin = false;
        this.features = {};
    }

    /**
     * Initialisiert Tier-Manager mit User-Daten
     */
    async init() {
        try {
            const response = await api.request('/users/me');
            this.currentTier = response.subscription_tier || 'free';
            this.isAdmin = response.is_admin || false;
            this.features = this._loadFeatureAccess();

            console.log(`[TierManager] Initialized: ${this.currentTier} (Admin: ${this.isAdmin})`);

            // Update UI
            this._updateUI();
        } catch (error) {
            console.error('[TierManager] Init failed:', error);
            this.currentTier = 'free';
        }
    }

    /**
     * Lädt Feature-Access basierend auf Tier
     */
    _loadFeatureAccess() {
        const allTiers = ['free', 'basic', 'premium', 'pro', 'business_solo', 'business_team', 'business_praxis'];
        const tierIndex = allTiers.indexOf(this.currentTier);

        return {
            // FREE Tier
            recipe_generation: tierIndex >= 0,
            basic_nutrition: tierIndex >= 0,
            be_calculation: tierIndex >= 0,
            pdf_export_favorites: tierIndex >= 0,

            // BASIC Tier+
            recipe_db: tierIndex >= 1,
            gi_gl: tierIndex >= 1,
            pdf_export_all: tierIndex >= 1,
            shopping_lists: tierIndex >= 1,

            // PREMIUM Tier+
            meal_planning: tierIndex >= 2,
            carb_budget: tierIndex >= 2,
            advanced_filters: tierIndex >= 2,

            // PRO Tier+
            api_access: tierIndex >= 3,
            team_sharing: tierIndex >= 3 && tierIndex !== 4, // Nicht BUSINESS_SOLO
            white_label: tierIndex >= 3,

            // BUSINESS Tiers
            sla_guarantee: tierIndex >= 4,
            priority_support: tierIndex >= 4,
            invoice_billing: tierIndex >= 4,
        };
    }

    /**
     * Prüft ob User Feature hat
     */
    hasFeature(feature) {
        if (this.isAdmin) return true; // Admin hat alle Features
        return this.features[feature] || false;
    }

    /**
     * Gibt Tier-Info zurück
     */
    getTierInfo() {
        const tierInfo = {
            free: {
                name: 'FREE',
                price: '0€',
                color: '#6c757d',
                icon: '🆓',
                speed: '1x (76s)',
                favorites: 10,
                db_size: 0,
            },
            basic: {
                name: 'BASIC',
                price: '2,99€/Monat',
                color: '#28a745',
                icon: '🌱',
                speed: '6x (12s)',
                favorites: 'Unbegrenzt',
                db_size: 1000,
            },
            premium: {
                name: 'PREMIUM',
                price: '4,99€/Monat',
                color: '#007bff',
                icon: '⭐',
                speed: '25x (3s)',
                favorites: 'Unbegrenzt',
                db_size: 10000,
            },
            pro: {
                name: 'PRO',
                price: '9,99€/Monat',
                color: '#6f42c1',
                icon: '💎',
                speed: '38x (2s)',
                favorites: 'Unbegrenzt',
                db_size: 50000,
            },
            business_solo: {
                name: 'BUSINESS Solo',
                price: '19,99€/Monat',
                color: '#fd7e14',
                icon: '🏢',
                speed: '38x (2s)',
                favorites: 'Unbegrenzt',
                db_size: 50000,
            },
        };

        return tierInfo[this.currentTier] || tierInfo.free;
    }

    /**
     * Gibt max Favoriten zurück
     */
    getMaxFavorites() {
        if (this.isAdmin) return 999999;
        return this.currentTier === 'free' ? 10 : 999999;
    }

    /**
     * Zeigt Upgrade-Modal wenn Feature nicht verfügbar
     */
    showUpgradeModal(feature) {
        const featureNames = {
            recipe_db: 'Rezept-Datenbank (6x schneller)',
            gi_gl: 'Glykämischer Index (GI/GL)',
            meal_planning: 'Meal-Planning',
            carb_budget: 'Kohlenhydrat-Budget',
            api_access: 'API-Zugang',
        };

        const requiredTier = this._getRequiredTier(feature);
        const tierInfo = this.getTierInfo();
        const requiredTierInfo = requiredTier ? this._getTierInfoByName(requiredTier) : null;

        UI.showModal({
            title: '🔒 Feature gesperrt',
            content: `
                <div style="text-align: center; padding: 20px;">
                    <p style="font-size: 18px; margin-bottom: 20px;">
                        <strong>${featureNames[feature] || feature}</strong> ist nur für höhere Tiers verfügbar.
                    </p>

                    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                        <p style="margin: 0;">Dein aktuelles Tier:</p>
                        <p style="font-size: 24px; font-weight: bold; color: ${tierInfo.color}; margin: 10px 0;">
                            ${tierInfo.icon} ${tierInfo.name}
                        </p>
                        <p style="margin: 0; color: #6c757d;">${tierInfo.price}</p>
                    </div>

                    ${requiredTierInfo ? `
                        <div style="background: linear-gradient(135deg, ${requiredTierInfo.color}22, ${requiredTierInfo.color}11); padding: 15px; border-radius: 8px; border: 2px solid ${requiredTierInfo.color};">
                            <p style="margin: 0;">Upgrade auf:</p>
                            <p style="font-size: 28px; font-weight: bold; color: ${requiredTierInfo.color}; margin: 10px 0;">
                                ${requiredTierInfo.icon} ${requiredTierInfo.name}
                            </p>
                            <p style="margin: 0; font-weight: bold;">${requiredTierInfo.price}</p>
                        </div>
                    ` : ''}

                    <button onclick="window.location.href='/settings.html'"
                            style="margin-top: 20px; padding: 12px 30px; font-size: 16px; background: ${requiredTierInfo?.color || '#007bff'}; color: white; border: none; border-radius: 6px; cursor: pointer;">
                        🚀 Jetzt upgraden
                    </button>
                </div>
            `,
        });
    }

    /**
     * Gibt benötigtes Tier für Feature zurück
     */
    _getRequiredTier(feature) {
        const featureTiers = {
            recipe_db: 'basic',
            gi_gl: 'basic',
            pdf_export_all: 'basic',
            shopping_lists: 'basic',
            meal_planning: 'premium',
            carb_budget: 'premium',
            advanced_filters: 'premium',
            api_access: 'pro',
            team_sharing: 'pro',
            white_label: 'pro',
        };
        return featureTiers[feature];
    }

    /**
     * Gibt Tier-Info nach Name zurück
     */
    _getTierInfoByName(tierName) {
        const tierInfo = {
            basic: {
                name: 'BASIC',
                price: '2,99€/Monat',
                color: '#28a745',
                icon: '🌱',
            },
            premium: {
                name: 'PREMIUM',
                price: '4,99€/Monat',
                color: '#007bff',
                icon: '⭐',
            },
            pro: {
                name: 'PRO',
                price: '9,99€/Monat',
                color: '#6f42c1',
                icon: '💎',
            },
        };
        return tierInfo[tierName];
    }

    /**
     * Updated UI mit Tier-Badge
     */
    _updateUI() {
        const tierInfo = this.getTierInfo();

        // Badge im Header hinzufügen
        const tierBadge = document.getElementById('tier-badge');
        if (tierBadge) {
            tierBadge.innerHTML = `
                <span style="background: ${tierInfo.color}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;">
                    ${tierInfo.icon} ${tierInfo.name}
                </span>
            `;
        }

        // Admin-Badge hinzufügen
        if (this.isAdmin) {
            const adminBadge = document.getElementById('admin-badge');
            if (adminBadge) {
                adminBadge.innerHTML = `
                    <span style="background: #dc3545; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-left: 8px;">
                        👑 ADMIN
                    </span>
                `;
            }
        }
    }
}

// Global instance
const tierManager = new TierManager();

// Auto-init when DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => tierManager.init());
} else {
    tierManager.init();
}
