/**
 * data-cache.js — Lightweight localStorage cache layer
 * OSRS Profit Finder tool
 * Provides shared caching utilities for all modules
 */
(function() {
    'use strict';

    const CACHE_PREFIX = 'osrsguru_pf_';

    const Cache = {
        /**
         * Set a cached value with expiration
         * @param {string} key - Cache key (prefix auto-added)
         * @param {*} value - Value to store (JSON-serializable)
         * @param {number} ttlMs - Time to live in milliseconds (default 1 hour)
         */
        set: function(key, value, ttlMs) {
            ttlMs = ttlMs || 3600000; // default 1 hour
            try {
                const entry = {
                    value: value,
                    expires: Date.now() + ttlMs,
                    created: Date.now()
                };
                localStorage.setItem(CACHE_PREFIX + key, JSON.stringify(entry));
                return true;
            } catch (e) {
                console.warn('Cache.set failed for key:', key, e);
                return false;
            }
        },

        /**
         * Get a cached value
         * @param {string} key - Cache key (prefix auto-added)
         * @returns {*|null} - Cached value or null if expired/missing
         */
        get: function(key) {
            try {
                const raw = localStorage.getItem(CACHE_PREFIX + key);
                if (!raw) return null;

                const entry = JSON.parse(raw);
                if (Date.now() > entry.expires) {
                    localStorage.removeItem(CACHE_PREFIX + key);
                    return null;
                }
                return entry.value;
            } catch (e) {
                return null;
            }
        },

        /**
         * Remove a cached entry
         * @param {string} key - Cache key (prefix auto-added)
         */
        remove: function(key) {
            try {
                localStorage.removeItem(CACHE_PREFIX + key);
            } catch (e) { /* silent */ }
        },

        /**
         * Clear all cache entries with our prefix
         */
        clearAll: function() {
            try {
                const keysToRemove = [];
                for (let i = 0; i < localStorage.length; i++) {
                    const key = localStorage.key(i);
                    if (key && key.startsWith(CACHE_PREFIX)) {
                        keysToRemove.push(key);
                    }
                }
                keysToRemove.forEach(function(k) { localStorage.removeItem(k); });
                return keysToRemove.length;
            } catch (e) {
                return 0;
            }
        },

        /**
         * Get cache info/stats
         * @returns {object} { entries: number, keys: string[] }
         */
        getInfo: function() {
            const keys = [];
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                if (key && key.startsWith(CACHE_PREFIX)) {
                    keys.push(key.replace(CACHE_PREFIX, ''));
                }
            }
            return { entries: keys.length, keys: keys };
        }
    };

    // Expose globally
    window.PfCache = Cache;

})();