// Session Timeout Handler
// Automatically logs out user after 15 minutes of inactivity

const SessionTimeout = {
    timeout: 15 * 60 * 1000, // 15 minutes
    warningTime: 2 * 60 * 1000, // Show warning 2 min before timeout
    timer: null,
    warningTimer: null,

    init() {
        if (!Auth.isAuthenticated()) {
            return; // Only run for logged-in users
        }

        this.resetTimer();

        // Listen for user activity
        const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
        events.forEach(event => {
            document.addEventListener(event, () => this.resetTimer(), true);
        });
    },

    resetTimer() {
        // Clear existing timers
        if (this.timer) clearTimeout(this.timer);
        if (this.warningTimer) clearTimeout(this.warningTimer);

        // Set warning timer (2 min before logout)
        this.warningTimer = setTimeout(() => {
            this.showWarning();
        }, this.timeout - this.warningTime);

        // Set logout timer (15 min)
        this.timer = setTimeout(() => {
            this.logout();
        }, this.timeout);
    },

    showWarning() {
        const message = i18n.t('session.timeout_warning') ||
                       'Du wirst in 2 Minuten aufgrund von Inaktivität abgemeldet.';

        // Show non-intrusive warning
        const warning = document.createElement('div');
        warning.id = 'session-warning';
        warning.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ff9800;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            z-index: 10000;
            max-width: 300px;
            animation: slideIn 0.3s ease-out;
        `;
        Sanitize.setHTML(warning, `
            <strong>⚠️ Sitzung läuft ab</strong><br>
            <span style="font-size: 14px;">${Sanitize.escapeHTML(message)}</span>
        `);

        document.body.appendChild(warning);

        // Remove warning after 5 seconds or on activity
        setTimeout(() => {
            const existingWarning = document.getElementById('session-warning');
            if (existingWarning) {
                existingWarning.remove();
            }
        }, 5000);
    },

    logout() {
        console.log('[SessionTimeout] Auto-logout due to inactivity');

        // Show logout message
        alert(i18n.t('session.logged_out') || 'Du wurdest aufgrund von Inaktivität abgemeldet.');

        // Perform logout
        Auth.logout();
    },

    destroy() {
        // Clean up timers
        if (this.timer) clearTimeout(this.timer);
        if (this.warningTimer) clearTimeout(this.warningTimer);
    }
};

// Auto-init on dashboard
if (window.location.pathname.includes('dashboard.html')) {
    document.addEventListener('DOMContentLoaded', () => {
        SessionTimeout.init();
    });
}
