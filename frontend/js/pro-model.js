// KitchenHelper-AI Pro Model Module

const ProModel = {
    // Update display with current tier
    updateDisplay() {
        const user = Auth.currentUser;
        if (!user) return;

        const tierDisplay = document.getElementById('current-tier-display');
        const subscribeBtn = document.getElementById('pro-subscribe-btn');

        if (tierDisplay) {
            const tier = user.subscription_tier || 'demo';
            tierDisplay.textContent = tier.toUpperCase();

            // Update color based on tier
            if (tier === 'pro') {
                tierDisplay.style.color = 'var(--success)';
            } else {
                tierDisplay.style.color = 'var(--primary)';
            }
        }

        // Hide/show upgrade button based on tier
        if (subscribeBtn) {
            if (user.subscription_tier === 'pro') {
                subscribeBtn.textContent = '✅ ' + i18n.t('pro.already_pro');
                subscribeBtn.disabled = true;
                subscribeBtn.style.opacity = '0.6';
            } else {
                subscribeBtn.innerHTML = '💎 <span data-i18n="pro.upgrade_now">Jetzt upgraden</span>';
                subscribeBtn.disabled = false;
                subscribeBtn.style.opacity = '1';
            }
        }

        console.log('[ProModel] Display updated for tier:', user.subscription_tier);
    },

    // Subscribe to Pro
    async subscribe() {
        const user = Auth.currentUser;

        if (!user) {
            UI.error(i18n.t('pro.login_required'));
            return;
        }

        if (user.subscription_tier === 'pro') {
            UI.info(i18n.t('pro.already_subscribed'));
            return;
        }

        // Confirm subscription
        if (!confirm(i18n.t('pro.confirm_subscribe'))) {
            return;
        }

        try {
            UI.showLoading(i18n.t('pro.processing'));

            // Call API to upgrade to Pro
            const response = await API.post('/users/subscribe', {
                tier: 'pro',
                payment_method: 'stripe' // TODO: Implement actual payment
            });

            if (response.success) {
                // Update local user data
                Auth.currentUser.subscription_tier = 'pro';

                // Update UI
                UserMenu.updateUserInfo(Auth.currentUser);
                this.updateDisplay();

                UI.hideLoading();
                UI.success(i18n.t('pro.upgrade_success'));

                console.log('[ProModel] Upgraded to Pro successfully');
            } else {
                throw new Error(response.message || 'Subscription failed');
            }
        } catch (error) {
            console.error('[ProModel] Subscription error:', error);
            UI.hideLoading();
            UI.error(i18n.t('pro.upgrade_error') + ': ' + error.message);
        }
    },

    // Cancel subscription
    async cancel() {
        const user = Auth.currentUser;

        if (!user || user.subscription_tier !== 'pro') {
            UI.error(i18n.t('pro.not_subscribed'));
            return;
        }

        // Confirm cancellation
        if (!confirm(i18n.t('pro.confirm_cancel'))) {
            return;
        }

        try {
            UI.showLoading(i18n.t('pro.processing'));

            const response = await API.post('/users/cancel-subscription');

            if (response.success) {
                // Update local user data
                Auth.currentUser.subscription_tier = 'demo';

                // Update UI
                UserMenu.updateUserInfo(Auth.currentUser);
                this.updateDisplay();

                UI.hideLoading();
                UI.success(i18n.t('pro.cancel_success'));

                console.log('[ProModel] Subscription cancelled');
            } else {
                throw new Error(response.message || 'Cancellation failed');
            }
        } catch (error) {
            console.error('[ProModel] Cancellation error:', error);
            UI.hideLoading();
            UI.error(i18n.t('pro.cancel_error') + ': ' + error.message);
        }
    }
};
