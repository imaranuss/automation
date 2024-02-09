*** Settings ***

Library  ../../modulo/keywords.py

*** Variables ***
# se pueden meter los valores directamente sustituyendo en el valor de la variable, para realizar la medida.
${vectorial_address}
${instrument_vectorial_analyzer}
${F_inicial}    1.55e9
${F_final}      4.5e9
${points}       2000
${value_z0}     50
*** Test Cases ***

Task 1 Find
    [Documentation]    Find instruments on the network
    [Tags]    Step 00 this step finds the instrument´s IP address
    ${vectorial_address}=   find_e5063a
    Set Global Variable     ${vectorial_address}
    Log     ${vectorial_address}

Task 2 Connect
    [Documentation]    Connecting to a VNA via IP address
    [Tags]    Step 01 this step opens a connection with the instrument
    ${instrument_vectorial_analyzer}=  connect_to_vectorial_analyzer  ${vectorial_address}
    Set Global Variable     ${instrument_vectorial_analyzer}
    Log     ${instrument_vectorial_analyzer}

Task 3 Reset instrument
    [Documentation]    resetting instrument
    [Tags]    Step 02 this step applies a reset
    reset_vectorial  ${instrument_vectorial_analyzer}

Task 4 Set internal Impedance
    [Documentation]    performing selection of internal impedance between 50 and 75 ohms
    [Tags]    Step 03 this step sets impedance value
    set_impedancia  ${instrument_vectorial_analyzer}        ${value_z0}

Task 5 Performing measurement
    [Documentation]    charactericing the input impedance of a DUT
    [Tags]    Step 04 this step performs the main task
    caracteriza_dut_sfreq  ${instrument_vectorial_analyzer}       ${F_inicial}       ${F_final}       ${points}       ${value_z0}

Task 6 Disconnecting procedure
    [Documentation]    This part is in charged of disconnection
    [Tags]    Step 05 this step ends a connection with the instrument
    disconnect_from_vectorial_analyzer  ${instrument_vectorial_analyzer}
