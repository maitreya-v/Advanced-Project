window.googletag = window.googletag || { cmd: [] };

// Ad size definitions
var ad_small_banner    = [320, 50];
var ad_medium_banner   = [728, 90];
var ad_large_banner    = [970, 90];
var ad_square          = [300, 250];
var ad_rectangle       = [300, 600];
var small              = [1, 1];

// Function to detect mobile devices (below 767px)
function isMobileDevice() {
    return window.innerWidth < 767;
}

googletag.cmd.push(function () {
    // Size mappings
    gam_banner = googletag.sizeMapping()
        .addSize([1, 1], [ad_small_banner, small])
        .addSize([767, 1], [ad_medium_banner, small])
        .addSize([1056, 1], [ad_medium_banner, ad_large_banner, small])
        .build();

    gam_banner_medium = googletag.sizeMapping()
        .addSize([1, 1], [ad_small_banner, small])
        .addSize([767, 1], [ad_medium_banner, small])
        .build();

    gam_square = googletag.sizeMapping()
        .addSize([1, 1], [ad_square, small])
        .build();

    gam_square_or_rectangle = googletag.sizeMapping()
        .addSize([1, 1], [ad_square, small])
        .addSize([767, 1], [ad_square, ad_rectangle])
        .build();

    gam_square_banner = googletag.sizeMapping()
        .addSize([1, 1], [ad_small_banner, small])
        .addSize([767, 1], [ad_medium_banner, small])
        .addSize([1200, 1], [ad_square, small])
        .build();

    // Ad-free footer tracking: one banner size per device so PulsePoint can
    // split mobile vs desktop reporting. 320x50 below 767px wide, 728x90 at or
    // above it. Deliberately no 1x1 or 970x90, so only these two ever serve and
    // each reports on exactly one device class.
    gam_footer_tracking = googletag.sizeMapping()
        .addSize([1, 1], [[320, 50]])
        .addSize([767, 1], [[728, 90]])
        .build();

    // Define other ad slots (e.g., static-footer) that should still render on mobile.
    // Skipped when the page has no footer unit: defining a slot whose container was
    // suppressed still sends the ad request, so an ad-free page was asking GAM for
    // inventory it had no intention of showing.
    // String compare on purpose: wp_localize_script stringifies, so this arrives
    // as "0", and a strict !== 0 would have been true on every page.
    if (typeof gam === 'undefined' || String(gam.static_footer) !== '0') {
        googletag.defineSlot('/1003210/static-footer', [[320, 50]], 'static-footer')
            .defineSizeMapping(gam_banner)
            .setTargeting("position", "static-footer")
            .addService(googletag.pubads());
    } else {
        // Ad-free pages still request this unit, for tracking only, into a
        // container that occupies no space (see footer.php). The impression is
        // how we signal PulsePoint, so this slot must fill.
        //
        // Per ad ops, the request carries the standard footer banner sizes, one
        // per device (320x50 mobile, 728x90 desktop, via gam_footer_tracking):
        // the PulsePoint tracking line item's creatives are standard sizes, so a
        // 1x1-only request could never fill it (getResponseInformation was null),
        // and the mobile/desktop split is separated in PulsePoint reporting. The
        // container stays 1px/hidden, so whatever serves is an invisible tracking
        // impression, which is the whole point on an ad-free page.
        googletag.defineSlot('/1003210/static-footer', [[320, 50], [728, 90]], 'static-footer-tracking')
            .defineSizeMapping(gam_footer_tracking)
            .setTargeting("position", "static-footer")
            .addService(googletag.pubads());
    }

    // Check if page_targeting exists and apply it to the page-level targeting
    if (gam.page_targeting) {
        var targeting = JSON.parse(gam.page_targeting);
        for (var key in targeting) {
            if (targeting.hasOwnProperty(key)) {
                googletag.pubads().setTargeting(key, targeting[key].toString());
            }
        }
    }

    // Enable lazy loading and other services.
    //
    // Lazy loading only earns its keep where there are real ads to defer. An
    // ad-free page has exactly one slot, the invisible 1x1 tracking pixel, and
    // deferring that is what stopped it fetching at all: Publisher Console
    // reported the slot defined and displayed with "Ad unit did not fetch".
    // There is nothing to defer here, so it stays off and the slot fetches on
    // load wherever it happens to sit in the document.
    if (typeof gam === 'undefined' || String(gam.static_footer) !== '0') {
        googletag.pubads()
            .enableLazyLoad({
                fetchMarginPercent: 50,
                renderMarginPercent: 10,
                mobileScaling: 1.0
            });
    }

    googletag.enableServices();
});

// Apply the async IQVIA HCP identity (window.iqviaTargeting.iqvia_type, set by
// the aim-tag signal callback in header.php) as page-level targeting as soon as
// it resolves. This is intentionally ADDITIVE: the enableServices()/display()
// flow above is left untouched, because deferring enableServices() until
// identity resolves blanks any slot whose display() runs first (that broke ad
// serving in a prior attempt). Page-level targeting applies to every ad request
// made after this point; with lazy load on, the large majority of slots fetch
// later and pick it up. We deliberately do NOT refresh() already-fetched slots,
// which would double-count impressions in GAM reporting.
function applyIqviaTargeting() {
    if (window.iqviaTargeting && window.iqviaTargeting.iqvia_type) {
        googletag.cmd.push(function () {
            googletag.pubads().setTargeting('iqvia_type', String(window.iqviaTargeting.iqvia_type));
        });
    }
}

if (window.iqviaTargetingReady) {
    // Identity resolved before this script ran.
    applyIqviaTargeting();
} else {
    // Otherwise apply it the moment the identity lookup completes.
    window.addEventListener('iqviaTargetingReady', applyIqviaTargeting, { once: true });
}

document.addEventListener('DOMContentLoaded', function() {
    // Function to refresh ads
    function refreshAds() {
        googletag.pubads().refresh();
    }

    // Listen for window resize and refresh ads
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            refreshAds();
        }, 250); // Refresh ads after resize is complete (debounce to prevent excessive refreshes)
    });

    const footerAd = document.getElementById('static-footer');
    const dismissBtn = document.querySelector('#footer-ad-container .ad-dismiss');

    if (dismissBtn) {
        dismissBtn.style.display = 'block';
        if (!dismissBtn.dataset.bound) {
            dismissBtn.addEventListener('click', () => {
                const container = document.getElementById('footer-ad-container');
                container?.remove();
            });
            dismissBtn.dataset.bound = 'true';
        }
    }

});
//# sourceMappingURL=data:application/json;charset=utf8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiIiwic291cmNlcyI6WyJnYW0taW5pdC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJ3aW5kb3cuZ29vZ2xldGFnID0gd2luZG93Lmdvb2dsZXRhZyB8fCB7IGNtZDogW10gfTtcblxuLy8gQWQgc2l6ZSBkZWZpbml0aW9uc1xudmFyIGFkX3NtYWxsX2Jhbm5lciAgICA9IFszMjAsIDUwXTtcbnZhciBhZF9tZWRpdW1fYmFubmVyICAgPSBbNzI4LCA5MF07XG52YXIgYWRfbGFyZ2VfYmFubmVyICAgID0gWzk3MCwgOTBdO1xudmFyIGFkX3NxdWFyZSAgICAgICAgICA9IFszMDAsIDI1MF07XG52YXIgYWRfcmVjdGFuZ2xlICAgICAgID0gWzMwMCwgNjAwXTtcbnZhciBzbWFsbCAgICAgICAgICAgICAgPSBbMSwgMV07XG5cbi8vIEZ1bmN0aW9uIHRvIGRldGVjdCBtb2JpbGUgZGV2aWNlcyAoYmVsb3cgNzY3cHgpXG5mdW5jdGlvbiBpc01vYmlsZURldmljZSgpIHtcbiAgICByZXR1cm4gd2luZG93LmlubmVyV2lkdGggPCA3Njc7XG59XG5cbmdvb2dsZXRhZy5jbWQucHVzaChmdW5jdGlvbiAoKSB7XG4gICAgLy8gU2l6ZSBtYXBwaW5nc1xuICAgIGdhbV9iYW5uZXIgPSBnb29nbGV0YWcuc2l6ZU1hcHBpbmcoKVxuICAgICAgICAuYWRkU2l6ZShbMSwgMV0sIFthZF9zbWFsbF9iYW5uZXIsIHNtYWxsXSlcbiAgICAgICAgLmFkZFNpemUoWzc2NywgMV0sIFthZF9tZWRpdW1fYmFubmVyLCBzbWFsbF0pXG4gICAgICAgIC5hZGRTaXplKFsxMDU2LCAxXSwgW2FkX21lZGl1bV9iYW5uZXIsIGFkX2xhcmdlX2Jhbm5lciwgc21hbGxdKVxuICAgICAgICAuYnVpbGQoKTtcblxuICAgIGdhbV9iYW5uZXJfbWVkaXVtID0gZ29vZ2xldGFnLnNpemVNYXBwaW5nKClcbiAgICAgICAgLmFkZFNpemUoWzEsIDFdLCBbYWRfc21hbGxfYmFubmVyLCBzbWFsbF0pXG4gICAgICAgIC5hZGRTaXplKFs3NjcsIDFdLCBbYWRfbWVkaXVtX2Jhbm5lciwgc21hbGxdKVxuICAgICAgICAuYnVpbGQoKTtcblxuICAgIGdhbV9zcXVhcmUgPSBnb29nbGV0YWcuc2l6ZU1hcHBpbmcoKVxuICAgICAgICAuYWRkU2l6ZShbMSwgMV0sIFthZF9zcXVhcmUsIHNtYWxsXSlcbiAgICAgICAgLmJ1aWxkKCk7XG5cbiAgICBnYW1fc3F1YXJlX29yX3JlY3RhbmdsZSA9IGdvb2dsZXRhZy5zaXplTWFwcGluZygpXG4gICAgICAgIC5hZGRTaXplKFsxLCAxXSwgW2FkX3NxdWFyZSwgc21hbGxdKVxuICAgICAgICAuYWRkU2l6ZShbNzY3LCAxXSwgW2FkX3NxdWFyZSwgYWRfcmVjdGFuZ2xlXSlcbiAgICAgICAgLmJ1aWxkKCk7XG5cbiAgICBnYW1fc3F1YXJlX2Jhbm5lciA9IGdvb2dsZXRhZy5zaXplTWFwcGluZygpXG4gICAgICAgIC5hZGRTaXplKFsxLCAxXSwgW2FkX3NtYWxsX2Jhbm5lciwgc21hbGxdKVxuICAgICAgICAuYWRkU2l6ZShbNzY3LCAxXSwgW2FkX21lZGl1bV9iYW5uZXIsIHNtYWxsXSlcbiAgICAgICAgLmFkZFNpemUoWzEyMDAsIDFdLCBbYWRfc3F1YXJlLCBzbWFsbF0pXG4gICAgICAgIC5idWlsZCgpO1xuXG4gICAgLy8gQWQtZnJlZSBmb290ZXIgdHJhY2tpbmc6IG9uZSBiYW5uZXIgc2l6ZSBwZXIgZGV2aWNlIHNvIFB1bHNlUG9pbnQgY2FuXG4gICAgLy8gc3BsaXQgbW9iaWxlIHZzIGRlc2t0b3AgcmVwb3J0aW5nLiAzMjB4NTAgYmVsb3cgNzY3cHggd2lkZSwgNzI4eDkwIGF0IG9yXG4gICAgLy8gYWJvdmUgaXQuIERlbGliZXJhdGVseSBubyAxeDEgb3IgOTcweDkwLCBzbyBvbmx5IHRoZXNlIHR3byBldmVyIHNlcnZlIGFuZFxuICAgIC8vIGVhY2ggcmVwb3J0cyBvbiBleGFjdGx5IG9uZSBkZXZpY2UgY2xhc3MuXG4gICAgZ2FtX2Zvb3Rlcl90cmFja2luZyA9IGdvb2dsZXRhZy5zaXplTWFwcGluZygpXG4gICAgICAgIC5hZGRTaXplKFsxLCAxXSwgW1szMjAsIDUwXV0pXG4gICAgICAgIC5hZGRTaXplKFs3NjcsIDFdLCBbWzcyOCwgOTBdXSlcbiAgICAgICAgLmJ1aWxkKCk7XG5cbiAgICAvLyBEZWZpbmUgb3RoZXIgYWQgc2xvdHMgKGUuZy4sIHN0YXRpYy1mb290ZXIpIHRoYXQgc2hvdWxkIHN0aWxsIHJlbmRlciBvbiBtb2JpbGUuXG4gICAgLy8gU2tpcHBlZCB3aGVuIHRoZSBwYWdlIGhhcyBubyBmb290ZXIgdW5pdDogZGVmaW5pbmcgYSBzbG90IHdob3NlIGNvbnRhaW5lciB3YXNcbiAgICAvLyBzdXBwcmVzc2VkIHN0aWxsIHNlbmRzIHRoZSBhZCByZXF1ZXN0LCBzbyBhbiBhZC1mcmVlIHBhZ2Ugd2FzIGFza2luZyBHQU0gZm9yXG4gICAgLy8gaW52ZW50b3J5IGl0IGhhZCBubyBpbnRlbnRpb24gb2Ygc2hvd2luZy5cbiAgICAvLyBTdHJpbmcgY29tcGFyZSBvbiBwdXJwb3NlOiB3cF9sb2NhbGl6ZV9zY3JpcHQgc3RyaW5naWZpZXMsIHNvIHRoaXMgYXJyaXZlc1xuICAgIC8vIGFzIFwiMFwiLCBhbmQgYSBzdHJpY3QgIT09IDAgd291bGQgaGF2ZSBiZWVuIHRydWUgb24gZXZlcnkgcGFnZS5cbiAgICBpZiAodHlwZW9mIGdhbSA9PT0gJ3VuZGVmaW5lZCcgfHwgU3RyaW5nKGdhbS5zdGF0aWNfZm9vdGVyKSAhPT0gJzAnKSB7XG4gICAgICAgIGdvb2dsZXRhZy5kZWZpbmVTbG90KCcvMTAwMzIxMC9zdGF0aWMtZm9vdGVyJywgW1szMjAsIDUwXV0sICdzdGF0aWMtZm9vdGVyJylcbiAgICAgICAgICAgIC5kZWZpbmVTaXplTWFwcGluZyhnYW1fYmFubmVyKVxuICAgICAgICAgICAgLnNldFRhcmdldGluZyhcInBvc2l0aW9uXCIsIFwic3RhdGljLWZvb3RlclwiKVxuICAgICAgICAgICAgLmFkZFNlcnZpY2UoZ29vZ2xldGFnLnB1YmFkcygpKTtcbiAgICB9IGVsc2Uge1xuICAgICAgICAvLyBBZC1mcmVlIHBhZ2VzIHN0aWxsIHJlcXVlc3QgdGhpcyB1bml0LCBmb3IgdHJhY2tpbmcgb25seSwgaW50byBhXG4gICAgICAgIC8vIGNvbnRhaW5lciB0aGF0IG9jY3VwaWVzIG5vIHNwYWNlIChzZWUgZm9vdGVyLnBocCkuIFRoZSBpbXByZXNzaW9uIGlzXG4gICAgICAgIC8vIGhvdyB3ZSBzaWduYWwgUHVsc2VQb2ludCwgc28gdGhpcyBzbG90IG11c3QgZmlsbC5cbiAgICAgICAgLy9cbiAgICAgICAgLy8gUGVyIGFkIG9wcywgdGhlIHJlcXVlc3QgY2FycmllcyB0aGUgc3RhbmRhcmQgZm9vdGVyIGJhbm5lciBzaXplcywgb25lXG4gICAgICAgIC8vIHBlciBkZXZpY2UgKDMyMHg1MCBtb2JpbGUsIDcyOHg5MCBkZXNrdG9wLCB2aWEgZ2FtX2Zvb3Rlcl90cmFja2luZyk6XG4gICAgICAgIC8vIHRoZSBQdWxzZVBvaW50IHRyYWNraW5nIGxpbmUgaXRlbSdzIGNyZWF0aXZlcyBhcmUgc3RhbmRhcmQgc2l6ZXMsIHNvIGFcbiAgICAgICAgLy8gMXgxLW9ubHkgcmVxdWVzdCBjb3VsZCBuZXZlciBmaWxsIGl0IChnZXRSZXNwb25zZUluZm9ybWF0aW9uIHdhcyBudWxsKSxcbiAgICAgICAgLy8gYW5kIHRoZSBtb2JpbGUvZGVza3RvcCBzcGxpdCBpcyBzZXBhcmF0ZWQgaW4gUHVsc2VQb2ludCByZXBvcnRpbmcuIFRoZVxuICAgICAgICAvLyBjb250YWluZXIgc3RheXMgMXB4L2hpZGRlbiwgc28gd2hhdGV2ZXIgc2VydmVzIGlzIGFuIGludmlzaWJsZSB0cmFja2luZ1xuICAgICAgICAvLyBpbXByZXNzaW9uLCB3aGljaCBpcyB0aGUgd2hvbGUgcG9pbnQgb24gYW4gYWQtZnJlZSBwYWdlLlxuICAgICAgICBnb29nbGV0YWcuZGVmaW5lU2xvdCgnLzEwMDMyMTAvc3RhdGljLWZvb3RlcicsIFtbMzIwLCA1MF0sIFs3MjgsIDkwXV0sICdzdGF0aWMtZm9vdGVyLXRyYWNraW5nJylcbiAgICAgICAgICAgIC5kZWZpbmVTaXplTWFwcGluZyhnYW1fZm9vdGVyX3RyYWNraW5nKVxuICAgICAgICAgICAgLnNldFRhcmdldGluZyhcInBvc2l0aW9uXCIsIFwic3RhdGljLWZvb3RlclwiKVxuICAgICAgICAgICAgLmFkZFNlcnZpY2UoZ29vZ2xldGFnLnB1YmFkcygpKTtcbiAgICB9XG5cbiAgICAvLyBDaGVjayBpZiBwYWdlX3RhcmdldGluZyBleGlzdHMgYW5kIGFwcGx5IGl0IHRvIHRoZSBwYWdlLWxldmVsIHRhcmdldGluZ1xuICAgIGlmIChnYW0ucGFnZV90YXJnZXRpbmcpIHtcbiAgICAgICAgdmFyIHRhcmdldGluZyA9IEpTT04ucGFyc2UoZ2FtLnBhZ2VfdGFyZ2V0aW5nKTtcbiAgICAgICAgZm9yICh2YXIga2V5IGluIHRhcmdldGluZykge1xuICAgICAgICAgICAgaWYgKHRhcmdldGluZy5oYXNPd25Qcm9wZXJ0eShrZXkpKSB7XG4gICAgICAgICAgICAgICAgZ29vZ2xldGFnLnB1YmFkcygpLnNldFRhcmdldGluZyhrZXksIHRhcmdldGluZ1trZXldLnRvU3RyaW5nKCkpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxuXG4gICAgLy8gRW5hYmxlIGxhenkgbG9hZGluZyBhbmQgb3RoZXIgc2VydmljZXMuXG4gICAgLy9cbiAgICAvLyBMYXp5IGxvYWRpbmcgb25seSBlYXJucyBpdHMga2VlcCB3aGVyZSB0aGVyZSBhcmUgcmVhbCBhZHMgdG8gZGVmZXIuIEFuXG4gICAgLy8gYWQtZnJlZSBwYWdlIGhhcyBleGFjdGx5IG9uZSBzbG90LCB0aGUgaW52aXNpYmxlIDF4MSB0cmFja2luZyBwaXhlbCwgYW5kXG4gICAgLy8gZGVmZXJyaW5nIHRoYXQgaXMgd2hhdCBzdG9wcGVkIGl0IGZldGNoaW5nIGF0IGFsbDogUHVibGlzaGVyIENvbnNvbGVcbiAgICAvLyByZXBvcnRlZCB0aGUgc2xvdCBkZWZpbmVkIGFuZCBkaXNwbGF5ZWQgd2l0aCBcIkFkIHVuaXQgZGlkIG5vdCBmZXRjaFwiLlxuICAgIC8vIFRoZXJlIGlzIG5vdGhpbmcgdG8gZGVmZXIgaGVyZSwgc28gaXQgc3RheXMgb2ZmIGFuZCB0aGUgc2xvdCBmZXRjaGVzIG9uXG4gICAgLy8gbG9hZCB3aGVyZXZlciBpdCBoYXBwZW5zIHRvIHNpdCBpbiB0aGUgZG9jdW1lbnQuXG4gICAgaWYgKHR5cGVvZiBnYW0gPT09ICd1bmRlZmluZWQnIHx8IFN0cmluZyhnYW0uc3RhdGljX2Zvb3RlcikgIT09ICcwJykge1xuICAgICAgICBnb29nbGV0YWcucHViYWRzKClcbiAgICAgICAgICAgIC5lbmFibGVMYXp5TG9hZCh7XG4gICAgICAgICAgICAgICAgZmV0Y2hNYXJnaW5QZXJjZW50OiA1MCxcbiAgICAgICAgICAgICAgICByZW5kZXJNYXJnaW5QZXJjZW50OiAxMCxcbiAgICAgICAgICAgICAgICBtb2JpbGVTY2FsaW5nOiAxLjBcbiAgICAgICAgICAgIH0pO1xuICAgIH1cblxuICAgIGdvb2dsZXRhZy5lbmFibGVTZXJ2aWNlcygpO1xufSk7XG5cbi8vIEFwcGx5IHRoZSBhc3luYyBJUVZJQSBIQ1AgaWRlbnRpdHkgKHdpbmRvdy5pcXZpYVRhcmdldGluZy5pcXZpYV90eXBlLCBzZXQgYnlcbi8vIHRoZSBhaW0tdGFnIHNpZ25hbCBjYWxsYmFjayBpbiBoZWFkZXIucGhwKSBhcyBwYWdlLWxldmVsIHRhcmdldGluZyBhcyBzb29uIGFzXG4vLyBpdCByZXNvbHZlcy4gVGhpcyBpcyBpbnRlbnRpb25hbGx5IEFERElUSVZFOiB0aGUgZW5hYmxlU2VydmljZXMoKS9kaXNwbGF5KClcbi8vIGZsb3cgYWJvdmUgaXMgbGVmdCB1bnRvdWNoZWQsIGJlY2F1c2UgZGVmZXJyaW5nIGVuYWJsZVNlcnZpY2VzKCkgdW50aWxcbi8vIGlkZW50aXR5IHJlc29sdmVzIGJsYW5rcyBhbnkgc2xvdCB3aG9zZSBkaXNwbGF5KCkgcnVucyBmaXJzdCAodGhhdCBicm9rZSBhZFxuLy8gc2VydmluZyBpbiBhIHByaW9yIGF0dGVtcHQpLiBQYWdlLWxldmVsIHRhcmdldGluZyBhcHBsaWVzIHRvIGV2ZXJ5IGFkIHJlcXVlc3Rcbi8vIG1hZGUgYWZ0ZXIgdGhpcyBwb2ludDsgd2l0aCBsYXp5IGxvYWQgb24sIHRoZSBsYXJnZSBtYWpvcml0eSBvZiBzbG90cyBmZXRjaFxuLy8gbGF0ZXIgYW5kIHBpY2sgaXQgdXAuIFdlIGRlbGliZXJhdGVseSBkbyBOT1QgcmVmcmVzaCgpIGFscmVhZHktZmV0Y2hlZCBzbG90cyxcbi8vIHdoaWNoIHdvdWxkIGRvdWJsZS1jb3VudCBpbXByZXNzaW9ucyBpbiBHQU0gcmVwb3J0aW5nLlxuZnVuY3Rpb24gYXBwbHlJcXZpYVRhcmdldGluZygpIHtcbiAgICBpZiAod2luZG93LmlxdmlhVGFyZ2V0aW5nICYmIHdpbmRvdy5pcXZpYVRhcmdldGluZy5pcXZpYV90eXBlKSB7XG4gICAgICAgIGdvb2dsZXRhZy5jbWQucHVzaChmdW5jdGlvbiAoKSB7XG4gICAgICAgICAgICBnb29nbGV0YWcucHViYWRzKCkuc2V0VGFyZ2V0aW5nKCdpcXZpYV90eXBlJywgU3RyaW5nKHdpbmRvdy5pcXZpYVRhcmdldGluZy5pcXZpYV90eXBlKSk7XG4gICAgICAgIH0pO1xuICAgIH1cbn1cblxuaWYgKHdpbmRvdy5pcXZpYVRhcmdldGluZ1JlYWR5KSB7XG4gICAgLy8gSWRlbnRpdHkgcmVzb2x2ZWQgYmVmb3JlIHRoaXMgc2NyaXB0IHJhbi5cbiAgICBhcHBseUlxdmlhVGFyZ2V0aW5nKCk7XG59IGVsc2Uge1xuICAgIC8vIE90aGVyd2lzZSBhcHBseSBpdCB0aGUgbW9tZW50IHRoZSBpZGVudGl0eSBsb29rdXAgY29tcGxldGVzLlxuICAgIHdpbmRvdy5hZGRFdmVudExpc3RlbmVyKCdpcXZpYVRhcmdldGluZ1JlYWR5JywgYXBwbHlJcXZpYVRhcmdldGluZywgeyBvbmNlOiB0cnVlIH0pO1xufVxuXG5kb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdET01Db250ZW50TG9hZGVkJywgZnVuY3Rpb24oKSB7XG4gICAgLy8gRnVuY3Rpb24gdG8gcmVmcmVzaCBhZHNcbiAgICBmdW5jdGlvbiByZWZyZXNoQWRzKCkge1xuICAgICAgICBnb29nbGV0YWcucHViYWRzKCkucmVmcmVzaCgpO1xuICAgIH1cblxuICAgIC8vIExpc3RlbiBmb3Igd2luZG93IHJlc2l6ZSBhbmQgcmVmcmVzaCBhZHNcbiAgICBsZXQgcmVzaXplVGltZW91dDtcbiAgICB3aW5kb3cuYWRkRXZlbnRMaXN0ZW5lcigncmVzaXplJywgZnVuY3Rpb24oKSB7XG4gICAgICAgIGNsZWFyVGltZW91dChyZXNpemVUaW1lb3V0KTtcbiAgICAgICAgcmVzaXplVGltZW91dCA9IHNldFRpbWVvdXQoZnVuY3Rpb24oKSB7XG4gICAgICAgICAgICByZWZyZXNoQWRzKCk7XG4gICAgICAgIH0sIDI1MCk7IC8vIFJlZnJlc2ggYWRzIGFmdGVyIHJlc2l6ZSBpcyBjb21wbGV0ZSAoZGVib3VuY2UgdG8gcHJldmVudCBleGNlc3NpdmUgcmVmcmVzaGVzKVxuICAgIH0pO1xuXG4gICAgY29uc3QgZm9vdGVyQWQgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnc3RhdGljLWZvb3RlcicpO1xuICAgIGNvbnN0IGRpc21pc3NCdG4gPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjZm9vdGVyLWFkLWNvbnRhaW5lciAuYWQtZGlzbWlzcycpO1xuXG4gICAgaWYgKGRpc21pc3NCdG4pIHtcbiAgICAgICAgZGlzbWlzc0J0bi5zdHlsZS5kaXNwbGF5ID0gJ2Jsb2NrJztcbiAgICAgICAgaWYgKCFkaXNtaXNzQnRuLmRhdGFzZXQuYm91bmQpIHtcbiAgICAgICAgICAgIGRpc21pc3NCdG4uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgICAgICAgICAgICAgY29uc3QgY29udGFpbmVyID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ2Zvb3Rlci1hZC1jb250YWluZXInKTtcbiAgICAgICAgICAgICAgICBjb250YWluZXI/LnJlbW92ZSgpO1xuICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICBkaXNtaXNzQnRuLmRhdGFzZXQuYm91bmQgPSAndHJ1ZSc7XG4gICAgICAgIH1cbiAgICB9XG5cbn0pOyJdLCJmaWxlIjoiZ2FtLWluaXQuanMifQ==
