#!/usr/bin/env python3
"""
Module APP -- UI Application Classes
Sub-Package UI of Package PLIB3 -- Python UI Framework
Copyright (C) 2008-2022 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information
"""

import sys

from plib.ui.imp import get_toolkit_object


# We will always need this one so we automatically import it

PApplication = get_toolkit_object('app', 'PApplication')


# This also serves as a nice reference for what is where

TOOLKIT_MODS = dict(
    # Standard widgets
    PButton='button',
    PActionButton='button',
    PCheckBox='button',
    PComboBox='combo',
    PNumComboBox='combo',
    PSortedComboBox='combo',
    PTextDisplay='display',
    PEditBox='editctrl',
    PNumEditBox='editctrl',
    PEditControl='editctrl',
    PPanel='form',
    PGroupBox='groupbox',
    PButtonGroup='group',
    PRadioGroup='group',
    PImageView='imageview',
    PTextLabel='label',
    PListBox='listbox',
    PSortedListBox='listbox',
    PTreeView='listview',
    PListView='listview',
    PSortedListView='listview',
    PPageWidget='pagewidget',
    PTable='table',
    PTabWidget='tabwidget',
    
    # Special widgets
    PContainer='container',
    
    # Dialog
    PDialog='dialog',
    
    # Special helpers
    PSocketNotifier='socket',
    PTableLabels='table',
    
    # Mixins for custom widgets to add signals
    PFocusMixin='focus',
    #PKeyboardMixin='keyboard',
    PMouseMixin='mouse',
)


# This is an evil hack, but it works ;)

def __getattr__(name):
    # We do this so that the only toolkit objects that actually get imported
    # are the ones that the application actually uses
    modname = TOOLKIT_MODS.get(name)
    if not modname:
        raise AttributeError("Toolkit object {} not found".format(name))
    obj = get_toolkit_object(modname, name)
    # This ensures we don't have to call this function again for this name
    setattr(sys.modules[__name__], name, obj)
    return obj
