document.addEventListener('DOMContentLoaded', function() {
    const blockObj = JSON.parse(block.obj); // Assuming 'obj' is the localized string
    const dynamicAds = blockObj.dynamic_ads; // Get the dynamic_ads array

    if (Array.isArray(dynamicAds)) {
        dynamicAds.forEach(function(obj) {
            const gamId = obj.advertisement_gam_id;
            const adType = obj.type;
            const divId = obj.div_id;
            const mobileHideOn = obj.mobile_hide_on; // Check if mobile hiding is enabled
            const mobileMaxWidth = obj.mobile_max_width; // Maximum width for mobile hiding
            const desktopHideOn = obj.desktop_hide_on; // Mobile-only ads: hide on desktop
            const desktopMinWidth = obj.desktop_min_width; // Minimum width for desktop hiding

            // Check if the ad should be hidden on mobile
            const shouldHideOnMobile =
                mobileHideOn && // Ensure mobile_hide_on is truthy
                mobileMaxWidth && // Ensure mobile_max_width is set
                !isNaN(mobileMaxWidth) && // Ensure mobile_max_width is a valid number
                window.innerWidth <= parseInt(mobileMaxWidth, 10); // Check if window width is <= mobile_max_width

            // Check if the ad should be hidden on desktop (mobile-only in-flow ads)
            const shouldHideOnDesktop =
                desktopHideOn &&
                desktopMinWidth &&
                !isNaN(desktopMinWidth) &&
                window.innerWidth >= parseInt(desktopMinWidth, 10);

            // Skip rendering the ad if it should be hidden for this viewport
            if (shouldHideOnMobile || shouldHideOnDesktop) {
                return; // Exit the forEach loop for this ad
            }

            // The gam_* size mappings are only assigned once gpt.js has loaded and
            // flushed the googletag.cmd queue (see gam-init.js). Because gpt.js is
            // loaded async, on a cold cache it may not be ready by DOMContentLoaded,
            // which is when this runs. Resolve the size mapping and define the slot
            // INSIDE cmd.push so it runs after gam-init's queued callback, keeping
            // gam_banner et al. guaranteed to exist.
            googletag.cmd = googletag.cmd || [];
            googletag.cmd.push(function() {
                let sizeMapping, initSize;
                // Use the predefined size mappings based on adType
                switch (adType) {
                    case 'banner':
                        sizeMapping = gam_banner;
                        initSize = ad_small_banner;
                        break;
                    case 'banner-medium':
                        sizeMapping = gam_banner_medium;
                        initSize = ad_small_banner;
                        break;
                    case 'square':
                        sizeMapping = gam_square;
                        initSize = ad_square;
                        break;
                    case 'square-or-rectangle':
                        sizeMapping = gam_square_or_rectangle;
                        initSize = ad_square;
                        break;
                    case 'banner-square':
                        sizeMapping = gam_square_banner;
                        initSize = ad_small_banner;
                        break;
                    default:
                        sizeMapping = null; // Fallback if the adType is unrecognized
                }

                // Ensure all necessary data is present
                if (gamId && divId && sizeMapping) {
                    const slot = googletag.defineSlot('/1003210/' + gamId, initSize, divId)
                        .defineSizeMapping(sizeMapping)
                        .addService(googletag.pubads());

                    // Set any custom key-values if provided
                    if (obj.slot_targeting) {
                        Object.keys(obj.slot_targeting).forEach(function(key) {
                            if (obj.slot_targeting[key]) {
                                slot.setTargeting(key, obj.slot_targeting[key]);
                            }
                        });
                    }

                    googletag.display(divId);

                    // Keep a handle per div so pages can refresh a single slot
                    // later (googletag.pubads().refresh([slot])) — e.g. the
                    // infinite-scroll news layout's per-article ad refresh.
                    window.PPPAdSlots = window.PPPAdSlots || {};
                    window.PPPAdSlots[divId] = slot;
                }
            });
        });
    }
});
//# sourceMappingURL=data:application/json;charset=utf8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiIiwic291cmNlcyI6WyJibG9ja3MvYWR2ZXJ0aXNlbWVudC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdET01Db250ZW50TG9hZGVkJywgZnVuY3Rpb24oKSB7XHJcbiAgICBjb25zdCBibG9ja09iaiA9IEpTT04ucGFyc2UoYmxvY2sub2JqKTsgLy8gQXNzdW1pbmcgJ29iaicgaXMgdGhlIGxvY2FsaXplZCBzdHJpbmdcclxuICAgIGNvbnN0IGR5bmFtaWNBZHMgPSBibG9ja09iai5keW5hbWljX2FkczsgLy8gR2V0IHRoZSBkeW5hbWljX2FkcyBhcnJheVxyXG5cclxuICAgIGlmIChBcnJheS5pc0FycmF5KGR5bmFtaWNBZHMpKSB7XHJcbiAgICAgICAgZHluYW1pY0Fkcy5mb3JFYWNoKGZ1bmN0aW9uKG9iaikge1xyXG4gICAgICAgICAgICBjb25zdCBnYW1JZCA9IG9iai5hZHZlcnRpc2VtZW50X2dhbV9pZDtcclxuICAgICAgICAgICAgY29uc3QgYWRUeXBlID0gb2JqLnR5cGU7XHJcbiAgICAgICAgICAgIGNvbnN0IGRpdklkID0gb2JqLmRpdl9pZDtcclxuICAgICAgICAgICAgY29uc3QgbW9iaWxlSGlkZU9uID0gb2JqLm1vYmlsZV9oaWRlX29uOyAvLyBDaGVjayBpZiBtb2JpbGUgaGlkaW5nIGlzIGVuYWJsZWRcclxuICAgICAgICAgICAgY29uc3QgbW9iaWxlTWF4V2lkdGggPSBvYmoubW9iaWxlX21heF93aWR0aDsgLy8gTWF4aW11bSB3aWR0aCBmb3IgbW9iaWxlIGhpZGluZ1xyXG4gICAgICAgICAgICBjb25zdCBkZXNrdG9wSGlkZU9uID0gb2JqLmRlc2t0b3BfaGlkZV9vbjsgLy8gTW9iaWxlLW9ubHkgYWRzOiBoaWRlIG9uIGRlc2t0b3BcclxuICAgICAgICAgICAgY29uc3QgZGVza3RvcE1pbldpZHRoID0gb2JqLmRlc2t0b3BfbWluX3dpZHRoOyAvLyBNaW5pbXVtIHdpZHRoIGZvciBkZXNrdG9wIGhpZGluZ1xyXG5cclxuICAgICAgICAgICAgLy8gQ2hlY2sgaWYgdGhlIGFkIHNob3VsZCBiZSBoaWRkZW4gb24gbW9iaWxlXHJcbiAgICAgICAgICAgIGNvbnN0IHNob3VsZEhpZGVPbk1vYmlsZSA9XHJcbiAgICAgICAgICAgICAgICBtb2JpbGVIaWRlT24gJiYgLy8gRW5zdXJlIG1vYmlsZV9oaWRlX29uIGlzIHRydXRoeVxyXG4gICAgICAgICAgICAgICAgbW9iaWxlTWF4V2lkdGggJiYgLy8gRW5zdXJlIG1vYmlsZV9tYXhfd2lkdGggaXMgc2V0XHJcbiAgICAgICAgICAgICAgICAhaXNOYU4obW9iaWxlTWF4V2lkdGgpICYmIC8vIEVuc3VyZSBtb2JpbGVfbWF4X3dpZHRoIGlzIGEgdmFsaWQgbnVtYmVyXHJcbiAgICAgICAgICAgICAgICB3aW5kb3cuaW5uZXJXaWR0aCA8PSBwYXJzZUludChtb2JpbGVNYXhXaWR0aCwgMTApOyAvLyBDaGVjayBpZiB3aW5kb3cgd2lkdGggaXMgPD0gbW9iaWxlX21heF93aWR0aFxyXG5cclxuICAgICAgICAgICAgLy8gQ2hlY2sgaWYgdGhlIGFkIHNob3VsZCBiZSBoaWRkZW4gb24gZGVza3RvcCAobW9iaWxlLW9ubHkgaW4tZmxvdyBhZHMpXHJcbiAgICAgICAgICAgIGNvbnN0IHNob3VsZEhpZGVPbkRlc2t0b3AgPVxyXG4gICAgICAgICAgICAgICAgZGVza3RvcEhpZGVPbiAmJlxyXG4gICAgICAgICAgICAgICAgZGVza3RvcE1pbldpZHRoICYmXHJcbiAgICAgICAgICAgICAgICAhaXNOYU4oZGVza3RvcE1pbldpZHRoKSAmJlxyXG4gICAgICAgICAgICAgICAgd2luZG93LmlubmVyV2lkdGggPj0gcGFyc2VJbnQoZGVza3RvcE1pbldpZHRoLCAxMCk7XHJcblxyXG4gICAgICAgICAgICAvLyBTa2lwIHJlbmRlcmluZyB0aGUgYWQgaWYgaXQgc2hvdWxkIGJlIGhpZGRlbiBmb3IgdGhpcyB2aWV3cG9ydFxyXG4gICAgICAgICAgICBpZiAoc2hvdWxkSGlkZU9uTW9iaWxlIHx8IHNob3VsZEhpZGVPbkRlc2t0b3ApIHtcclxuICAgICAgICAgICAgICAgIHJldHVybjsgLy8gRXhpdCB0aGUgZm9yRWFjaCBsb29wIGZvciB0aGlzIGFkXHJcbiAgICAgICAgICAgIH1cclxuXHJcbiAgICAgICAgICAgIC8vIFRoZSBnYW1fKiBzaXplIG1hcHBpbmdzIGFyZSBvbmx5IGFzc2lnbmVkIG9uY2UgZ3B0LmpzIGhhcyBsb2FkZWQgYW5kXHJcbiAgICAgICAgICAgIC8vIGZsdXNoZWQgdGhlIGdvb2dsZXRhZy5jbWQgcXVldWUgKHNlZSBnYW0taW5pdC5qcykuIEJlY2F1c2UgZ3B0LmpzIGlzXHJcbiAgICAgICAgICAgIC8vIGxvYWRlZCBhc3luYywgb24gYSBjb2xkIGNhY2hlIGl0IG1heSBub3QgYmUgcmVhZHkgYnkgRE9NQ29udGVudExvYWRlZCxcclxuICAgICAgICAgICAgLy8gd2hpY2ggaXMgd2hlbiB0aGlzIHJ1bnMuIFJlc29sdmUgdGhlIHNpemUgbWFwcGluZyBhbmQgZGVmaW5lIHRoZSBzbG90XHJcbiAgICAgICAgICAgIC8vIElOU0lERSBjbWQucHVzaCBzbyBpdCBydW5zIGFmdGVyIGdhbS1pbml0J3MgcXVldWVkIGNhbGxiYWNrLCBrZWVwaW5nXHJcbiAgICAgICAgICAgIC8vIGdhbV9iYW5uZXIgZXQgYWwuIGd1YXJhbnRlZWQgdG8gZXhpc3QuXHJcbiAgICAgICAgICAgIGdvb2dsZXRhZy5jbWQgPSBnb29nbGV0YWcuY21kIHx8IFtdO1xyXG4gICAgICAgICAgICBnb29nbGV0YWcuY21kLnB1c2goZnVuY3Rpb24oKSB7XHJcbiAgICAgICAgICAgICAgICBsZXQgc2l6ZU1hcHBpbmcsIGluaXRTaXplO1xyXG4gICAgICAgICAgICAgICAgLy8gVXNlIHRoZSBwcmVkZWZpbmVkIHNpemUgbWFwcGluZ3MgYmFzZWQgb24gYWRUeXBlXHJcbiAgICAgICAgICAgICAgICBzd2l0Y2ggKGFkVHlwZSkge1xyXG4gICAgICAgICAgICAgICAgICAgIGNhc2UgJ2Jhbm5lcic6XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIHNpemVNYXBwaW5nID0gZ2FtX2Jhbm5lcjtcclxuICAgICAgICAgICAgICAgICAgICAgICAgaW5pdFNpemUgPSBhZF9zbWFsbF9iYW5uZXI7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIGJyZWFrO1xyXG4gICAgICAgICAgICAgICAgICAgIGNhc2UgJ2Jhbm5lci1tZWRpdW0nOlxyXG4gICAgICAgICAgICAgICAgICAgICAgICBzaXplTWFwcGluZyA9IGdhbV9iYW5uZXJfbWVkaXVtO1xyXG4gICAgICAgICAgICAgICAgICAgICAgICBpbml0U2l6ZSA9IGFkX3NtYWxsX2Jhbm5lcjtcclxuICAgICAgICAgICAgICAgICAgICAgICAgYnJlYWs7XHJcbiAgICAgICAgICAgICAgICAgICAgY2FzZSAnc3F1YXJlJzpcclxuICAgICAgICAgICAgICAgICAgICAgICAgc2l6ZU1hcHBpbmcgPSBnYW1fc3F1YXJlO1xyXG4gICAgICAgICAgICAgICAgICAgICAgICBpbml0U2l6ZSA9IGFkX3NxdWFyZTtcclxuICAgICAgICAgICAgICAgICAgICAgICAgYnJlYWs7XHJcbiAgICAgICAgICAgICAgICAgICAgY2FzZSAnc3F1YXJlLW9yLXJlY3RhbmdsZSc6XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIHNpemVNYXBwaW5nID0gZ2FtX3NxdWFyZV9vcl9yZWN0YW5nbGU7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIGluaXRTaXplID0gYWRfc3F1YXJlO1xyXG4gICAgICAgICAgICAgICAgICAgICAgICBicmVhaztcclxuICAgICAgICAgICAgICAgICAgICBjYXNlICdiYW5uZXItc3F1YXJlJzpcclxuICAgICAgICAgICAgICAgICAgICAgICAgc2l6ZU1hcHBpbmcgPSBnYW1fc3F1YXJlX2Jhbm5lcjtcclxuICAgICAgICAgICAgICAgICAgICAgICAgaW5pdFNpemUgPSBhZF9zbWFsbF9iYW5uZXI7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIGJyZWFrO1xyXG4gICAgICAgICAgICAgICAgICAgIGRlZmF1bHQ6XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIHNpemVNYXBwaW5nID0gbnVsbDsgLy8gRmFsbGJhY2sgaWYgdGhlIGFkVHlwZSBpcyB1bnJlY29nbml6ZWRcclxuICAgICAgICAgICAgICAgIH1cclxuXHJcbiAgICAgICAgICAgICAgICAvLyBFbnN1cmUgYWxsIG5lY2Vzc2FyeSBkYXRhIGlzIHByZXNlbnRcclxuICAgICAgICAgICAgICAgIGlmIChnYW1JZCAmJiBkaXZJZCAmJiBzaXplTWFwcGluZykge1xyXG4gICAgICAgICAgICAgICAgICAgIGNvbnN0IHNsb3QgPSBnb29nbGV0YWcuZGVmaW5lU2xvdCgnLzEwMDMyMTAvJyArIGdhbUlkLCBpbml0U2l6ZSwgZGl2SWQpXHJcbiAgICAgICAgICAgICAgICAgICAgICAgIC5kZWZpbmVTaXplTWFwcGluZyhzaXplTWFwcGluZylcclxuICAgICAgICAgICAgICAgICAgICAgICAgLmFkZFNlcnZpY2UoZ29vZ2xldGFnLnB1YmFkcygpKTtcclxuXHJcbiAgICAgICAgICAgICAgICAgICAgLy8gU2V0IGFueSBjdXN0b20ga2V5LXZhbHVlcyBpZiBwcm92aWRlZFxyXG4gICAgICAgICAgICAgICAgICAgIGlmIChvYmouc2xvdF90YXJnZXRpbmcpIHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgT2JqZWN0LmtleXMob2JqLnNsb3RfdGFyZ2V0aW5nKS5mb3JFYWNoKGZ1bmN0aW9uKGtleSkge1xyXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgaWYgKG9iai5zbG90X3RhcmdldGluZ1trZXldKSB7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgc2xvdC5zZXRUYXJnZXRpbmcoa2V5LCBvYmouc2xvdF90YXJnZXRpbmdba2V5XSk7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB9XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIH0pO1xyXG4gICAgICAgICAgICAgICAgICAgIH1cclxuXHJcbiAgICAgICAgICAgICAgICAgICAgZ29vZ2xldGFnLmRpc3BsYXkoZGl2SWQpO1xyXG5cclxuICAgICAgICAgICAgICAgICAgICAvLyBLZWVwIGEgaGFuZGxlIHBlciBkaXYgc28gcGFnZXMgY2FuIHJlZnJlc2ggYSBzaW5nbGUgc2xvdFxyXG4gICAgICAgICAgICAgICAgICAgIC8vIGxhdGVyIChnb29nbGV0YWcucHViYWRzKCkucmVmcmVzaChbc2xvdF0pKSDigJQgZS5nLiB0aGVcclxuICAgICAgICAgICAgICAgICAgICAvLyBpbmZpbml0ZS1zY3JvbGwgbmV3cyBsYXlvdXQncyBwZXItYXJ0aWNsZSBhZCByZWZyZXNoLlxyXG4gICAgICAgICAgICAgICAgICAgIHdpbmRvdy5QUFBBZFNsb3RzID0gd2luZG93LlBQUEFkU2xvdHMgfHwge307XHJcbiAgICAgICAgICAgICAgICAgICAgd2luZG93LlBQUEFkU2xvdHNbZGl2SWRdID0gc2xvdDtcclxuICAgICAgICAgICAgICAgIH1cclxuICAgICAgICAgICAgfSk7XHJcbiAgICAgICAgfSk7XHJcbiAgICB9XHJcbn0pOyJdLCJmaWxlIjoiYmxvY2tzL2FkdmVydGlzZW1lbnQuanMifQ==
