# The MIT License (MIT)
#
# Copyright (c) 2017 University of Sussex
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
Hides button controls from the Galicaster recorder UI
"""

from galicaster.core import context


ALL_BUTTONS = {
    "record": "recbutton",
    "pause": "pausebutton",
    "stop": "stopbutton",
    "help": "helpbutton"
}
"""
The edit and swap buttons aren't included as part of this plugin, `swap` can be
configured within [basic] and `edit` is an admin-only option.
"""

dispatcher = context.get_dispatcher()
conf = context.get_conf()
logger = context.get_logger()

def init():
    """
    Plugin initialization
    """
    
    dispatcher.connect("init", post_init)


def post_init(source=None):
    """
    Plugin initialized
    """
    recorder_ui = context.get_mainwindow().nbox.get_nth_page(0).gui

    # Customize buttons in the recorder UI
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
                    button.hide()
    except Exception:
        # The conf parameter isn't defined. Ignore
        logger.warn("Plugin enabled but not configured, see documentation on "
                    "setting the 'hide' configuration option for this plugin")