(function() {
	var getLocalStorageItem = function(name, defaultValue) {
		defaultValue = defaultValue || '';
		var returnValue = '';

		try {
			returnValue = localStorage.getItem(name) || defaultValue;
		} catch (e) {
			returnValue = defaultValue;
		}

		return returnValue;
	};

	// infer product and environment from URL
	var product = document.location.pathname.indexOf('nursing') > -1 ? 'n' : 'p';
	var environment = (function() {
		var hostName = document.location.hostname;
		if (/staging/.test(hostName)) {
			return 'staging';
		} else if (/ck2-cert/.test(hostName) || /ck2-dev/.test(hostName)) {
			return 'cert';
		} else if (/dev/.test(hostName) || /localhost/.test(hostName)) {
			return 'dev';
		} else {
			return 'prod';
		}
	})();

	// If language isn't available in localStorage, default to 'en'
	var language = getLocalStorageItem('analytics.page.language', 'en');

	window.defaults = ({
		pageObj: {
			businessUnit: 'els:cs',
			environment: environment,
			eventName: '',
			errorType: '',
			loadTime: '',
			loadTimestamp: String(new Date().getTime()),
			noTracking: getLocalStorageItem('analytics.page.noTracking', 'false'),
			productName: 'ck',
			section: '',
			sectionName: '',
			language: language,
			name: product + ':' + language + ':home-init', // CK-15390: always use defaults for these
			type: 'NP-RD'
		},
		visitorObj: {
			accessType: getLocalStorageItem('analytics.visitor.accessType', 'ae:anon_user'),
			accountId: getLocalStorageItem('analytics.visitor.accountId'),
			accountName: getLocalStorageItem('analytics.visitor.accountName'),
			appSessionId: getLocalStorageItem('analytics.visitor.appSessionId', 'AUTH_PENDING'),
			consortiumId: getLocalStorageItem('analytics.visitor.consortiumId'),
			departmentId: getLocalStorageItem('analytics.visitor.departmentId'),
			departmentName: getLocalStorageItem('analytics.visitor.departmentName'),
			industry: getLocalStorageItem('analytics.visitor.industry'),
			ipAddress: getLocalStorageItem('analytics.visitor.ipAddress'),
			loginStatus: getLocalStorageItem('analytics.visitor.loginStatus', 'anonymous'),
			loginSuccess: getLocalStorageItem('analytics.visitor.loginSuccess', 'false'),
			sisId: getLocalStorageItem('analytics.visitor.sisId'),
			usagePathInfo: getLocalStorageItem('analytics.visitor.usagePathInfo'),
			userId: getLocalStorageItem('analytics.visitor.userId')
		},
		search: '',
		video: ''
	});
})();
