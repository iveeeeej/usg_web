(function () {
    const apiBaseUrl = String(
        (window.USG_CONFIG && window.USG_CONFIG.API_BASE_URL) || ""
    ).replace(/\/+$/, "");

    function buildUrl(path) {
        if (!path) {
            return apiBaseUrl;
        }

        if (/^https?:\/\//i.test(path)) {
            return path;
        }

        return path.charAt(0) === "/"
            ? apiBaseUrl + path
            : apiBaseUrl + "/" + path;
    }

    function getAccessToken() {
        return localStorage.getItem("access_token");
    }

    function getRefreshToken() {
        return localStorage.getItem("refresh_token");
    }

    function setTokens(tokens) {
        if (!tokens || typeof tokens !== "object") {
            return;
        }

        if (tokens.access) {
            localStorage.setItem("access_token", tokens.access);
        }

        if (tokens.refresh) {
            localStorage.setItem("refresh_token", tokens.refresh);
        }
    }

    function clearTokens() {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
    }

    function logout(redirectPath) {
        clearTokens();

        if (redirectPath) {
            window.location.href = redirectPath;
        }
    }

    function isAuthFailureStatus(status) {
        return status === 401 || status === 403;
    }

    async function parseResponseData(response) {
        if (response.status === 204) {
            return null;
        }

        const contentType = response.headers.get("content-type") || "";
        if (contentType.includes("application/json")) {
            return await response.json().catch(function () {
                return null;
            });
        }

        return await response.text().catch(function () {
            return null;
        });
    }

    async function request(path, options) {
        const requestOptions = options || {};
        const headers = {
            ...(requestOptions.headers || {})
        };

        if (requestOptions.auth) {
            const accessToken = getAccessToken();
            if (accessToken && !headers.Authorization) {
                headers.Authorization = "Bearer " + accessToken;
            }
        }

        let body = requestOptions.body;
        if (Object.prototype.hasOwnProperty.call(requestOptions, "json")) {
            headers["Content-Type"] = headers["Content-Type"] || "application/json";
            body = JSON.stringify(requestOptions.json);
        }

        const response = await fetch(buildUrl(path), {
            method: requestOptions.method || "GET",
            headers: headers,
            body: body
        });
        const data = await parseResponseData(response);
        const authRedirectPath = requestOptions.redirectOnAuthFailure;
        const authRedirected = Boolean(authRedirectPath) && isAuthFailureStatus(response.status);

        if (authRedirected) {
            logout(authRedirectPath);
        }

        return {
            response: response,
            data: data,
            ok: response.ok,
            status: response.status,
            authRedirected: authRedirected
        };
    }

    function get(path, options) {
        return request(path, {
            ...(options || {}),
            method: "GET"
        });
    }

    function post(path, options) {
        return request(path, {
            ...(options || {}),
            method: "POST"
        });
    }

    function patch(path, options) {
        return request(path, {
            ...(options || {}),
            method: "PATCH"
        });
    }

    function deleteRequest(path, options) {
        return request(path, {
            ...(options || {}),
            method: "DELETE"
        });
    }

    window.USG_API = {
        API_BASE_URL: apiBaseUrl,
        buildUrl: buildUrl,
        request: request,
        get: get,
        post: post,
        patch: patch,
        delete: deleteRequest,
        getAccessToken: getAccessToken,
        getRefreshToken: getRefreshToken,
        setTokens: setTokens,
        clearTokens: clearTokens,
        logout: logout,
        isAuthFailureStatus: isAuthFailureStatus
    };
})();
