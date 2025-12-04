// HTML Sanitization Helper
// Prevents XSS attacks by escaping HTML entities

const Sanitize = {
    /**
     * Escape HTML entities to prevent XSS
     * @param {string} html - Unsafe HTML string
     * @returns {string} - Safe escaped string
     */
    escapeHTML(html) {
        if (typeof html !== 'string') {
            return '';
        }

        const div = document.createElement('div');
        div.textContent = html;
        return div.innerHTML;
    },

    /**
     * Safe innerHTML replacement
     * Use: Sanitize.setHTML(element, unsafeHTML)
     * @param {HTMLElement} element - Target element
     * @param {string} html - HTML string to sanitize
     */
    setHTML(element, html) {
        element.innerHTML = this.escapeHTML(html);
    },

    /**
     * Sanitize user input for display
     * Allows basic formatting but strips scripts/events
     * @param {string} text - User input
     * @returns {string} - Sanitized text
     */
    sanitizeUserInput(text) {
        if (typeof text !== 'string') {
            return '';
        }

        return text
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#x27;')
            .replace(/\//g, '&#x2F;');
    },

    /**
     * Safe way to append text (no HTML interpretation)
     * @param {HTMLElement} element - Target element
     * @param {string} text - Text to append
     */
    setText(element, text) {
        element.textContent = text;
    }
};

// Export for use in other scripts
window.Sanitize = Sanitize;
