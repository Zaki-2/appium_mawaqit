*** Settings ***
Documentation    Contient l'ensemble des mots-clés et ressources communes au tests
Library    OperatingSystem    
Resource    loader.robot

*** Variables ***

${ANDROID_SDK_ROOT}=   (path)/Library/Android/sdk

*** Keywords ***

Initialisation
    [Documentation]    Demarre l'emulateur et le serveur Appium et choisir l'environnement de test
    Log Variables
    #Log To Console    Serveur Appium démarré
    #Process.Start Process     appium -p ${Port}  shell=True    alias=appiumserver    stdout=${EXECDIR}/appium_stdout.txt    stderr=${EXECDIR}/appium_stderr.txt
    #Process Should Be Running    appiumserver
    #Log To Console    Lancement du emulateur
    #Process.Start Process    ${ANDROID_SDK_ROOT}/emulator/emulator  @${Capabilities.DEVICE_NAME}    shell=True    alias=androidemu    stdout=${EXECDIR}/emulator_stdout.txt    stderr=${EXECDIR}/emulator_stderr.txt
    #Process Should Be Running    androidemu
    #Sleep    5s    reason=None
    #Log To Console    Emulator ${Capabilities.DEVICE_NAME} est lancé

Terminer Processus 
    Process.Terminate All Processes
  

Demarrer Enregistrement Video
    [Documentation]    Permet de demarer la video
    Run Keyword And Ignore Error   AppiumLibrary.Start Screen Recording
     
Arreter Eenregistrement Video
    [Documentation]    Permet d'arreter la video
    Run Keyword And Ignore Error   AppiumLibrary.Stop Screen Recording

Open Android Application
    [Documentation]    Permet d'ouvrir l'application android de mcare
    [Arguments]  ${noReset}=False
    Open Application  ${${emulator}.REMOTE_URL}
    ...  automationName=${${emulator}.AUTOMATION_NAME}
    ...  platformName=${${emulator}.PLATFORM_NAME}
    ...  platformVersion=${${emulator}.PLATFORM_VERSION}
    ...  deviceName=${${emulator}.DEVICE_NAME}
    ...  appPackage=${${emulator}.PACKAGE_NAME}
    ...  appActivity=${${emulator}.ACTIVITY_NAME}
    ...  noReset=${noReset}
    ...  app=${app}

Open iOS Application
    [Documentation]    Permet d'ouvrir l'application android de mcare
    [Arguments]  ${noReset}=False
    Open Application  ${${emulator}.REMOTE_URL}
    ...  automationName=${${emulator}.AUTOMATION_NAME}
    ...  platformName=${${emulator}.PLATFORM_NAME}
    ...  platformVersion=${${emulator}.PLATFORM_VERSION}
    ...  deviceName=${${emulator}.DEVICE_NAME}
    ...  autoAcceptAlerts=true
    ...  noReset=${noReset}
    ...  applicationName=${${emulator}.APPLICATION_NAME}
    ...  app=${app}
 
Gerer Popup Localisation
    [Documentation]    Permet de gerer le popup de localisation
    AppiumLibrary.Wait Until Element Is Visible  //XCUIElementTypeButton[@name="Allow Once"]   timeout=20s
    AppiumLibrary.Click Element   //XCUIElementTypeButton[@name="Allow Once"]
    
Lancer Application mawaqit
    [Documentation]    Permet de lancer l'application
    [Arguments]  ${noReset}=False
    Run Keyword If  '${OS}'=='iOS'  Open iOS Application  noReset=${noReset}
    ...  ELSE    Open Android Application  noReset=${noReset}

L'utilisateur est redirigé sur la Page
    [Arguments]    ${nom_page}
    Vérifier La Présence De    ${nom_page}

L'utilisateur est sur la Page
    [Arguments]    ${nom_page}
    Vérifier La Présence De    ${nom_page}

Killer L'application
    [Documentation]    Permet de killer l'application
    AppiumLibrary.Quit Application
   
Parcours Teardown
    [Documentation]    Permet de gerer le teardown
    Arreter Eenregistrement Video
    AppiumLibrary.Remove Application   fr.bouyguestelecom.ecm.android.debug

L'image est visible dans la Page 
    [Documentation]  Permet de verifier l'existance d'une image dans la page 
    [Arguments]   ${name}
    ${statut}=    Run Keyword And Return Status  ImageHorizonLibrary.Wait For   reference_image=${name}
    Run Keyword If   "${statut}"=="False"  Log  l'image ${name} n'est pas visible  level=ERROR
    