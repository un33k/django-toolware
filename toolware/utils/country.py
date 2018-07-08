import locale
import functools

from django.conf import settings
from django.utils import translation
from django.utils.translation import ugettext as _

from .translation import TranslationMixin


# http://xml.coverpages.org/country3166.html
COUNTRY_CODES = [
    "AD","AE","AF","AG","AI","AL","AM","AO",
    "AQ","AR","AS","AT","AU","AW","AZ","BA",
    "BB","BD","BE","BF","BG","BH","BI","BJ",
    "BM","BN","BO","BR","BS","BT","BW","BY",
    "BZ","CA","CC","CF","CG","CH","CI","CK",
    "CL","CM","CN","CO","CR","CU","CV","CX",
    "CY","CZ","DE","DJ","DK","DM","DO","DZ",
    "EC","EE","EG","EH","ER","ES","ET","FI",
    "FJ","FK","FM","FO","FR","GA","GB","GD",
    "GE","GF","GH","GI","GL","GM","GN","GP",
    "GQ","GR","GS","GT","GU","GW","GY","HK",
    "HM","HN","HR","HT","HU","ID","IE","IL",
    "IN","IO","IQ","IR","IS","IT","JM","JO",
    "JP","KE","KG","KH","KI","KM","KN","KP",
    "KR","KW","KY","KZ","LA","LB","LC","LI",
    "LK","LR","LS","LT","LU","LV","LY","MA",
    "MC","MD","MG","MH","ML","MN","MM","MO",
    "MP","MQ","MR","MS","MT","MU","MV","MW",
    "MX","MY","MZ","NA","NC","NE","NF","NG",
    "NI","NL","NO","NP","NR","NU","NZ","OM",
    "PA","PE","PF","PG","PH","PK","PL","PM",
    "PN","PR","PT","PW","PY","QA","RE","RO",
    "RU","RW","SA","SB","SC","SD","SE","SG",
    "SH","SI","SJ","SK","SL","SM","SN","SO",
    "SR","ST","SV","SY","SZ","TC","TD","TF",
    "TG","TH","TJ","TK","TM","TN","TO","TR",
    "TT","TV","TW","TZ","UA","UG","UM","US",
    "UY","UZ","VA","VC","VE","VG","VI","VN",
    "VU","WF","WS","YE","YT","ZA","ZM","ZW"
]


class CountryField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 2)
        kwargs.setdefault('choices', COUNTRY_CODES)
        super(CharField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"


class Country(TranslationMixin):
    "Singleton translation-aware class for Countries"
    
    def __init__(self, *args, **kwargs):
        self.__init__(*args, **kwargs)
        self.priority = getattr(settings, 'PRIORITY_COUNTRY_CODES')


country = Country(prefix="ISO_3166-1.", codes=COUNTRY_CODES)

# Usage:
# from toolware.utils.country import country, CountryField
# country = CountryField(
#     _("Country"),
#     choices=country.get_priority_translations(),
#
# Note: LOCALE_PATHS must include path to translations.country.locale in this module