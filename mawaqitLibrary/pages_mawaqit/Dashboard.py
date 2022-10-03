from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from robot.api.deco import keyword
from robot.errors import ExecutionFailed
from  .Elements  import BasicWebObject


class Dashboard(BasicWebObject):

    name = "dashboard"
    description = "Correspond à la page d'acceuil"


    _locators = {

        "page_acceuil": {"ios": "xpath=//XCUIElementTypeButton[@name=' Accueil']", "android": "//android.widget.TextView[@text='Accueil']"},
        "bouton_se_deconnecter": {"ios": "xpath=(//XCUIElementTypeOther[@name=''])[4]", "android": "//android.widget.TextView[@text='']"},
        "bouton_conso": {"ios": "xpath=//XCUIElementTypeButton[@name=' Conso']", "android": "//android.widget.TextView[@text='Conso']"}

    }   
    
    def _check_object(self):
        self.get_and_check_visible_element("page acceuil")
        self.BuiltIn.sleep('10s','Attente des appels suite au chargement de la page')

    @keyword("L'élément 'Se déconnecter' est affiché")
    def verifier_affichage_bouton_deconnecter(self):
        self.get_and_check_visible_element("bouton se deconnecter")


    @keyword("L'élément 'Se déconnecter' est affiché")
    def verifier_affichage_bouton_deconnecter(self):
        self.get_and_check_visible_element("bouton se deconnecter")
