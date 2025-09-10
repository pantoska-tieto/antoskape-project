*** Settings ***
Library           Process

*** Test Cases ***
Echo Command
    ${result}=    Run Process    echo    Hello, Zephyr!
    Should Contain    ${result.stdout}    Hello, Zephyr!