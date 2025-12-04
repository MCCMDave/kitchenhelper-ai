// KitchenHelper-AI Food Scanner Module
// Barcode Scanning + OCR for ingredient lists

const Scanner = {
    // Scanner State
    html5QrCode: null,
    isScanning: false,
    currentMode: 'barcode', // 'barcode' or 'ocr'
    cameraId: null,

    // ==================== INITIALIZATION ====================
    async init() {
        console.log('[Scanner] Initializing...');

        // Load html5-qrcode library dynamically
        await this.loadLibraries();

        // Setup scanner UI
        this.setupUI();
    },

    async loadLibraries() {
        // Load html5-qrcode for barcode scanning
        if (!window.Html5Qrcode) {
            const script = document.createElement('script');
            script.src = 'https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.min.js';
            script.onload = () => console.log('[Scanner] html5-qrcode loaded');
            document.head.appendChild(script);

            // Wait for library to load
            await new Promise(resolve => {
                const interval = setInterval(() => {
                    if (window.Html5Qrcode) {
                        clearInterval(interval);
                        resolve();
                    }
                }, 100);
            });
        }

        // Load Tesseract.js for OCR
        if (!window.Tesseract) {
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js';
            script.onload = () => console.log('[Scanner] Tesseract.js loaded');
            document.head.appendChild(script);

            // Wait for library to load
            await new Promise(resolve => {
                const interval = setInterval(() => {
                    if (window.Tesseract) {
                        clearInterval(interval);
                        resolve();
                    }
                }, 100);
            });
        }
    },

    setupUI() {
        // Scanner mode tabs
        const barcodeModeBtn = document.getElementById('scanner-mode-barcode');
        const ocrModeBtn = document.getElementById('scanner-mode-ocr');

        if (barcodeModeBtn) {
            barcodeModeBtn.addEventListener('click', () => this.switchMode('barcode'));
        }
        if (ocrModeBtn) {
            ocrModeBtn.addEventListener('click', () => this.switchMode('ocr'));
        }

        // Scanner controls
        const startBtn = document.getElementById('scanner-start');
        const stopBtn = document.getElementById('scanner-stop');

        if (startBtn) {
            startBtn.addEventListener('click', () => this.startScanner());
        }
        if (stopBtn) {
            stopBtn.addEventListener('click', () => this.stopScanner());
        }
    },

    // ==================== MODE SWITCHING ====================
    switchMode(mode) {
        this.currentMode = mode;

        // Update tabs
        document.querySelectorAll('.scanner-mode-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.getElementById(`scanner-mode-${mode}`).classList.add('active');

        // Update UI sections
        document.getElementById('barcode-section').style.display = mode === 'barcode' ? 'block' : 'none';
        document.getElementById('ocr-section').style.display = mode === 'ocr' ? 'block' : 'none';

        // Stop current scan
        if (this.isScanning) {
            this.stopScanner();
        }

        console.log(`[Scanner] Switched to ${mode} mode`);
    },

    // ==================== BARCODE SCANNING ====================
    async startScanner() {
        if (this.isScanning) {
            console.log('[Scanner] Already scanning');
            return;
        }

        try {
            if (this.currentMode === 'barcode') {
                await this.startBarcodeScanner();
            } else {
                await this.startOCRScanner();
            }
        } catch (error) {
            console.error('[Scanner] Start failed:', error);
            UI.error(i18n.currentLang === 'de'
                ? 'Kamera konnte nicht gestartet werden.'
                : 'Could not start camera.');
        }
    },

    async startBarcodeScanner() {
        this.html5QrCode = new Html5Qrcode("scanner-reader");

        const config = {
            fps: 10,
            qrbox: { width: 250, height: 250 },
            aspectRatio: 1.0
        };

        try {
            await this.html5QrCode.start(
                { facingMode: "environment" }, // Use back camera
                config,
                (decodedText, decodedResult) => {
                    console.log(`[Scanner] Barcode detected: ${decodedText}`);
                    this.handleBarcodeDetected(decodedText);
                },
                (errorMessage) => {
                    // Scanning errors (can be ignored)
                }
            );

            this.isScanning = true;
            this.updateScannerControls();
            console.log('[Scanner] Barcode scanner started');

        } catch (error) {
            console.error('[Scanner] Barcode scanner failed:', error);
            throw error;
        }
    },

    async handleBarcodeDetected(barcode) {
        // Stop scanner temporarily
        await this.stopScanner();

        // Show loading
        UI.showLoading(i18n.t('scanner.loading_product'));

        try {
            // Fetch product data from backend
            const response = await api.scanBarcode(barcode);

            if (!response.found) {
                UI.error(i18n.currentLang === 'de'
                    ? `Produkt mit Barcode ${barcode} nicht gefunden.`
                    : `Product with barcode ${barcode} not found.`);
                return;
            }

            // Show product details
            this.showProductDetails(response);

        } catch (error) {
            console.error('[Scanner] Failed to fetch product:', error);
            UI.error(i18n.t('scanner.error_loading_product'));
        } finally {
            UI.hideLoading();
        }
    },

    showProductDetails(product) {
        const lang = i18n.currentLang;
        const productName = Sanitize.escapeHTML(product[`product_name_${lang}`] || product.product_name || i18n.t('scanner.unknown_product'));
        const ingredientsText = Sanitize.escapeHTML(product[`ingredients_text_${lang}`] || product.ingredients_text || '');
        const brands = Sanitize.escapeHTML(product.brands || '');
        const categories = Sanitize.escapeHTML(product.categories || '');
        const imageUrl = Sanitize.escapeHTML(product.image_url || '');
        const nutriscoreGrade = product.nutriscore_grade ? Sanitize.escapeHTML(product.nutriscore_grade) : '';

        const resultDiv = document.getElementById('scanner-result');
        Sanitize.setHTML(resultDiv, `
            <div class="card scanner-product-card">
                ${imageUrl ? `<img src="${imageUrl}" alt="${productName}" class="scanner-product-image">` : ''}
                <h3>${productName}</h3>
                ${brands ? `<p><strong>${i18n.t('scanner.brands')}:</strong> ${brands}</p>` : ''}
                ${categories ? `<p><strong>${i18n.t('scanner.categories')}:</strong> ${categories}</p>` : ''}
                ${nutriscoreGrade ? `<p><strong>Nutri-Score:</strong> <span class="nutriscore-${nutriscoreGrade}">${nutriscoreGrade.toUpperCase()}</span></p>` : ''}

                ${ingredientsText ? `
                    <div class="scanner-ingredients">
                        <h4>${i18n.t('scanner.ingredients')}</h4>
                        <p>${ingredientsText}</p>
                    </div>
                ` : ''}

                <div class="scanner-actions">
                    <button class="btn btn-primary" onclick="Scanner.addIngredientsFromProduct('${ingredientsText}')">
                        ${i18n.t('scanner.add_ingredients')}
                    </button>
                    <button class="btn btn-outline" onclick="Scanner.startScanner()">
                        ${i18n.t('scanner.scan_another')}
                    </button>
                </div>
            </div>
        `);
        resultDiv.style.display = 'block';
    },

    async addIngredientsFromProduct(ingredientsText) {
        if (!ingredientsText) {
            UI.error(i18n.t('scanner.no_ingredients'));
            return;
        }

        // Parse ingredients (simple split by comma)
        const ingredients = ingredientsText
            .split(',')
            .map(i => i.trim())
            .filter(i => i.length > 0)
            .slice(0, 10); // Limit to first 10 ingredients

        // Show ingredient selection modal
        this.showIngredientSelectionModal(ingredients);
    },

    showIngredientSelectionModal(ingredients) {
        // Create modal for ingredient selection
        const modal = UI.createModal(i18n.t('scanner.select_ingredients'));

        const checkboxes = ingredients.map((ing, index) => `
            <div class="form-check">
                <input type="checkbox" id="ing-${index}" value="${ing}" checked>
                <label for="ing-${index}">${ing}</label>
            </div>
        `).join('');

        modal.setContent(`
            <div class="scanner-ingredient-selection">
                <p>${i18n.t('scanner.select_ingredients_hint')}</p>
                ${checkboxes}
                <div style="margin-top: var(--spacing-lg);">
                    <button class="btn btn-primary" onclick="Scanner.confirmIngredientSelection()">
                        ${i18n.t('common.add')}
                    </button>
                    <button class="btn btn-outline" onclick="UI.closeModal()">
                        ${i18n.t('common.cancel')}
                    </button>
                </div>
            </div>
        `);

        modal.show();
    },

    async confirmIngredientSelection() {
        const selected = [];
        document.querySelectorAll('.scanner-ingredient-selection input[type="checkbox"]:checked').forEach(cb => {
            selected.push(cb.value);
        });

        if (selected.length === 0) {
            UI.error(i18n.t('scanner.no_ingredients_selected'));
            return;
        }

        // Add ingredients to user's inventory
        for (const ingredient of selected) {
            try {
                await api.addIngredient({
                    name: ingredient,
                    quantity: 1,
                    unit: 'x',
                    category: 'other'
                });
            } catch (error) {
                console.error(`[Scanner] Failed to add ingredient ${ingredient}:`, error);
            }
        }

        UI.closeModal();
        UI.success(i18n.currentLang === 'de'
            ? `${selected.length} Zutat(en) hinzugefügt!`
            : `${selected.length} ingredient(s) added!`);

        // Reload ingredients
        await Ingredients.load();
    },

    // ==================== OCR SCANNING ====================
    async startOCRScanner() {
        // Show camera preview
        const videoElement = document.getElementById('ocr-video');

        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: "environment" }
            });

            videoElement.srcObject = stream;
            videoElement.play();

            this.isScanning = true;
            this.updateScannerControls();

            // Show capture button
            document.getElementById('ocr-capture').style.display = 'block';

        } catch (error) {
            console.error('[Scanner] OCR camera failed:', error);
            throw error;
        }
    },

    async captureOCRImage() {
        const videoElement = document.getElementById('ocr-video');
        const canvas = document.createElement('canvas');
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;

        const ctx = canvas.getContext('2d');
        ctx.drawImage(videoElement, 0, 0);

        // Convert to blob
        canvas.toBlob(async (blob) => {
            await this.processOCRImage(blob);
        }, 'image/jpeg', 0.9);
    },

    async processOCRImage(imageBlob) {
        UI.showLoading(i18n.t('scanner.processing_ocr'));

        try {
            const { data: { text } } = await Tesseract.recognize(
                imageBlob,
                i18n.currentLang === 'de' ? 'deu' : 'eng',
                {
                    logger: m => console.log('[OCR]', m)
                }
            );

            console.log('[Scanner] OCR Result:', text);

            // Parse ingredients from text
            const ingredients = this.parseIngredientsFromOCR(text);

            if (ingredients.length === 0) {
                UI.error(i18n.t('scanner.no_ingredients_found'));
                return;
            }

            // Show ingredient selection
            this.showIngredientSelectionModal(ingredients);

        } catch (error) {
            console.error('[Scanner] OCR failed:', error);
            UI.error(i18n.t('scanner.ocr_error'));
        } finally {
            UI.hideLoading();
        }
    },

    parseIngredientsFromOCR(text) {
        // Simple parsing: Split by common delimiters
        const delimiters = /[,;:\n]/;
        const ingredients = text
            .split(delimiters)
            .map(i => i.trim())
            .filter(i => i.length > 2 && i.length < 50) // Filter noise
            .slice(0, 15); // Limit to 15

        return ingredients;
    },

    // ==================== CONTROLS ====================
    async stopScanner() {
        if (!this.isScanning) {
            return;
        }

        try {
            if (this.currentMode === 'barcode' && this.html5QrCode) {
                await this.html5QrCode.stop();
                this.html5QrCode = null;
            } else if (this.currentMode === 'ocr') {
                const videoElement = document.getElementById('ocr-video');
                if (videoElement.srcObject) {
                    videoElement.srcObject.getTracks().forEach(track => track.stop());
                    videoElement.srcObject = null;
                }
                document.getElementById('ocr-capture').style.display = 'none';
            }

            this.isScanning = false;
            this.updateScannerControls();
            console.log('[Scanner] Stopped');

        } catch (error) {
            console.error('[Scanner] Stop failed:', error);
        }
    },

    updateScannerControls() {
        const startBtn = document.getElementById('scanner-start');
        const stopBtn = document.getElementById('scanner-stop');

        if (startBtn) startBtn.style.display = this.isScanning ? 'none' : 'inline-block';
        if (stopBtn) stopBtn.style.display = this.isScanning ? 'inline-block' : 'none';
    }
};
