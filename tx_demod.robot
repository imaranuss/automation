*** Settings ***
Library  ../../modulo/keywords.py

*** Variables ***
# se pueden meter los valores directamente sustituyendo en el valor de la variable, para realizar la medida.
${spectrum_address}
${instrument_spectrum}
${cnt_freq}     107.9e6     #valor de frecuencia central para la demodulación fm
${span}     0             #valor de span.  a span distinto a 0, no se ejecuta la demodulación

*** Test Cases ***
Task 1 Find
    [Documentation]    Finding the instrument on the network
    [Tags]  Step 00 finding the correct instrument to iniciate procedure
    Log     ${spectrum_address}
    ${spectrum_address}=   find_n9320b
    Set Global Variable    ${spectrum_address}
    Log     ${spectrum_address}

Task 2 Connect
    [Documentation]    Connecting to spectrum analyzer via IP address
    [Tags]  Step 01 Opening connection with the instrument
    Log  ${spectrum_address}
    ${instrument_spectrum}=  connect_to_spectrum_analyzer       ${spectrum_address}
    Set Global Variable    ${instrument_spectrum}
    Log  ${spectrum_address}
    Log  ${instrument_spectrum}

#Task 3 Reset instrument
#    [Documentation]    resetting instrument
#    [Tags]  Step 02 Performing a reset to the instrument to start with no errors
 #   reset_spectrum  ${instrument_spectrum}

Task 4 Performing main task
    [Documentation]    Demodulating audio transmision FM
    [Tags]  Step 03 In this step the demodulation is applied
    demod_fm  ${instrument_spectrum}        ${cnt_freq}     ${span}

Task 5 Disconnecting procedure
    [Documentation]    Disconnecting from the instrument in use
    [Tags]  Step 04 Ends the connection with the instrument
    disconnect_from_signal_generator  ${instrument_spectrum}

