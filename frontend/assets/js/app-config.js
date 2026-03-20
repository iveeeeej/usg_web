(function () {
    const existingConfig = window.USG_CONFIG || {};
    // Change this in one place for deployment, or define window.USG_CONFIG first.
    const configuredBaseUrl = existingConfig.API_BASE_URL || "http://127.0.0.1:8000";

    window.USG_CONFIG = {
        ...existingConfig,
        API_BASE_URL: configuredBaseUrl.replace(/\/+$/, "")
    };
})();
