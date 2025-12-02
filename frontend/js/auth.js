// KitchenHelper-AI Auth Module

const Auth = {
    // Check if user is authenticated
    isAuthenticated() {
        return !!api.getToken();
    },

    // Get current user from localStorage
    getCurrentUser() {
        const userJson = localStorage.getItem(CONFIG.USER_KEY);
        try {
            return userJson ? JSON.parse(userJson) : null;
        } catch {
            return null;
        }
    },

    // Save user to localStorage
    saveUser(user) {
        localStorage.setItem(CONFIG.USER_KEY, JSON.stringify(user));
    },

    // Login (mit Email oder Username)
    async login(emailOrUsername, password) {
        try {
            console.log('[Auth] Login attempt:', emailOrUsername);
            const response = await api.login(emailOrUsername, password);
            api.setToken(response.access_token);

            // Fetch and save user data
            const user = await api.getMe();
            this.saveUser(user);

            console.log('[Auth] Login successful:', user.username);
            return user;
        } catch (error) {
            console.error('[Auth] Login failed:', error);
            throw error;
        }
    },

    // Register (mit Username statt Name)
    async register(email, username, password) {
        try {
            console.log('[Auth] Register attempt:', { email, username });
            // Register user
            await api.register(email, username, password);
            // Then login
            const user = await this.login(email, password);

            // Send verification email
            try {
                await api.sendVerificationEmail(email);
                console.log('[Auth] Verification email sent to:', email);
            } catch (emailError) {
                console.warn('[Auth] Failed to send verification email:', emailError);
                // Don't fail registration if email fails
            }

            return user;
        } catch (error) {
            console.error('[Auth] Register failed:', error);
            throw error;
        }
    },

    // Logout
    logout() {
        api.clearToken();
        window.location.href = 'index.html';
    },

    // Require authentication - redirect if not logged in
    requireAuth() {
        if (!this.isAuthenticated()) {
            window.location.href = 'index.html';
            return false;
        }
        return true;
    },

    // Redirect if already authenticated
    redirectIfAuthenticated() {
        if (this.isAuthenticated()) {
            window.location.href = 'dashboard.html';
            return true;
        }
        return false;
    },

    // Refresh user data from API
    async refreshUser() {
        try {
            const user = await api.getMe();
            this.saveUser(user);
            return user;
        } catch (error) {
            console.error('Failed to refresh user:', error);
            return null;
        }
    },

    // Update user profile
    async updateProfile(data) {
        try {
            const user = await api.updateMe(data);
            this.saveUser(user);
            return user;
        } catch (error) {
            throw error;
        }
    },

    // Get user tier info
    getTierInfo() {
        const user = this.getCurrentUser();
        if (!user) return CONFIG.TIERS.demo;
        return CONFIG.TIERS[user.subscription_tier] || CONFIG.TIERS.demo;
    }
};
