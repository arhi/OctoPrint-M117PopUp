$(function() {
    function M117PopUpViewModel(parameters) {
        var self = this;
		
		self.settingsViewModel = parameters[0];
		
		self.autoClose = ko.observable();
		self.msgType = ko.observable();
		self.msgTypes = ko.observableArray([{
						name : 'Notice',
						value : 'notice'
					}, {
						name : 'Error',
						value : 'error'
					}, {
						name : 'Info',
						value : 'info'
					}, {
						name : 'success',
						value : 'success'
					}
				]);

		self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "M117PopUp") {
				// console.log('Ignoring '+plugin);
                return;
            }
			
			if(data.type == "popup") {
				// console.log(data.msg);
				new PNotify({
					title: 'M117 Pop Up Message',
					text: data.msg,
					type: self.settingsViewModel.settings.plugins.M117PopUp.msgType(),
					hide: self.settingsViewModel.settings.plugins.M117PopUp.autoClose()
					});
			}
		}
		
		self.onBeforeBinding = function() {
            self.msgType(self.settingsViewModel.settings.plugins.M117PopUp.msgType());
            self.autoClose(self.settingsViewModel.settings.plugins.M117PopUp.autoClose());
        }
		
		self.onEventSettingsUpdated = function (payload) {            
            self.msgType = self.settingsViewModel.settings.plugins.M117PopUp.msgType();
            self.autoClose = self.settingsViewModel.settings.plugins.M117PopUp.autoClose();
        }
    }

    // This is how our plugin registers itself with the application, by adding some configuration
    // information to the global variable OCTOPRINT_VIEWMODELS
    ADDITIONAL_VIEWMODELS.push([
        // This is the constructor to call for instantiating the plugin
        M117PopUpViewModel,

        // This is a list of dependencies to inject into the plugin, the order which you request
        // here is the order in which the dependencies will be injected into your view model upon
        // instantiation via the parameters argument
        ["settingsViewModel"],

        // Finally, this is the list of selectors for all elements we want this view model to be bound to.
        ["#settings_plugin_M117PopUp_form"]
    ]);
});