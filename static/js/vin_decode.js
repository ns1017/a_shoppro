function initVinLookup() {
    const container = document.querySelector('[data-vin-lookup]');
    if (!container) return;

    const lookupUrl = container.dataset.vinLookupUrl;
    const vinInput = document.getElementById('id_vin');
    const yearInput = document.getElementById('id_year');
    const makeInput = document.getElementById('id_make');
    const modelInput = document.getElementById('id_model');
    const statusEl = container.querySelector('[data-vin-status]');

    if (!lookupUrl || !vinInput || !yearInput || !makeInput || !modelInput) return;

    const cachePrefix = 'autoshop:vin-decode:';
    const cacheTtlMs = 1000 * 60 * 60 * 24 * 30;
    let lookupController = null;
    let lookupTimer = null;
    let lastVin = '';

    function normalizeVin(value) {
        return (value || '').trim().toUpperCase();
    }

    function setStatus(message, isError = false) {
        if (!statusEl) return;
        statusEl.textContent = message;
        statusEl.className = `mt-2 text-xs ${isError ? 'text-red-600' : 'text-slate-500'}`;
    }

    function readCache(vin) {
        try {
            const raw = localStorage.getItem(cachePrefix + vin);
            if (!raw) return null;
            const payload = JSON.parse(raw);
            if (!payload || !payload.timestamp || !payload.data) return null;
            if (Date.now() - payload.timestamp > cacheTtlMs) {
                localStorage.removeItem(cachePrefix + vin);
                return null;
            }
            return payload.data;
        } catch (_error) {
            return null;
        }
    }

    function writeCache(vin, data) {
        try {
            localStorage.setItem(cachePrefix + vin, JSON.stringify({
                timestamp: Date.now(),
                data,
            }));
        } catch (_error) {
            // Ignore storage quota or privacy mode failures.
        }
    }

    function applyDecodedData(data) {
        if (!data) return;

        if (data.year) {
            yearInput.value = data.year;
        }
        if (data.make) {
            makeInput.value = data.make;
        }
        if (data.model) {
            modelInput.value = data.model;
        }
    }

    async function fetchVinData(vin) {
        const cachedData = readCache(vin);
        if (cachedData) {
            applyDecodedData(cachedData);
            setStatus('Vehicle data loaded from browser cache.');
            lastVin = vin;
            return;
        }

        if (lookupController) {
            lookupController.abort();
        }

        lookupController = new AbortController();
        setStatus('Decoding VIN...');

        try {
            const response = await fetch(`${lookupUrl}?vin=${encodeURIComponent(vin)}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                signal: lookupController.signal,
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || 'Unable to decode VIN.');
            }

            applyDecodedData(data);
            writeCache(vin, data);
            setStatus(data.cached ? 'Vehicle data loaded from server cache.' : 'Vehicle data decoded successfully.');
            lastVin = vin;
        } catch (error) {
            if (error.name === 'AbortError') return;
            setStatus(error.message || 'Unable to decode VIN.', true);
        }
    }

    function scheduleLookup() {
        const vin = normalizeVin(vinInput.value);
        if (vin === lastVin && vin.length === 17) return;

        if (lookupTimer) {
            window.clearTimeout(lookupTimer);
        }

        if (vin.length < 17) {
            setStatus('Enter a full 17-character VIN to auto-fill year, make, and model.');
            return;
        }

        lookupTimer = window.setTimeout(() => {
            fetchVinData(vin);
        }, 350);
    }

    vinInput.addEventListener('input', scheduleLookup);
    vinInput.addEventListener('blur', scheduleLookup);

    const initialVin = normalizeVin(vinInput.value);
    if (initialVin.length === 17) {
        fetchVinData(initialVin);
    }
}

document.addEventListener('DOMContentLoaded', initVinLookup);