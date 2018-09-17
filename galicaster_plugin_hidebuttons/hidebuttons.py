"""
Plugin to hide buttons from the non-admin UI
"""

from galicaster.core import context

ALL_BUTTONS = {
    "help": "helpbutton",
    "pause": "pausebutton",
    "record": "recbutton",
    "stop": "stopbutton",
    "swap": "swapbutton"
}

dispatcher = context.get_dispatcher()
conf = context.get_conf()
logger = context.get_logger()

def init():
    """
    Plugin initialization
    """
    dispatcher.connect("init", post_init)


def post_init(_source):
    """
    Plugin initialized
    """
    recorder_ui = context.get_mainwindow().nbox.get_nth_page(0).gui

    try:
        if conf.get_boolean('basic', 'admin'):
            logger.info("Admin mode is set to true")
            return
        button_names = set(conf.get('hidebuttons', 'hide').split())
        if not button_names:
            logger.warn("No buttons specified in configuration to hide")
            return
        buttons_to_hide = set(ALL_BUTTONS.keys()).intersection(button_names)
        logger.info("Hiding buttons: {}".format(', '.join(buttons_to_hide)))
        if buttons_to_hide:
            for button_to_hide in buttons_to_hide:
                button = recorder_ui.get_object(ALL_BUTTONS[button_to_hide])
                if button:
                    if not button.get_realized():
                        logger.warn("Hiding button `{}` though it is already hidden...".format(button_to_hide))
                    button.hide()
    except Exception:
        # The conf parameter isn't defined. Ignore
        logger.warn("Plugin enabled but not configured, see documentation on "
                    "setting the 'hide' configuration option for this plugin")
