from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Optional


COUNTRY_SOURCES = {
    "austria": {
        "official": ["bmb.gv.at"],
        "universities": ["univie.ac.at", "tugraz.at", "uibk.ac.at"],
        "portals": ["studyinaustria.at", "oead.at"]
    },
    "belgium": {
        "official": ["belgium.be"],
        "universities": ["kuleuven.be", "ugent.be", "uclouvain.be", "ulb.be"],
        "portals": ["studyinbelgium.be", "research-in-flanders.be"]
    },
    "czech_republic": {
        "official": ["msmt.gov.cz"],
        "universities": ["cuni.cz", "muni.cz", "cvut.cz"],
        "portals": ["studyin.cz", "portal.gov.cz"]
    },
    "denmark": {
        "official": ["ufm.dk"],
        "universities": ["ku.dk", "dtu.dk", "au.dk"],
        "portals": ["studyindenmark.dk"]
    },
    "estonia": {
        "official": ["hm.ee"],
        "universities": ["ut.ee", "taltech.ee"],
        "portals": ["studyinestonia.ee"]
    },
    "finland": {
        "official": ["okm.fi"],
        "universities": ["helsinki.fi", "aalto.fi", "utu.fi"],
        "portals": ["studyinfinland.fi", "studyinfo.fi"]
    },
    "france": {
        "official": ["enseignementsup-recherche.gouv.fr"],
        "universities": ["sorbonne-universite.fr", "universite-paris-saclay.fr", "univ-psl.fr"],
        "portals": ["campusfrance.org", "trouvermonmaster.gouv.fr"]
    },
    "germany": {
        "official": ["bmbf.de"],
        "universities": ["tum.de", "uni-heidelberg.de", "rwth-aachen.de", "lmu.de"],
        "portals": ["daad.de", "academics.de", "research-in-germany.org"]
    },
    "greece": {
        "official": ["minedu.gov.gr"],
        "universities": ["uoa.gr", "auth.gr", "ntua.gr"],
        "portals": ["studyingreece.edu.gr"]
    },
    "hungary": {
        "official": ["kormany.hu"],
        "universities": ["elte.hu", "u-szeged.hu", "bme.hu"],
        "portals": ["studyinhungary.hu", "doktori.hu"]
    },
    "iceland": {
        "official": ["stjornarradid.is"],
        "universities": ["hi.is", "ru.is"],
        "portals": ["study.iceland.is"]
    },
    "italy": {
        "official": ["mur.gov.it"],
        "universities": ["uniroma1.it", "unibo.it", "polimi.it", "unipd.it"],
        "portals": ["universitaly.it"]
    },
    "latvia": {
        "official": ["izm.gov.lv"],
        "universities": ["lu.lv", "rtu.lv"],
        "portals": ["studyinlatvia.lv"]
    },
    "liechtenstein": {
        "official": ["regierung.li"],
        "universities": ["uni.li"],
        "portals": []
    },
    "lithuania": {
        "official": ["smsm.lrv.lt"],
        "universities": ["vu.lt", "ktu.edu"],
        "portals": ["studyin.lt"]
    },
    "luxembourg": {
        "official": ["mesr.gouvernement.lu"],
        "universities": ["uni.lu"],
        "portals": ["fnr.lu"]
    },
    "malta": {
        "official": ["education.gov.mt"],
        "universities": ["um.edu.mt", "mcast.edu.mt"],
        "portals": []
    },
    "netherlands": {
        "official": ["government.nl"],
        "universities": ["tudelft.nl", "uva.nl", "universiteitleiden.nl", "uu.nl"],
        "portals": ["studyinnl.org", "academictransfer.com"]
    },
    "norway": {
        "official": ["regjeringen.no"],
        "universities": ["uio.no", "ntnu.edu", "uib.no"],
        "portals": ["studyinnorway.no"]
    },
    "poland": {
        "official": ["gov.pl/web/science"],
        "universities": ["uw.edu.pl", "uj.edu.pl", "pw.edu.pl"],
        "portals": ["study.gov.pl"]
    },
    "portugal": {
        "official": ["portugal.gov.pt"],
        "universities": ["ulisboa.pt", "up.pt", "uc.pt"],
        "portals": ["studyinportugal.pt", "dges.gov.pt"]
    },
    "slovakia": {
        "official": ["minedu.sk"],
        "universities": ["uniba.sk", "stuba.sk"],
        "portals": ["studyinslovakia.saia.sk"]
    },
    "slovenia": {
        "official": ["gov.si"],
        "universities": ["uni-lj.si", "um.si"],
        "portals": ["studyinslovenia.si"]
    },
    "spain": {
        "official": ["universidades.gob.es"],
        "universities": ["ub.edu", "uam.es", "ucm.es", "upc.edu"],
        "portals": ["studyinginspain.es"]
    },
    "sweden": {
        "official": ["government.se"],
        "universities": ["ki.se", "kth.se", "lu.se", "su.se"],
        "portals": ["studyinsweden.se", "universityadmissions.se"]
    },
    "switzerland": {
        "official": ["sbfi.admin.ch"],
        "universities": ["ethz.ch", "epfl.ch", "uzh.ch", "unige.ch"],
        "portals": ["studyinswitzerland.plus"]
    }
}


class CountryRegistry:
    def __init__(self, sources: Dict):
        self.sources = sources

    def get_sources_for_country(self, country_name: str) -> Optional[Dict]:
        """Normalize input and find the country data."""
        target = country_name.lower().strip().replace(" ", "_")
        return self.sources.get(target)

    def is_url_allowed(self, url: str, country: str) -> bool:
        """Safety check: ensures the agent never leaves the approved domains."""
        country_data = self.get_sources_for_country(country)
        if not country_data:
            return False
        
        # Flatten all allowed domains for that country
        allowed_domains = (
            country_data["official"] + 
            country_data["universities"] + 
            country_data["portals"]
        )
        return any(domain in url for domain in allowed_domains)

# Initialize the helper
registry = CountryRegistry(COUNTRY_SOURCES)