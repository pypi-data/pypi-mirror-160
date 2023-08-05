*** Settings ***

Resource  keywords.robot

Test Setup  Setup Mosaic Example Page
Test Teardown  Close all browsers


*** Test Cases ***

Show how Mosaic editor is opened
    Go to  ${PLONE_URL}/example-document
    Wait For Element  id=contentview-edit
    Highlight  id=contentview-edit
    Capture Page Screenshot  mosaic-editor-open.png


Show the Mosaic editing capabilities
    Go to  ${PLONE_URL}/example-document/edit
    Wait For Element  css=.mosaic-select-layout
    Capture Page Screenshot  mosaic-editor-layout-selector.png

    # Show how to select the initial layout
    Wait For Element  jquery=a[data-value="default/basic.html"]
    Highlight  jquery=a[data-value="default/basic.html"] img
    Capture Page Screenshot  mosaic-editor-layout-selector-select.png

    Click element  jquery=a[data-value="default/basic.html"]

    # Show the properties view in Mosaic editor
    Run keyword and ignore error  Set window size  1024  1200
    Wait For Element  css=.mosaic-toolbar
    Click Overlay Button  css=.mosaic-button-properties

    Highlight  css=.autotoc-nav

    Capture Page Screenshot  mosaic-editor-properties-modal.png

    Run keyword and ignore error  Set window size  1024  800
    Click element  css=.modal-wrapper .modal-close

    # Show the Mosaic editor
    Wait For Element  css=.mosaic-toolbar
    Highlight  css=.mosaic-button-layout
    Capture Page Screenshot  mosaic-editor-layout.png

    Element should be visible  css=.mosaic-button-customizelayout

    Highlight  css=.mosaic-button-customizelayout
    Capture Page Screenshot  mosaic-editor-customize.png

    Clear highlight  css=.mosaic-button-layout
    Clear highlight  css=.mosaic-button-customizelayout

    Click element  css=.mosaic-button-customizelayout

    # Show how to select a new tile from menu
    Wait For Element  css=.mosaic-toolbar
    Highlight  css=.select2-container.mosaic-menu-insert
    Click element  css=.select2-container.mosaic-menu-insert a
    Wait until element is visible  css=.select2-result.mosaic-option-irichtextbehavior-text
    Mouse over  css=.mosaic-dropdown .select2-result.mosaic-option-irichtextbehavior-text

    Capture Page Screenshot  mosaic-editor-select-field-text-tile.png

    Clear highlight  css=.mosaic-menu-insert

    # Show how to drag a new tile into its initial position

    Click element  css=.mosaic-dropdown .mosaic-option-irichtextbehavior-text
    Wait until page contains element  css=.mosaic-helper-tile-new
    Wait until element is visible  css=.mosaic-helper-tile-new
    Update element style
    ...  css=.mosaic-IDublinCore-description-tile .mosaic-divider-bottom
    ...  display  block
    Mouse over
    ...  css=.mosaic-IDublinCore-description-tile .mosaic-divider-bottom
    Capture Page Screenshot  mosaic-editor-drag-field-text-tile.png

    # Show how to drop a new tile into its initial position

    Click element  css=.mosaic-selected-divider
    Wait For Element  css=.mosaic-button-save
    Highlight  css=.mosaic-button-save
    Capture Page Screenshot  mosaic-editor-drop-field-text-tile.png

    # Show how the custom layout looks after saving

    Click button  css=.mosaic-button-save
    # some people reported sporadic page unload alert ... if so, accept it
    Run keyword and ignore error  Handle Alert  action=ACCEPT  timeout=5
    Capture Page Screenshot  mosaic-page-saved.png


*** Keywords ***
