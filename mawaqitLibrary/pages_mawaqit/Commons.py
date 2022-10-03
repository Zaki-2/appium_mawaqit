from .Elements import BasicWebObject
from robot.api.deco import keyword
#script où mettre les webobjects qui ne sont pas liés à des pages. Typiquement des popups.
# script where you should put webobjetcs that are not bound to a specific page. Usually things such as, popups, chat-bots, banners...


class commons(BasicWebObject):
    '''
    Class to handle the privacy agreement popup.

    At the moment, were only closing it by accepting everything
    '''

    _locators = {
        "continuer_sans_accepter":{
            "android": "//android.widget.TextView[@text='Continuer sans accepter']",
            "ios": "//XCUIElementTypeOther[@name='Accepter']"
        },
        "accepter":{
            "android": "//android.widget.TextView[@text='Accepter']",
            "ios": "nsp=label=='Accepter'"
        },
        "bouton_se_deconnecter": {"ios": "xpath=(//XCUIElementTypeOther[@name=''])[4]", "android": "//android.widget.TextView[@text='']"},
        "gerer_mes_choix":{
            "android": "//android.widget.TextView[@text='Continuer sans accepter']",
            "ios": "//XCUIElementTypeOther[@name='Gérer mes choix']"
        },
        "tout_accepter":{
            "android": "//android.widget.TextView[@text='Continuer sans accepter']",
            "ios": "//XCUIElementTypeButton[@name='Tout accepter']"
        },
        "bouton_acceder_espace_client":{
            "android": "accessibility_id=btnAccessMyCustomerArea",
            "ios": "accessibility_id=btnAccessMyCustomerArea"
        }
    }


    @keyword("Lancer L'application")
    def launch_application(self, timeout='40s'):
        '''
        Detects and closes the popup. Won't raise any errors.
        '''
        self.log.info("Détection de la popup liées à la vie privée", also_console=True) 
        try:
            self.applib.wait_until_element_is_visible(self._get_element(
                "continuer sans accepter"), timeout=timeout)
            self.log.info("popup fermée", also_console=True)
        except:
            self.log.info("pas de popup détectée", also_console=True)

    @keyword("Se déconnecter")
    def se_deconnecter(self, timeout='10'):
            self.applib.wait_until_element_is_visible(self._get_element(
                "bouton se deconnecter"), timeout=timeout)
            self.get_and_click_on_element("bouton se deconnecter")


        
