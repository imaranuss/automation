*** Settings ***

Library  ../../modulo/keywords.py

*** Variables ***
${gen_address}
${instrument_generator}
${TEST_NAME}    main_barrido_freq
${start_freq}           3e6
${stop_freq}            10e6
${start_amplitude}      -3
${stop_amplitude}       -15
${N_puntos}             2000
${mod_state}            ON

*** Test Cases ***

Task 1 Find
    [Documentation]    Find instruments on the network
    [Tags]    Step 00 this step finds intruments IP address
    ${gen_address}=   find_n5171b
    Set Global Variable     ${gen_address}
    Log     ${gen_address}

Task 2 Connect
    [Documentation]    Connecting to signal generator via IP address
    [Tags]    Step 01 this step opens connection with instrument
    ${instrument_generator}=  connect_to_signal_generator  ${gen_address}
    Set Global Variable     ${instrument_generator}
    Log     ${instrument_generator}

Task 3 Reset instrument
    [Documentation]    resetting instrument
    [Tags]    Step 02 this step applies a reset
    reset_generador  ${instrument_generator}

Task 4 Performing sweep in frequency
    [Documentation]    performing frequency sweep
    [Tags]    Step 03 this step sets Sweep parameters
    generator_barrido  ${instrument_generator}      ${start_freq}    ${stop_freq}    ${start_amplitude}     ${stop_amplitude}     ${N_puntos}

Task 5 Selecting modulation on/off
    [Documentation]    selection of modulation on or off
    [Tags]    Step 04 this step selects modulation state
    modulacion_off_on  ${instrument_generator}              ${mod_state}

Task 6 Activating output
    [Documentation]    output on
    [Tags]    Step 05 this step activates output
    activar_salida_signal_generator     ${instrument_generator}

Task 7 deactivate output
    [Documentation]    output off
    [Tags]    Step 06 this step turns off output
    desactivar_salida_signal_generator      ${instrument_generator}

Task 8 Disconnecting procedure
    [Documentation]    This part is in charged of disconnection
    [Tags]    Step 07 this step ends connection with instrument
    disconnect_from_vectorial_analyzer  ${instrument_generator}

*** Keywords ***
