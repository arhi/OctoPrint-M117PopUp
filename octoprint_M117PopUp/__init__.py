# coding=utf-8

import octoprint.plugin
import re
import time
import Adafruit_CharLCD as LCD
import Adafruit_GPIO.MCP230xx as MCP

lcd_rs        = 15
lcd_en        = 13
lcd_d4        = 12
lcd_d5        = 11
lcd_d6        = 10
lcd_d7        =  9
lcd_red       =  6
lcd_green     =  7
lcd_blue      =  8

lcd_columns = 16
lcd_rows = 2

class M117PopUp(octoprint.plugin.AssetPlugin,
				octoprint.plugin.TemplatePlugin,
                octoprint.plugin.SettingsPlugin):

	def on_after_startup(self):
                self.gpio = MCP.MCP23017(0x20, busnum=0)
		self.lcd = LCD.Adafruit_RGBCharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_red, lcd_green, lcd_blue, gpio=self.gpio)

	
	def AlertM117(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
		if gcode and cmd.startswith("M117"):
			self._plugin_manager.send_plugin_message(self._identifier, dict(type="popup", msg=re.sub(r'^M117\s?', '', cmd)))
			self.lcd.clear()
			self.lcd.message(re.sub(r'^M117\s?', '', cmd))
			return
	
	##-- AssetPlugin hooks
	def get_assets(self):
		return dict(js=["js/M117PopUp.js"])
		
	##-- Settings hooks
	def get_settings_defaults(self):
		return dict(msgType="info",autoClose=True)	
	
	##-- Template hooks
	def get_template_configs(self):
		return [dict(type="settings",custom_bindings=True)]
		
	##~~ Softwareupdate hook
	def get_version(self):
		return self._plugin_version
		
	def get_update_information(self):
		return dict(
			m117popup=dict(
				displayName="M117PopUp",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="jneilliii",
				repo="OctoPrint-M117PopUp",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/arhi/OctoPrint-M117PopUp-and-LCD/archive/{target_version}.zip"
			)
		)

__plugin_name__ = "M117PopUp"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = M117PopUp()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.AlertM117,
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
