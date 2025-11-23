// KitchenHelper-AI User Menu Module

const UserMenu = {
    isOpen: false,

    // Toggle dropdown visibility
    toggle(event) {
        if (event) {
            event.stopPropagation();
        }

        const dropdown = document.getElementById('user-dropdown');
        this.isOpen = !this.isOpen;

        if (this.isOpen) {
            dropdown.classList.add('show');
        } else {
            dropdown.classList.remove('show');
        }

        console.log('[UserMenu] Toggle:', this.isOpen);
    },

    // Close dropdown
    close() {
        const dropdown = document.getElementById('user-dropdown');
        if (dropdown) {
            dropdown.classList.remove('show');
            this.isOpen = false;
        }
    },

    // Navigate to settings
    goToSettings() {
        this.close();
        const settingsTab = document.querySelector('[data-section="settings"]');
        if (settingsTab) {
            settingsTab.click();
        }
    },

    // Navigate to profiles
    goToProfiles() {
        this.close();
        const profilesTab = document.querySelector('[data-section="profiles"]');
        if (profilesTab) {
            profilesTab.click();
        }
    },

    // Update user info in menu
    updateUserInfo(user) {
        if (!user) return;

        // Update tier badge
        const tierBadge = document.getElementById('user-tier');
        if (tierBadge) {
            tierBadge.textContent = user.subscription_tier.toUpperCase();

            // Add tier-specific class
            tierBadge.className = 'user-tier-badge tier-' + user.subscription_tier;
        }

        // Update emoji (use user emoji or default)
        const userEmoji = document.getElementById('user-emoji');
        if (userEmoji) {
            userEmoji.textContent = user.emoji || '👤';
        }

        // Update dropdown header
        const dropdownName = document.getElementById('dropdown-name');
        const dropdownEmail = document.getElementById('dropdown-email');

        if (dropdownName) {
            dropdownName.textContent = user.username || 'User';
        }
        if (dropdownEmail) {
            dropdownEmail.textContent = user.email;
        }

        console.log('[UserMenu] Updated user info:', user.username || user.email);
    },

    // Set user emoji
    async setEmoji(emoji) {
        try {
            const user = await Auth.updateProfile({ emoji });
            const userEmoji = document.getElementById('user-emoji');
            if (userEmoji) {
                userEmoji.textContent = emoji;
            }
            UI.success('Emoji aktualisiert!');
            console.log('[UserMenu] Emoji updated to:', emoji);
        } catch (error) {
            console.error('[UserMenu] Emoji update error:', error);
            UI.error('Fehler beim Aktualisieren des Emojis');
        }
    }
};

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.user-menu')) {
        UserMenu.close();
    }
});

// Close dropdown on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        UserMenu.close();
    }
});
