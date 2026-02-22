document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const closeSidebar = document.getElementById('closeSidebar');

    // Toggle sidebar on menu button click
    menuToggle.addEventListener('click', function () {
        sidebar.classList.add('active');
        sidebarOverlay.classList.add('active');
    });

    // Close sidebar methods:

    // 1. Close button click
    closeSidebar.addEventListener('click', function () {
        sidebar.classList.remove('active');
        sidebarOverlay.classList.remove('active');
    });

    // 2. Overlay click
    sidebarOverlay.addEventListener('click', function () {
        sidebar.classList.remove('active');
        sidebarOverlay.classList.remove('active');
    });

    // 3. Auto-close when clicking menu links
    document.querySelectorAll('.sidebar .nav-link').forEach(link => {
        link.addEventListener('click', function () {
            if (window.innerWidth <= 992) {
                sidebar.classList.remove('active');
                sidebarOverlay.classList.remove('active');
            }
        });
    });

    // 4. Window resize (close on desktop)
    window.addEventListener('resize', function () {
        if (window.innerWidth > 992) {
            sidebar.classList.remove('active');
            sidebarOverlay.classList.remove('active');
        }
    });
});

// ── Collapsible Sidebar Sections with localStorage ──
(function () {
    const STORAGE_KEY = 'sidebar-sections';

    // Load saved state (default: all expanded)
    function loadState() {
        try {
            return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
        } catch (e) {
            return {};
        }
    }

    function saveState(state) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    }

    const state = loadState();
    const sections = document.querySelectorAll('.sidebar-section[data-section]');

    sections.forEach(function (section) {
        const key = section.getAttribute('data-section');
        const title = section.querySelector('.sidebar-section-title.collapsible');
        if (!title) return;

        // Apply saved state (collapsed = true means collapsed)
        if (state[key] === true) {
            section.classList.add('collapsed');
        }

        // Toggle on click
        title.addEventListener('click', function () {
            section.classList.toggle('collapsed');
            const currentState = loadState();
            currentState[key] = section.classList.contains('collapsed');
            saveState(currentState);
        });
    });
})();

// ── User Avatar Dropdown ──
(function () {
    const wrapper = document.getElementById('userAvatarWrapper');
    const dropdown = document.getElementById('userDropdown');

    if (!wrapper) return;

    wrapper.addEventListener('click', function (e) {
        e.stopPropagation();
        dropdown.classList.toggle('show');
    });

    document.addEventListener('click', function () {
        dropdown.classList.remove('show');
    });
})();