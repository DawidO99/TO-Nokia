*** Settings ***
Library    ../libs/EpcSimulationLibrary.py

*** Keywords ***
Reset Simulator
    Reset Simulator

Attach UE
    [Arguments]    ${id}
    Attach UE    ${id}

Detach UE
    [Arguments]    ${id}
    Detach UE    ${id}

Start DL Transfer
    [Arguments]    ${ue_id}    ${speed}    ${bearer_id}=9
    Start DL Transfer    ${ue_id}    ${speed}    ${bearer_id}

Verify DL Transfer
    [Arguments]    ${ue_id}    ${expected_speed}
    Verify DL Transfer    ${ue_id}    ${expected_speed}

Verify UE Is Connected
    [Arguments]    ${id}
    Verify UE Is Connected    ${id}

Verify UE Is Disconnected
    [Arguments]    ${id}
    Verify UE Is Disconnected    ${id}