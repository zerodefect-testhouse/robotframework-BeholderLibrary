# Robot Framework - BeholderLibrary

A Robot Framework's library to integrate with the Zero Defect's Visual Regression testing platform.


## Installation

The recommended installation method is using [pip](http://pip-installer.org/):

```sh
pip install robotframework-beholderlibrary
```

Running this command installs also the latest [SeleniumLibrary](https://github.com/robotframework/SeleniumLibrary) and [Robot Framework](https://robotframework.org)
versions, but you still need to install `browser drivers` separately.
The `--upgrade` option can be omitted when installing the library for the
first time.

With recent versions of `pip` it is possible to install directly from the
GitHub_ repository. To install latest source from the master branch, use
this command:
```sh
pip install git+https://github.com/zerodefect-testhouse/robotframework-BeholderLibrary.git
```
Please note that installation will take some time, because `pip` will
clone the BeholderLibrary project to a temporary directory and then
perform the installation.


## Usage

To use BeholderLibrary in Robot Framework tests, the library needs to
first be imported using the `Library` setting as any other library.

```robot

    *** Settings ***
    Documentation     Simple example using BeholderLibrary.
    Library           SeleniumLibrary
    Library           BeholderLibrary

    *** Variables ***
    ${URL}      http://localhost:8000
    ${BROWSER}        Chrome

    *** Test Cases ***
    Verify HomePage
        Open Browser to HomePage
        Welcome Page Should Be Correctly Displayed
        [Teardown]    Close Browser

    *** Keywords ***
    Open Browser to HomePage
        Open Browser    ${URL}    ${BROWSER}
        Title Should Be    Login Page


    Input Password
        [Arguments]    ${password}
        Input Text    password_field    ${password}

    Submit Credentials
        Click Button    login_button

    Welcome Page Should Be Correctly Displayed
        Take Beholder Snapshot 
```
