from typing import Match
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from robot.api.deco import keyword
from robot.errors import ExecutionFailed
from  .Elements  import BasicWebObject
from  .Commons import commons


class Login(BasicWebObject):

    name = "login"
    description = "Correspond à la page login"

    BuiltIn = BuiltIn()
    log = logger

    @property
    def applib(self):
        return self.BuiltIn.get_library_instance('AppiumLibrary')

    _locators = {
        "input_nom_famille": {"ios": "nsp=value == 'Mon nom de famille'", 
                            "android": "//android.widget.EditText[contains(@text, 'Mon nom de famille')]"},

        "input_identifiant": {"ios": "nsp=value == 'Mon identifiant (n° de mobile, e-mail etc.)'", 
                            "android": "//android.widget.EditText[contains(@text, 'Mon identifiant (n° de mobile, e-mail etc.)')]"},

        "input_mot_de_passe": {"ios": "//XCUIElementTypeStaticText[@name='']/preceding-sibling::XCUIElementTypeOther", 
                            "android": "//android.widget.TextView[@text='']/preceding-sibling::android.widget.EditText"}

    }

    
    def _check_object(self):
      self.get_and_check_visible_element("bouton me connecter")
      self.BuiltIn.sleep('5s','Attente des appels suite au chargement de la page')


    @keyword("s'authenifier avec",tags=[name])
    def authentification_picasso(self,name,login,password,faceID=False):
        '''
        sur la page d'authentification procéde a la saisie du login et mot de passe
        '''
        self.get_and_input_text_in_element('input nom famille',name)
        self.BuiltIn.sleep('0.5s')
        self.get_and_input_text_in_element('input identifiant',login)
        self.BuiltIn.sleep('0.5s')
        self.get_and_input_text_in_element('input mot de passe',password)
        self.BuiltIn.sleep('0.5s')
        self.applib.hide_keyboard(key_name="retour")
        self.get_and_click_on_element("bouton me connecter")
        self.BuiltIn.sleep('0.5s')
        if faceID==False:
            self.get_and_check_visible_element("bouton peut etre plus tard")
            self.get_and_click_on_element("bouton peut etre plus tard")
        elif faceID==True:
            self.get_and_check_visible_element("bouton utiliser empreinte digitale")
            self.get_and_click_on_element("bouton utiliser empreinte digitale")
        # self.click_on_element(self._get_element("bouton me connecter"))
        # locator= self._get_element("bouton me connecter")
        # self.BuiltIn.run_keyword_and_ignore_error("bouton",self.applib.click_element(locator))

      
    @keyword('Le texte du placeholder \"${element}\" est affiché en minuscule au dessus du champ saisi')
    def _verifier_placeholder(self,element):
        '''
        Le texte du placeholder identifiant ou mot de passe est affiché en minuscule au dessus du champ saisi
        '''
        self.get_and_check_visible_element(element)
        
    @keyword("L'icone Oeil Est \"${mode}\"")
    def icon_oeil(self, mode='barre'): 
        '''
        verification de l'icone oeil
        '''
        if mode == 'barre':
            self.get_and_check_visible_element("icon oeil barre")
        else:
            self.get_and_check_visible_element("icon oeil non barre")

    @keyword("Le mot de passe saisi est \"${statut}\"")
    def etat_mot_de_passe(self, statut='non visible'):
        '''
        verification de l'affichage su mot de passe : 1-visible 2-non visible
        '''
        if statut == 'non visible':
            locator = self._get_element(
                "valeur mot de passe").format(password="••••••••")
            self.check_visible_element(locator)
        else:
            locator = self._get_element("valeur mot de passe").format(password="p@Ssw0rd")
            self.check_visible_element(locator)

    @keyword("Le bouton 'Je me connecte a mon espace client' est \"${statut}\"")
    def etat_bouton_connexion(self, statut='actif'):
        '''
        verification de l'état du bouton "me connecter"
        '''
        if statut == 'actif':
            locator = self._get_element("bouton me connecter")
            self.applib.element_should_be_enabled(locator)
        else:
            locator = self._get_element("bouton me connecter")
            self.applib.element_should_be_disabled(locator)

    @keyword("Le champ de saisie du 'Mot de passe' est affichée")
    def verifier_page_login_apres_logout(self):
        self.get_and_check_visible_element("input mot de passe")

    @keyword("les 'Mentions Légales' est affiché")
    def verifier_lien_login_mentions_legales(self):
        locator= self._get_element("mentions legales")
        self.applib.page_should_contain_element(locator)

    @keyword("Verifier l'affichage du modale d'activation de connexion")
    def verifier_modale_activation_connexion(self):
        self.get_and_check_visible_element("bouton peut etre plus tard")

    @keyword("Message de non validité des champs saisi est affiché")
    def verifier_messgae_non_validite_authentification(self):
        self.get_and_check_visible_element("message non validite authentification")

    @keyword("Vérification de la page warning")
    def verifier_page_warning(self):
        self.get_and_check_visible_element("oups 3 erreurs")
        self.get_and_check_visible_element("bouton nouvelle tentative")
        self.get_and_check_visible_element("bouton reinitialiser mot de passe")
        
    @keyword("Attendre la fin du décompte de 4 minutes")
    def attendre_fin_blocage_authentification(self):
        locator= self._get_element("bouton me connecter")
        self.applib.wait_until_element_is_visible(locator,timeout="245s")

    # @keyword("Personnalisation de l'application")
    # def gerer_personnalisation_application(self):
    #     self.get_and_check_visible_element("bouton etape suivante")
    #     self.get_and_click_on_element("bouton etape suivante")
    #     self.get_and_check_visible_element("bouton etape suivante")
    #     self.get_and_click_on_element("bouton etape suivante")
    #     self.get_and_check_visible_element("bouton etape suivante")
    #     # self.get_and_click_on_element("bouton etape suivante")
    #     # self.get_and_click_on_element("bouton etape suivante")
    #     locator= self._get_element("bouton etape suivante")
    #     self.applib.long_press(locator)
    #     self.get_and_check_visible_element("bouton acceder ecran acceuil")
    #     self.get_and_click_on_element("bouton acceder ecran acceuil")

class ForgetPassword(BasicWebObject):

    name = "mot de passe oublie"
    description = "Correspond à la page mot de passe oublié"

    BuiltIn = BuiltIn()
    log = logger

    @property
    def applib(self):
        return self.BuiltIn.get_library_instance('AppiumLibrary')

    _locators = {
        "page_mot_de_passe_oublie": {"ios": "accessibility_id=C'est parti pour une chasse au mot de passe", "android": '//android.widget.TextView[@text="C\'est parti pour une chasse au mot de passe"]'},
        "retourner_a_laccueil": {"ios": "accessibility_id=Retourner à l'accueil", "android": '//android.widget.TextView[@text="Retourner à l\'accueil"]'},
        "icon_cadenas": {"ios": "//XCUIElementTypeStaticText[@name='']", "android": "//android.widget.TextView[@text='']"},
        "texte_renseignez_identifiant": {"ios": "accessibility_id=Renseigner votre identifiant et votre nom de famille pour recevoir un code de vérification.", "android": "//android.widget.TextView[@text='Renseigner votre identifiant et votre nom de famille pour recevoir un code de vérification.']"},
        "input_identifiant": {"ios": "xpath=(//XCUIElementTypeOther[@name='Votre n° de mobile, clé / tablette ou email'])[1]", "android": "//android.widget.EditText[@text='Votre n° de mobile, clé / tablette ou email']"},
        "input_nom_de_famille": {"ios": "xpath=(//XCUIElementTypeOther[@name='Votre nom de famille'])[1]", "android": "//android.widget.EditText[@text='Votre nom de famille']"},
        "bouton_continuer": {"ios": "nsp=label=='Continuer'", "android": "//android.widget.TextView[@text='Continuer']"},
        "saisir_code_verification": {"ios": "accessibility_id=Saisir le code de vérification", "android": "//android.widget.Button[@content-desc='retour, back']"},
    }

    def _check_object(self):
      self.get_and_check_visible_element("page mot de passe oublie")
      self.BuiltIn.sleep(
          '5s', 'Attente des appels suite au chargement de la page')
