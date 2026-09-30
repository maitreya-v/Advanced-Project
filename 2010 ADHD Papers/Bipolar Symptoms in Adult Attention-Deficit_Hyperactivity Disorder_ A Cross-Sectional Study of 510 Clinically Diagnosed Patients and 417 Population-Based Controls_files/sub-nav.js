document.addEventListener('DOMContentLoaded', function () {
    const backToTopBtn = document.querySelector('.sub-nav .top');
    const openMenuBtn = document.querySelector('.sub-nav .open');
    const menuItems = document.querySelector('.sub-nav .menu-items');
    const subNav = document.querySelector('.sub-nav');
    const header = document.querySelector('.site-header');
    const mainContent = document.querySelector('.main');
    const menuText = document.querySelector('.open .menu-text');

    // Links
    const menuLinks = document.querySelectorAll('.sub-nav .menu-items > :is(a, button).sub-nav-item:not(.dropdown-toggle)');

    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    const dropdownMenus = document.querySelectorAll('.dropdown-menu');
    const dropdownLinks = document.querySelectorAll('.dropdown-menu a');

    function isMobileView() {
        return window.getComputedStyle(openMenuBtn).display !== 'none';
    }

    // -------------------------------
// GTM TRACKING HELPER
// -------------------------------
    function trackSubNavClick(element, interactionType) {
        if (!window.dataLayer) {
            console.warn('GTM dataLayer not found');
            return;
        }

        const articleType = subNav.getAttribute('data-article-type') || 'Unknown';
        const articleTypeSlug = subNav.getAttribute('data-article-type-slug') || 'unknown';
        const postId = subNav.getAttribute('data-post-id') || '';
        const postTitle = subNav.getAttribute('data-post-title') || '';
        const navLabel = element.getAttribute('data-nav-label') || element.textContent.trim();
        const navType = element.getAttribute('data-nav-type') || 'unknown';
        const parentDropdown = element.getAttribute('data-parent-dropdown') || '';

        window.dataLayer.push({
            'event': 'subnav_click',
            'article_type': articleType,
            'article_type_slug': articleTypeSlug,
            'article_id': postId,
            'article_title': postTitle,
            'click_element': 'subnav',
            'click_label': navLabel,
            'click_type': navType,
            'parent_element': parentDropdown,
            'interaction_type': interactionType,
            'device_type': isMobileView() ? 'mobile' : 'desktop'
        });
    }

    // -------------------------------
    // 1) BACK TO TOP
    // -------------------------------
    backToTopBtn?.addEventListener('click', function (e) {
        e.preventDefault();
        trackSubNavClick(this, 'back_to_top');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // -------------------------------
    // 2) MOBILE OPEN/CLOSE MENU
    // -------------------------------
    openMenuBtn?.addEventListener('click', function (e) {
        e.preventDefault();
        const expanded = openMenuBtn.classList.toggle('expanded');
        menuItems.classList.toggle('expanded');
        openMenuBtn.setAttribute('aria-expanded', expanded ? 'true' : 'false');
        menuText.textContent = expanded ? 'Close menu' : 'Open menu';

        // Track menu toggle
        window.dataLayer && window.dataLayer.push({
            'event': 'subnav_menu_toggle',
            'subnav_menu_state': expanded ? 'opened' : 'closed',
            'subnav_article_type': subNav.getAttribute('data-article-type') || 'Unknown'
        });
    });

    // -------------------------------
    // 3) CLICKING NON-DROPDOWN LINKS
    // -------------------------------
    menuLinks.forEach(link => {
        link.addEventListener('click', function () {
            trackSubNavClick(this, 'link_click');

            if (isMobileView()) {
                openMenuBtn.classList.remove('expanded');
                menuItems.classList.remove('expanded');
                openMenuBtn.setAttribute('aria-expanded', 'false');
                menuText.textContent = 'Open menu';
            }
        });
    });

    // -------------------------------
    // 4) DROPDOWN TOGGLES (ARIA)
    // -------------------------------
    dropdownToggles.forEach((toggle, i) => {
        const menu = toggle.nextElementSibling;
        if (menu) {
            const menuId = `dropdown-menu-${i}`;
            menu.id = menuId;
            toggle.setAttribute('aria-controls', menuId);
            toggle.setAttribute('aria-expanded', 'false');
            menu.hidden = true;
        }

        toggle.addEventListener('click', function (e) {
            e.preventDefault();
            const expanded = this.getAttribute('aria-expanded') === 'true';
            this.setAttribute('aria-expanded', String(!expanded));
            if (menu) menu.hidden = expanded;

            // Track dropdown toggle
            trackSubNavClick(this, expanded ? 'dropdown_closed' : 'dropdown_opened');
        });
    });

    // -------------------------------
    // 5) DROPDOWN LINKS
    // -------------------------------
    dropdownLinks.forEach(item => {
        item.addEventListener('click', function () {
            trackSubNavClick(this, 'dropdown_link_click');

            const parentMenu = item.closest('.dropdown-menu');
            if (parentMenu) {
                parentMenu.hidden = true;
                const toggle = parentMenu.previousElementSibling;
                if (toggle && toggle.classList.contains('dropdown-toggle')) {
                    toggle.setAttribute('aria-expanded', 'false');
                }
            }

            if (isMobileView()) {
                openMenuBtn.classList.remove('expanded');
                menuItems.classList.remove('expanded');
                openMenuBtn.setAttribute('aria-expanded', 'false');
                menuText.textContent = 'Open menu';
            }
        });
    });

    // -------------------------------
    // 6) STICKY SUBNAV
    // -------------------------------
    function getAdminBarHeight() {
        const adminBar = document.getElementById('wpadminbar');
        return adminBar ? adminBar.getBoundingClientRect().height : 0;
    }
    const subNavOffset = subNav?.offsetTop || 0;

    window.addEventListener('scroll', function () {
        // On article pages the site header is position:static and the tab strip is the
        // persistent chrome — the subnav scrolls away naturally. Skip sticky logic entirely
        // so it neither becomes fixed nor pushes the main content down with margin-top.
        if (document.body.classList.contains('is-article-page')) return;

        const headerHeight = header ? header.getBoundingClientRect().height : 0;
        const adminBarHeight = getAdminBarHeight();

        if (window.pageYOffset > subNavOffset - headerHeight) {
            subNav.classList.add('sticky');
            subNav.style.top = `${headerHeight + adminBarHeight}px`;
            mainContent.style.marginTop = `${subNav.getBoundingClientRect().height}px`;
        } else {
            subNav.classList.remove('sticky');
            subNav.style.top = 'auto';
            mainContent.style.marginTop = '0';
        }
    });

    // -------------------------------
    // 7) LOGO SWAP
    // -------------------------------
    const logoLinkJcp = document.querySelector('.sub-nav .logo.logo-jcp');
    const logoLinkPcc = document.querySelector('.sub-nav .logo.logo-pcc');
    if (logoLinkJcp) {
        const img = document.createElement('img');
        img.src = '/wp-content/themes/psych/dist/images/logos/jcp-abv-alt.png';
        img.alt = 'JCP Logo';
        logoLinkJcp.textContent = '';
        logoLinkJcp.appendChild(img);
    }
    if (logoLinkPcc) {
        const img = document.createElement('img');
        img.src = '/wp-content/themes/psych/dist/images/logos/pcc-abv-alt.png';
        img.alt = 'PCC Logo';
        logoLinkPcc.textContent = '';
        logoLinkPcc.appendChild(img);
    }

    // -------------------------------
    // 8) CLICK OUTSIDE TO CLOSE DROPDOWNS
    // -------------------------------
    document.addEventListener('click', function (e) {
        if (!e.target.closest('.dropdown')) {
            dropdownToggles.forEach(toggle => {
                toggle.setAttribute('aria-expanded', 'false');
            });
            dropdownMenus.forEach(menu => {
                menu.hidden = true;
            });
        }
    });

    // -------------------------------
    // 9) ESC KEY TO CLOSE DROPDOWNS
    // -------------------------------
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            dropdownToggles.forEach(toggle => {
                toggle.setAttribute('aria-expanded', 'false');
            });
            dropdownMenus.forEach(menu => {
                menu.hidden = true;
            });
        }
    });
});
//# sourceMappingURL=data:application/json;charset=utf8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiIiwic291cmNlcyI6WyJibG9ja3Mvc3ViLW5hdi5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdET01Db250ZW50TG9hZGVkJywgZnVuY3Rpb24gKCkge1xyXG4gICAgY29uc3QgYmFja1RvVG9wQnRuID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignLnN1Yi1uYXYgLnRvcCcpO1xyXG4gICAgY29uc3Qgb3Blbk1lbnVCdG4gPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcuc3ViLW5hdiAub3BlbicpO1xyXG4gICAgY29uc3QgbWVudUl0ZW1zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignLnN1Yi1uYXYgLm1lbnUtaXRlbXMnKTtcclxuICAgIGNvbnN0IHN1Yk5hdiA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJy5zdWItbmF2Jyk7XHJcbiAgICBjb25zdCBoZWFkZXIgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcuc2l0ZS1oZWFkZXInKTtcclxuICAgIGNvbnN0IG1haW5Db250ZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignLm1haW4nKTtcclxuICAgIGNvbnN0IG1lbnVUZXh0ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignLm9wZW4gLm1lbnUtdGV4dCcpO1xyXG5cclxuICAgIC8vIExpbmtzXHJcbiAgICBjb25zdCBtZW51TGlua3MgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCcuc3ViLW5hdiAubWVudS1pdGVtcyA+IDppcyhhLCBidXR0b24pLnN1Yi1uYXYtaXRlbTpub3QoLmRyb3Bkb3duLXRvZ2dsZSknKTtcclxuXHJcbiAgICBjb25zdCBkcm9wZG93blRvZ2dsZXMgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCcuZHJvcGRvd24tdG9nZ2xlJyk7XHJcbiAgICBjb25zdCBkcm9wZG93bk1lbnVzID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbCgnLmRyb3Bkb3duLW1lbnUnKTtcclxuICAgIGNvbnN0IGRyb3Bkb3duTGlua3MgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCcuZHJvcGRvd24tbWVudSBhJyk7XHJcblxyXG4gICAgZnVuY3Rpb24gaXNNb2JpbGVWaWV3KCkge1xyXG4gICAgICAgIHJldHVybiB3aW5kb3cuZ2V0Q29tcHV0ZWRTdHlsZShvcGVuTWVudUJ0bikuZGlzcGxheSAhPT0gJ25vbmUnO1xyXG4gICAgfVxyXG5cclxuICAgIC8vIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cclxuLy8gR1RNIFRSQUNLSU5HIEhFTFBFUlxyXG4vLyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXHJcbiAgICBmdW5jdGlvbiB0cmFja1N1Yk5hdkNsaWNrKGVsZW1lbnQsIGludGVyYWN0aW9uVHlwZSkge1xyXG4gICAgICAgIGlmICghd2luZG93LmRhdGFMYXllcikge1xyXG4gICAgICAgICAgICBjb25zb2xlLndhcm4oJ0dUTSBkYXRhTGF5ZXIgbm90IGZvdW5kJyk7XHJcbiAgICAgICAgICAgIHJldHVybjtcclxuICAgICAgICB9XHJcblxyXG4gICAgICAgIGNvbnN0IGFydGljbGVUeXBlID0gc3ViTmF2LmdldEF0dHJpYnV0ZSgnZGF0YS1hcnRpY2xlLXR5cGUnKSB8fCAnVW5rbm93bic7XHJcbiAgICAgICAgY29uc3QgYXJ0aWNsZVR5cGVTbHVnID0gc3ViTmF2LmdldEF0dHJpYnV0ZSgnZGF0YS1hcnRpY2xlLXR5cGUtc2x1ZycpIHx8ICd1bmtub3duJztcclxuICAgICAgICBjb25zdCBwb3N0SWQgPSBzdWJOYXYuZ2V0QXR0cmlidXRlKCdkYXRhLXBvc3QtaWQnKSB8fCAnJztcclxuICAgICAgICBjb25zdCBwb3N0VGl0bGUgPSBzdWJOYXYuZ2V0QXR0cmlidXRlKCdkYXRhLXBvc3QtdGl0bGUnKSB8fCAnJztcclxuICAgICAgICBjb25zdCBuYXZMYWJlbCA9IGVsZW1lbnQuZ2V0QXR0cmlidXRlKCdkYXRhLW5hdi1sYWJlbCcpIHx8IGVsZW1lbnQudGV4dENvbnRlbnQudHJpbSgpO1xyXG4gICAgICAgIGNvbnN0IG5hdlR5cGUgPSBlbGVtZW50LmdldEF0dHJpYnV0ZSgnZGF0YS1uYXYtdHlwZScpIHx8ICd1bmtub3duJztcclxuICAgICAgICBjb25zdCBwYXJlbnREcm9wZG93biA9IGVsZW1lbnQuZ2V0QXR0cmlidXRlKCdkYXRhLXBhcmVudC1kcm9wZG93bicpIHx8ICcnO1xyXG5cclxuICAgICAgICB3aW5kb3cuZGF0YUxheWVyLnB1c2goe1xyXG4gICAgICAgICAgICAnZXZlbnQnOiAnc3VibmF2X2NsaWNrJyxcclxuICAgICAgICAgICAgJ2FydGljbGVfdHlwZSc6IGFydGljbGVUeXBlLFxyXG4gICAgICAgICAgICAnYXJ0aWNsZV90eXBlX3NsdWcnOiBhcnRpY2xlVHlwZVNsdWcsXHJcbiAgICAgICAgICAgICdhcnRpY2xlX2lkJzogcG9zdElkLFxyXG4gICAgICAgICAgICAnYXJ0aWNsZV90aXRsZSc6IHBvc3RUaXRsZSxcclxuICAgICAgICAgICAgJ2NsaWNrX2VsZW1lbnQnOiAnc3VibmF2JyxcclxuICAgICAgICAgICAgJ2NsaWNrX2xhYmVsJzogbmF2TGFiZWwsXHJcbiAgICAgICAgICAgICdjbGlja190eXBlJzogbmF2VHlwZSxcclxuICAgICAgICAgICAgJ3BhcmVudF9lbGVtZW50JzogcGFyZW50RHJvcGRvd24sXHJcbiAgICAgICAgICAgICdpbnRlcmFjdGlvbl90eXBlJzogaW50ZXJhY3Rpb25UeXBlLFxyXG4gICAgICAgICAgICAnZGV2aWNlX3R5cGUnOiBpc01vYmlsZVZpZXcoKSA/ICdtb2JpbGUnIDogJ2Rlc2t0b3AnXHJcbiAgICAgICAgfSk7XHJcbiAgICB9XHJcblxyXG4gICAgLy8gLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxyXG4gICAgLy8gMSkgQkFDSyBUTyBUT1BcclxuICAgIC8vIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cclxuICAgIGJhY2tUb1RvcEJ0bj8uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCBmdW5jdGlvbiAoZSkge1xyXG4gICAgICAgIGUucHJldmVudERlZmF1bHQoKTtcclxuICAgICAgICB0cmFja1N1Yk5hdkNsaWNrKHRoaXMsICdiYWNrX3RvX3RvcCcpO1xyXG4gICAgICAgIHdpbmRvdy5zY3JvbGxUbyh7IHRvcDogMCwgYmVoYXZpb3I6ICdzbW9vdGgnIH0pO1xyXG4gICAgfSk7XHJcblxyXG4gICAgLy8gLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxyXG4gICAgLy8gMikgTU9CSUxFIE9QRU4vQ0xPU0UgTUVOVVxyXG4gICAgLy8gLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxyXG4gICAgb3Blbk1lbnVCdG4/LmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgZnVuY3Rpb24gKGUpIHtcclxuICAgICAgICBlLnByZXZlbnREZWZhdWx0KCk7XHJcbiAgICAgICAgY29uc3QgZXhwYW5kZWQgPSBvcGVuTWVudUJ0bi5jbGFzc0xpc3QudG9nZ2xlKCdleHBhbmRlZCcpO1xyXG4gICAgICAgIG1lbnVJdGVtcy5jbGFzc0xpc3QudG9nZ2xlKCdleHBhbmRlZCcpO1xyXG4gICAgICAgIG9wZW5NZW51QnRuLnNldEF0dHJpYnV0ZSgnYXJpYS1leHBhbmRlZCcsIGV4cGFuZGVkID8gJ3RydWUnIDogJ2ZhbHNlJyk7XHJcbiAgICAgICAgbWVudVRleHQudGV4dENvbnRlbnQgPSBleHBhbmRlZCA/ICdDbG9zZSBtZW51JyA6ICdPcGVuIG1lbnUnO1xyXG5cclxuICAgICAgICAvLyBUcmFjayBtZW51IHRvZ2dsZVxyXG4gICAgICAgIHdpbmRvdy5kYXRhTGF5ZXIgJiYgd2luZG93LmRhdGFMYXllci5wdXNoKHtcclxuICAgICAgICAgICAgJ2V2ZW50JzogJ3N1Ym5hdl9tZW51X3RvZ2dsZScsXHJcbiAgICAgICAgICAgICdzdWJuYXZfbWVudV9zdGF0ZSc6IGV4cGFuZGVkID8gJ29wZW5lZCcgOiAnY2xvc2VkJyxcclxuICAgICAgICAgICAgJ3N1Ym5hdl9hcnRpY2xlX3R5cGUnOiBzdWJOYXYuZ2V0QXR0cmlidXRlKCdkYXRhLWFydGljbGUtdHlwZScpIHx8ICdVbmtub3duJ1xyXG4gICAgICAgIH0pO1xyXG4gICAgfSk7XHJcblxyXG4gICAgLy8gLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxyXG4gICAgLy8gMykgQ0xJQ0tJTkcgTk9OLURST1BET1dOIExJTktTXHJcbiAgICAvLyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXHJcbiAgICBtZW51TGlua3MuZm9yRWFjaChsaW5rID0+IHtcclxuICAgICAgICBsaW5rLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgZnVuY3Rpb24gKCkge1xyXG4gICAgICAgICAgICB0cmFja1N1Yk5hdkNsaWNrKHRoaXMsICdsaW5rX2NsaWNrJyk7XHJcblxyXG4gICAgICAgICAgICBpZiAoaXNNb2JpbGVWaWV3KCkpIHtcclxuICAgICAgICAgICAgICAgIG9wZW5NZW51QnRuLmNsYXNzTGlzdC5yZW1vdmUoJ2V4cGFuZGVkJyk7XHJcbiAgICAgICAgICAgICAgICBtZW51SXRlbXMuY2xhc3NMaXN0LnJlbW92ZSgnZXhwYW5kZWQnKTtcclxuICAgICAgICAgICAgICAgIG9wZW5NZW51QnRuLnNldEF0dHJpYnV0ZSgnYXJpYS1leHBhbmRlZCcsICdmYWxzZScpO1xyXG4gICAgICAgICAgICAgICAgbWVudVRleHQudGV4dENvbnRlbnQgPSAnT3BlbiBtZW51JztcclxuICAgICAgICAgICAgfVxyXG4gICAgICAgIH0pO1xyXG4gICAgfSk7XHJcblxyXG4gICAgLy8gLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxyXG4gICAgLy8gNCkgRFJPUERPV04gVE9HR0xFUyAoQVJJQSlcclxuICAgIC8vIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cclxuICAgIGRyb3Bkb3duVG9nZ2xlcy5mb3JFYWNoKCh0b2dnbGUsIGkpID0+IHtcclxuICAgICAgICBjb25zdCBtZW51ID0gdG9nZ2xlLm5leHRFbGVtZW50U2libGluZztcclxuICAgICAgICBpZiAobWVudSkge1xyXG4gICAgICAgICAgICBjb25zdCBtZW51SWQgPSBgZHJvcGRvd24tbWVudS0ke2l9YDtcclxuICAgICAgICAgICAgbWVudS5pZCA9IG1lbnVJZDtcclxuICAgICAgICAgICAgdG9nZ2xlLnNldEF0dHJpYnV0ZSgnYXJpYS1jb250cm9scycsIG1lbnVJZCk7XHJcbiAgICAgICAgICAgIHRvZ2dsZS5zZXRBdHRyaWJ1dGUoJ2FyaWEtZXhwYW5kZWQnLCAnZmFsc2UnKTtcclxuICAgICAgICAgICAgbWVudS5oaWRkZW4gPSB0cnVlO1xyXG4gICAgICAgIH1cclxuXHJcbiAgICAgICAgdG9nZ2xlLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgZnVuY3Rpb24gKGUpIHtcclxuICAgICAgICAgICAgZS5wcmV2ZW50RGVmYXVsdCgpO1xyXG4gICAgICAgICAgICBjb25zdCBleHBhbmRlZCA9IHRoaXMuZ2V0QXR0cmlidXRlKCdhcmlhLWV4cGFuZGVkJykgPT09ICd0cnVlJztcclxuICAgICAgICAgICAgdGhpcy5zZXRBdHRyaWJ1dGUoJ2FyaWEtZXhwYW5kZWQnLCBTdHJpbmcoIWV4cGFuZGVkKSk7XHJcbiAgICAgICAgICAgIGlmIChtZW51KSBtZW51LmhpZGRlbiA9IGV4cGFuZGVkO1xyXG5cclxuICAgICAgICAgICAgLy8gVHJhY2sgZHJvcGRvd24gdG9nZ2xlXHJcbiAgICAgICAgICAgIHRyYWNrU3ViTmF2Q2xpY2sodGhpcywgZXhwYW5kZWQgPyAnZHJvcGRvd25fY2xvc2VkJyA6ICdkcm9wZG93bl9vcGVuZWQnKTtcclxuICAgICAgICB9KTtcclxuICAgIH0pO1xyXG5cclxuICAgIC8vIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cclxuICAgIC8vIDUpIERST1BET1dOIExJTktTXHJcbiAgICAvLyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXHJcbiAgICBkcm9wZG93bkxpbmtzLmZvckVhY2goaXRlbSA9PiB7XHJcbiAgICAgICAgaXRlbS5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIGZ1bmN0aW9uICgpIHtcclxuICAgICAgICAgICAgdHJhY2tTdWJOYXZDbGljayh0aGlzLCAnZHJvcGRvd25fbGlua19jbGljaycpO1xyXG5cclxuICAgICAgICAgICAgY29uc3QgcGFyZW50TWVudSA9IGl0ZW0uY2xvc2VzdCgnLmRyb3Bkb3duLW1lbnUnKTtcclxuICAgICAgICAgICAgaWYgKHBhcmVudE1lbnUpIHtcclxuICAgICAgICAgICAgICAgIHBhcmVudE1lbnUuaGlkZGVuID0gdHJ1ZTtcclxuICAgICAgICAgICAgICAgIGNvbnN0IHRvZ2dsZSA9IHBhcmVudE1lbnUucHJldmlvdXNFbGVtZW50U2libGluZztcclxuICAgICAgICAgICAgICAgIGlmICh0b2dnbGUgJiYgdG9nZ2xlLmNsYXNzTGlzdC5jb250YWlucygnZHJvcGRvd24tdG9nZ2xlJykpIHtcclxuICAgICAgICAgICAgICAgICAgICB0b2dnbGUuc2V0QXR0cmlidXRlKCdhcmlhLWV4cGFuZGVkJywgJ2ZhbHNlJyk7XHJcbiAgICAgICAgICAgICAgICB9XHJcbiAgICAgICAgICAgIH1cclxuXHJcbiAgICAgICAgICAgIGlmIChpc01vYmlsZVZpZXcoKSkge1xyXG4gICAgICAgICAgICAgICAgb3Blbk1lbnVCdG4uY2xhc3NMaXN0LnJlbW92ZSgnZXhwYW5kZWQnKTtcclxuICAgICAgICAgICAgICAgIG1lbnVJdGVtcy5jbGFzc0xpc3QucmVtb3ZlKCdleHBhbmRlZCcpO1xyXG4gICAgICAgICAgICAgICAgb3Blbk1lbnVCdG4uc2V0QXR0cmlidXRlKCdhcmlhLWV4cGFuZGVkJywgJ2ZhbHNlJyk7XHJcbiAgICAgICAgICAgICAgICBtZW51VGV4dC50ZXh0Q29udGVudCA9ICdPcGVuIG1lbnUnO1xyXG4gICAgICAgICAgICB9XHJcbiAgICAgICAgfSk7XHJcbiAgICB9KTtcclxuXHJcbiAgICAvLyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXHJcbiAgICAvLyA2KSBTVElDS1kgU1VCTkFWXHJcbiAgICAvLyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXHJcbiAgICBmdW5jdGlvbiBnZXRBZG1pbkJhckhlaWdodCgpIHtcclxuICAgICAgICBjb25zdCBhZG1pbkJhciA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCd3cGFkbWluYmFyJyk7XHJcbiAgICAgICAgcmV0dXJuIGFkbWluQmFyID8gYWRtaW5CYXIuZ2V0Qm91bmRpbmdDbGllbnRSZWN0KCkuaGVpZ2h0IDogMDtcclxuICAgIH1cclxuICAgIGNvbnN0IHN1Yk5hdk9mZnNldCA9IHN1Yk5hdj8ub2Zmc2V0VG9wIHx8IDA7XHJcblxyXG4gICAgd2luZG93LmFkZEV2ZW50TGlzdGVuZXIoJ3Njcm9sbCcsIGZ1bmN0aW9uICgpIHtcclxuICAgICAgICAvLyBPbiBhcnRpY2xlIHBhZ2VzIHRoZSBzaXRlIGhlYWRlciBpcyBwb3NpdGlvbjpzdGF0aWMgYW5kIHRoZSB0YWIgc3RyaXAgaXMgdGhlXHJcbiAgICAgICAgLy8gcGVyc2lzdGVudCBjaHJvbWUg4oCUIHRoZSBzdWJuYXYgc2Nyb2xscyBhd2F5IG5hdHVyYWxseS4gU2tpcCBzdGlja3kgbG9naWMgZW50aXJlbHlcclxuICAgICAgICAvLyBzbyBpdCBuZWl0aGVyIGJlY29tZXMgZml4ZWQgbm9yIHB1c2hlcyB0aGUgbWFpbiBjb250ZW50IGRvd24gd2l0aCBtYXJnaW4tdG9wLlxyXG4gICAgICAgIGlmIChkb2N1bWVudC5ib2R5LmNsYXNzTGlzdC5jb250YWlucygnaXMtYXJ0aWNsZS1wYWdlJykpIHJldHVybjtcclxuXHJcbiAgICAgICAgY29uc3QgaGVhZGVySGVpZ2h0ID0gaGVhZGVyID8gaGVhZGVyLmdldEJvdW5kaW5nQ2xpZW50UmVjdCgpLmhlaWdodCA6IDA7XHJcbiAgICAgICAgY29uc3QgYWRtaW5CYXJIZWlnaHQgPSBnZXRBZG1pbkJhckhlaWdodCgpO1xyXG5cclxuICAgICAgICBpZiAod2luZG93LnBhZ2VZT2Zmc2V0ID4gc3ViTmF2T2Zmc2V0IC0gaGVhZGVySGVpZ2h0KSB7XHJcbiAgICAgICAgICAgIHN1Yk5hdi5jbGFzc0xpc3QuYWRkKCdzdGlja3knKTtcclxuICAgICAgICAgICAgc3ViTmF2LnN0eWxlLnRvcCA9IGAke2hlYWRlckhlaWdodCArIGFkbWluQmFySGVpZ2h0fXB4YDtcclxuICAgICAgICAgICAgbWFpbkNvbnRlbnQuc3R5bGUubWFyZ2luVG9wID0gYCR7c3ViTmF2LmdldEJvdW5kaW5nQ2xpZW50UmVjdCgpLmhlaWdodH1weGA7XHJcbiAgICAgICAgfSBlbHNlIHtcclxuICAgICAgICAgICAgc3ViTmF2LmNsYXNzTGlzdC5yZW1vdmUoJ3N0aWNreScpO1xyXG4gICAgICAgICAgICBzdWJOYXYuc3R5bGUudG9wID0gJ2F1dG8nO1xyXG4gICAgICAgICAgICBtYWluQ29udGVudC5zdHlsZS5tYXJnaW5Ub3AgPSAnMCc7XHJcbiAgICAgICAgfVxyXG4gICAgfSk7XHJcblxyXG4gICAgLy8gLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxyXG4gICAgLy8gNykgTE9HTyBTV0FQXHJcbiAgICAvLyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXHJcbiAgICBjb25zdCBsb2dvTGlua0pjcCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJy5zdWItbmF2IC5sb2dvLmxvZ28tamNwJyk7XHJcbiAgICBjb25zdCBsb2dvTGlua1BjYyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJy5zdWItbmF2IC5sb2dvLmxvZ28tcGNjJyk7XHJcbiAgICBpZiAobG9nb0xpbmtKY3ApIHtcclxuICAgICAgICBjb25zdCBpbWcgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdpbWcnKTtcclxuICAgICAgICBpbWcuc3JjID0gJy93cC1jb250ZW50L3RoZW1lcy9wc3ljaC9kaXN0L2ltYWdlcy9sb2dvcy9qY3AtYWJ2LWFsdC5wbmcnO1xyXG4gICAgICAgIGltZy5hbHQgPSAnSkNQIExvZ28nO1xyXG4gICAgICAgIGxvZ29MaW5rSmNwLnRleHRDb250ZW50ID0gJyc7XHJcbiAgICAgICAgbG9nb0xpbmtKY3AuYXBwZW5kQ2hpbGQoaW1nKTtcclxuICAgIH1cclxuICAgIGlmIChsb2dvTGlua1BjYykge1xyXG4gICAgICAgIGNvbnN0IGltZyA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2ltZycpO1xyXG4gICAgICAgIGltZy5zcmMgPSAnL3dwLWNvbnRlbnQvdGhlbWVzL3BzeWNoL2Rpc3QvaW1hZ2VzL2xvZ29zL3BjYy1hYnYtYWx0LnBuZyc7XHJcbiAgICAgICAgaW1nLmFsdCA9ICdQQ0MgTG9nbyc7XHJcbiAgICAgICAgbG9nb0xpbmtQY2MudGV4dENvbnRlbnQgPSAnJztcclxuICAgICAgICBsb2dvTGlua1BjYy5hcHBlbmRDaGlsZChpbWcpO1xyXG4gICAgfVxyXG5cclxuICAgIC8vIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cclxuICAgIC8vIDgpIENMSUNLIE9VVFNJREUgVE8gQ0xPU0UgRFJPUERPV05TXHJcbiAgICAvLyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXHJcbiAgICBkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIGZ1bmN0aW9uIChlKSB7XHJcbiAgICAgICAgaWYgKCFlLnRhcmdldC5jbG9zZXN0KCcuZHJvcGRvd24nKSkge1xyXG4gICAgICAgICAgICBkcm9wZG93blRvZ2dsZXMuZm9yRWFjaCh0b2dnbGUgPT4ge1xyXG4gICAgICAgICAgICAgICAgdG9nZ2xlLnNldEF0dHJpYnV0ZSgnYXJpYS1leHBhbmRlZCcsICdmYWxzZScpO1xyXG4gICAgICAgICAgICB9KTtcclxuICAgICAgICAgICAgZHJvcGRvd25NZW51cy5mb3JFYWNoKG1lbnUgPT4ge1xyXG4gICAgICAgICAgICAgICAgbWVudS5oaWRkZW4gPSB0cnVlO1xyXG4gICAgICAgICAgICB9KTtcclxuICAgICAgICB9XHJcbiAgICB9KTtcclxuXHJcbiAgICAvLyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXHJcbiAgICAvLyA5KSBFU0MgS0VZIFRPIENMT1NFIERST1BET1dOU1xyXG4gICAgLy8gLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxyXG4gICAgZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcigna2V5ZG93bicsIGZ1bmN0aW9uIChlKSB7XHJcbiAgICAgICAgaWYgKGUua2V5ID09PSAnRXNjYXBlJykge1xyXG4gICAgICAgICAgICBkcm9wZG93blRvZ2dsZXMuZm9yRWFjaCh0b2dnbGUgPT4ge1xyXG4gICAgICAgICAgICAgICAgdG9nZ2xlLnNldEF0dHJpYnV0ZSgnYXJpYS1leHBhbmRlZCcsICdmYWxzZScpO1xyXG4gICAgICAgICAgICB9KTtcclxuICAgICAgICAgICAgZHJvcGRvd25NZW51cy5mb3JFYWNoKG1lbnUgPT4ge1xyXG4gICAgICAgICAgICAgICAgbWVudS5oaWRkZW4gPSB0cnVlO1xyXG4gICAgICAgICAgICB9KTtcclxuICAgICAgICB9XHJcbiAgICB9KTtcclxufSk7Il0sImZpbGUiOiJibG9ja3Mvc3ViLW5hdi5qcyJ9
