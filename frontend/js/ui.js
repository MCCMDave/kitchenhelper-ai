// KitchenHelper-AI UI Helper Module

const UI = {
    // ==================== LOADING ====================
    showLoading(element) {
        element.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <span>Laden...</span>
            </div>
        `;
    },

    hideLoading(element) {
        const loading = element.querySelector('.loading');
        if (loading) loading.remove();
    },

    // ==================== ERROR ====================
    showError(element, message) {
        element.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">!</div>
                <p>${message}</p>
            </div>
        `;
    },

    // ==================== EMPTY STATE ====================
    showEmpty(element, message, icon = '') {
        element.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">${icon}</div>
                <p class="empty-state-title">${message}</p>
            </div>
        `;
    },

    // ==================== CLEAR ====================
    clear(element) {
        element.innerHTML = '';
    },

    // ==================== TOAST NOTIFICATIONS ====================
    toast(message, type = 'info') {
        // Ensure toast container exists
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }

        // Create toast
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <span>${message}</span>
            <button class="toast-close" onclick="this.parentElement.remove()">&times;</button>
        `;

        container.appendChild(toast);

        // Animate in
        setTimeout(() => toast.classList.add('show'), 10);

        // Auto remove
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    },

    success(message) {
        this.toast(message, 'success');
    },

    error(message) {
        this.toast(message, 'error');
    },

    warning(message) {
        this.toast(message, 'warning');
    },

    info(message) {
        this.toast(message, 'info');
    },

    // ==================== MODAL ====================
    showModal(options) {
        const { title, content, onConfirm, onCancel, confirmText = 'OK', cancelText = 'Abbrechen', showCancel = true } = options;

        // Create overlay
        const overlay = document.createElement('div');
        overlay.className = 'modal-overlay';
        overlay.innerHTML = `
            <div class="modal">
                <div class="modal-header">
                    <h3 class="modal-title">${title}</h3>
                    <button class="modal-close" data-action="close">&times;</button>
                </div>
                <div class="modal-body">
                    ${content}
                </div>
                <div class="modal-footer">
                    ${showCancel ? `<button class="btn btn-ghost" data-action="cancel">${cancelText}</button>` : ''}
                    <button class="btn btn-primary" data-action="confirm">${confirmText}</button>
                </div>
            </div>
        `;

        document.body.appendChild(overlay);

        // Animate in
        setTimeout(() => overlay.classList.add('show'), 10);

        // Event listeners
        const closeModal = () => {
            overlay.classList.remove('show');
            setTimeout(() => overlay.remove(), 300);
        };

        overlay.querySelector('[data-action="close"]').onclick = () => {
            closeModal();
            onCancel && onCancel();
        };

        if (showCancel) {
            overlay.querySelector('[data-action="cancel"]').onclick = () => {
                closeModal();
                onCancel && onCancel();
            };
        }

        overlay.querySelector('[data-action="confirm"]').onclick = () => {
            closeModal();
            onConfirm && onConfirm();
        };

        // Close on overlay click
        overlay.onclick = (e) => {
            if (e.target === overlay) {
                closeModal();
                onCancel && onCancel();
            }
        };

        return overlay;
    },

    // Confirmation dialog
    confirm(message, onConfirm) {
        return this.showModal({
            title: 'Bestätigung',
            content: `<p>${message}</p>`,
            onConfirm,
            confirmText: 'Ja',
            cancelText: 'Nein'
        });
    },

    // HTML Confirmation dialog (returns Promise)
    confirmHtml(htmlMessage, confirmText = 'Ja', cancelText = 'Nein') {
        return new Promise((resolve) => {
            const overlay = document.createElement('div');
            overlay.className = 'modal-overlay';
            overlay.innerHTML = `
                <div class="modal">
                    <div class="modal-header">
                        <h3 class="modal-title">Bestätigung</h3>
                        <button class="modal-close" data-action="close">&times;</button>
                    </div>
                    <div class="modal-body">
                        ${htmlMessage}
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-ghost" data-action="cancel">${cancelText}</button>
                        <button class="btn btn-primary" data-action="confirm">${confirmText}</button>
                    </div>
                </div>
            `;

            document.body.appendChild(overlay);
            setTimeout(() => overlay.classList.add('show'), 10);

            const closeModal = (result) => {
                overlay.classList.remove('show');
                setTimeout(() => overlay.remove(), 300);
                resolve(result);
            };

            overlay.querySelector('[data-action="close"]').onclick = () => closeModal(false);
            overlay.querySelector('[data-action="cancel"]').onclick = () => closeModal(false);
            overlay.querySelector('[data-action="confirm"]').onclick = () => closeModal(true);

            overlay.onclick = (e) => {
                if (e.target === overlay) closeModal(false);
            };
        });
    },

    // Form modal
    showFormModal(options) {
        const { title, fields, onSubmit, submitText = 'Speichern' } = options;

        let formHTML = fields.map(field => {
            if (field.type === 'select') {
                const optionsHTML = field.options.map(opt =>
                    `<option value="${opt.value}" ${opt.value === field.value ? 'selected' : ''}>${opt.label}</option>`
                ).join('');
                return `
                    <div class="form-group">
                        <label class="form-label">${field.label}</label>
                        <select class="form-control" name="${field.name}" ${field.required ? 'required' : ''}>
                            ${optionsHTML}
                        </select>
                    </div>
                `;
            } else if (field.type === 'checkbox') {
                return `
                    <div class="form-group">
                        <label class="checkbox">
                            <input type="checkbox" name="${field.name}" ${field.value ? 'checked' : ''}>
                            <span class="checkbox-box"></span>
                            <span>${field.label}</span>
                        </label>
                    </div>
                `;
            } else if (field.type === 'textarea') {
                return `
                    <div class="form-group">
                        <label class="form-label">${field.label}</label>
                        <textarea class="form-control" name="${field.name}"
                            placeholder="${field.placeholder || ''}"
                            ${field.required ? 'required' : ''}>${field.value || ''}</textarea>
                    </div>
                `;
            } else {
                return `
                    <div class="form-group">
                        <label class="form-label">${field.label}</label>
                        <input type="${field.type || 'text'}" class="form-control" name="${field.name}"
                            value="${field.value || ''}"
                            placeholder="${field.placeholder || ''}"
                            ${field.required ? 'required' : ''}>
                    </div>
                `;
            }
        }).join('');

        const overlay = this.showModal({
            title,
            content: `<form id="modal-form">${formHTML}</form>`,
            confirmText: submitText,
            onConfirm: () => {
                const form = document.getElementById('modal-form');
                const formData = new FormData(form);
                const data = {};

                fields.forEach(field => {
                    if (field.type === 'checkbox') {
                        data[field.name] = formData.get(field.name) === 'on';
                    } else if (field.type === 'number') {
                        data[field.name] = formData.get(field.name) ? Number(formData.get(field.name)) : null;
                    } else {
                        data[field.name] = formData.get(field.name);
                    }
                });

                onSubmit(data);
            }
        });

        return overlay;
    },

    // ==================== UTILITIES ====================
    formatDate(dateString) {
        if (!dateString) return '-';
        const date = new Date(dateString);
        return date.toLocaleDateString('de-DE', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        });
    },

    formatDateTime(dateString) {
        if (!dateString) return '-';
        const date = new Date(dateString);
        return date.toLocaleDateString('de-DE', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    isExpired(dateString) {
        if (!dateString) return false;
        return new Date(dateString) < new Date();
    },

    // Difficulty stars
    getDifficultyStars(level) {
        return Array(5).fill(0).map((_, i) =>
            i < level ? '*' : '-'
        ).join('');
    },

    // Escape HTML
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};
