import requests
import csv
import zipfile
import io
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# ✅ Nigerian Banks
nigerian_banks = [
    "accessbankplc.com", "gtbank.com", "zenithbank.com", "firstbanknigeria.com",
    "uba.com", "fidelitybank.ng", "unionbankng.com", "stanbicibtcbank.com",
    "ecobank.com", "polarisbanklimited.com", "providusbank.com", "jaizbankplc.com",
    "wema.ng", "heritagebank.com", "sterling.ng", "keystonebankng.com", "fcmb.com"
]

# ✅ Nigerian Universities & Oyo Schools
nigerian_universities = [
    "unilag.edu.ng", "ui.edu.ng", "oauife.edu.ng", "lasu.edu.ng", "uniben.edu",
    "unilorin.edu.ng", "unn.edu.ng", "abu.edu.ng", "buk.edu.ng", "futa.edu.ng",
    "lautech.edu.ng", "uniosun.edu.ng", "osunpoly.edu.ng", "eksu.edu.ng", "eksuportal.eksu.edu.ng",
    "unimed.edu.ng", "uniosun.edu.ng", "uniabuja.edu.ng", "noun.edu.ng", "unilag.edu.ng",
    "oysconme.edu.ng", "oyscatech.edu.ng", "ibpoly.edu.ng"
]

# ✅ Popular Vendors (global & Nigerian)
global_vendors = [
    "google.com", "facebook.com", "amazon.com", "jumia.com.ng", "konga.com",
    "netflix.com", "paypal.com", "apple.com", "youtube.com", "mtn.ng",
    "airtel.com.ng", "9mobile.com.ng", "tiktok.com", "instagram.com", "whatsapp.com",
    "snapchat.com", "twitter.com", "linkedin.com", "microsoft.com", "openai.com",
    "spotify.com", "ubereats.com", "uber.com", "paxful.com"
]

# ✅ Federal Government & Military
nigerian_gov_domains = [
    "nigeria.gov.ng", "e.gov.ng", "osgf.gov.ng", "statehouse.gov.ng"
]

ministries = [
    "agriculture.gov.ng", "fmard.gov.ng", "artculture.gov.ng", "aviation.gov.ng",
    "budgetoffice.gov.ng", "commtech.gov.ng", "defence.gov.ng", "education.gov.ng",
    "environment.gov.ng", "fcta.gov.ng", "finance.gov.ng", "foreignaffairs.gov.ng",
    "health.gov.ng", "housing.gov.ng", "humanitarianaffairs.gov.ng",
    "industry.gov.ng", "information.gov.ng", "interior.gov.ng", "justice.gov.ng",
    "labour.gov.ng", "maritime.gov.ng", "nigerdelta.gov.ng", "petroleumresources.gov.ng",
    "policeaffairs.gov.ng", "power.gov.ng", "minesandsteel.gov.ng", "specialduties.gov.ng",
    "sports.gov.ng", "tourism.gov.ng", "transportation.gov.ng", "waterresources.gov.ng",
    "womenaffairs.gov.ng", "youthandsports.gov.ng"
]

national_assembly = [
    "customs.gov.ng", "immigration.gov.ng", "frsc.gov.ng", "ncc.gov.ng", "ncdc.gov.ng",
    "nafdac.gov.ng", "ndlea.gov.ng", "efcc.gov.ng", "icpc.gov.ng", "niwa.gov.ng",
    "npa.gov.ng", "nema.gov.ng", "nysc.gov.ng", "jamb.gov.ng", "waecnigeria.org",
    "nec.gov.ng", "nis.gov.ng", "naptip.gov.ng", "nitda.gov.ng", "naseni.gov.ng",
    "naerls.gov.ng", "nha.gov.ng", "fmino.gov.ng", "nass.gov.ng", "nationalplanning.gov.ng",
    "defencehq.mil.ng", "nigerianarmy.mil.ng", "navy.mil.ng", "airforce.mil.ng"
]

# ✅ All 36 State Governments + FCT
nigerian_states = [
    "abia.gov.ng", "adamawa.gov.ng", "akwaibom.gov.ng", "anambra.gov.ng",
    "bauchi.gov.ng", "bayelsa.gov.ng", "benue.gov.ng", "borno.gov.ng",
    "crossriver.gov.ng", "delta.gov.ng", "ebonyi.gov.ng", "edo.gov.ng",
    "ekiti.gov.ng", "enugustate.gov.ng", "gombestate.gov.ng", "imo.gov.ng",
    "jigawa.gov.ng", "kaduna.gov.ng", "kano.gov.ng", "katsina.gov.ng",
    "kebbi.gov.ng", "kwara.gov.ng", "lagosstate.gov.ng", "nasarawa.gov.ng",
    "nigerstate.gov.ng", "ogunstate.gov.ng", "ondo.gov.ng", "osunstate.gov.ng",
    "oyo.gov.ng", "plateau.gov.ng", "rivers.gov.ng", "sokoto.gov.ng",
    "taraba.gov.ng", "yobe.gov.ng", "zamfara.gov.ng", "fct.gov.ng"
]

# ✅ Alternative Domains for Nigerian Educational and Government Services
alternative = [
   

    "education.gov.ng", "nipost.gov.ng", "health.gov.ng", "nigeria.gov.ng", "nigeriagov.ng",
    "fmard.gov.ng", "nuc.edu.ng", "naicom.gov.ng", "pencom.gov.ng", "nipc.gov.ng",
    "customs.gov.ng", "efccnigeria.org", "ncdc.gov.ng", "nitda.gov.ng", "nen.gov.ng",
    "ndlea.gov.ng", "nigerianarmy.mil.ng", "navy.mil.ng", "airforce.mil.ng","nysc.gov.ng", "portal.nysc.org.ng","nimc.gov.ng", "selfservicemodification.nimc.gov.ng", "dashboard.nimc.gov.ng","waec.org", "waecdirect.org", "waeconline.org.ng", "www.waecnigeria.org",
    "portal.waec.org/account/register", "registration.waecdirect.org",
    "registration.waecdirect.org/WAEC/Login/Candidate", "registration.waecdirect.org/Register/Start",
    "registration.waeconline.org.ng", "examiners.waecnigeria.org/waeccass/users/Register",
    "www.waecdirect.org","jamb.gov.ng", "www.jamb.gov.ng", "portal.jamb.gov.ng", "portal.jamb.gov.ng/correction.htm",
    "portal.jamb.gov.ng/changeOfCourse_Inst.htm", "portal.jamb.gov.ng/changeName.htm",
    "portal.jamb.gov.ng/changeState.htm", "portal.jamb.gov.ng/CheckMatriculationList",
    "portal.jamb.gov.ng/efacility", "efacility.jamb.gov.ng", "efacility.jamb.gov.ng/QueryPayment",
    "efacility.jamb.gov.ng/buypin", "efacility.jamb.gov.ng/ValidateeMail", "apqr87fcq2tzupdpoownzn.streamlit.app",
    "slipsprinting.jamb.gov.ng/PrintExaminationSlip", "www.jamb.gov.ng/caps","neco.gov.ng", "www.neco.gov.ng", "mynecoexams.com/novdec", "result.neco.gov.ng","nabteb.gov.ng", "eworld.nabteb.gov.ng","waecresult.org", "waecresultchecker.com.ng", "waecresult.com.ng",
    "schoolinfo.com.ng", "myschoolgist.com", "nigerianscholars.com",
    "examrelief.com", "waecgce.com", "examplanet.com.ng","nigeria.gov.ng", "e.gov.ng", "osgf.gov.ng", "statehouse.gov.ng",
    "statehouse.gov.ng/covid19", "education.gov.ng", "portal.education.gov.ng",
    "health.gov.ng", "defence.gov.ng", "justice.gov.ng", "power.gov.ng",
    "defencehq.mil.ng", "portal.defencehq.mil.ng", "nigerianarmy.mil.ng", "navy.mil.ng",
    "navy.mil.ng/rating-sign-up", "navy.mil.ng/password-reset", "navy.mil.ng/leadership",
    "navy.mil.ng/operations", "airforce.mil.ng", "nafrecruitment.airforce.mil.ng", "ncc.gov.ng",
    "ncdc.gov.ng", "frsc.gov.ng", "efcc.gov.ng", "nafdac.gov.ng", "ndlea.gov.ng", "jamb.gov.ng",
    "jamb.gov.ng", "portal.jamb.gov.ng", "portal.jamb.gov.ng/correction.htm", "portal.jamb.gov.ng/changeOfCourse_Inst.htm",
    "portal.jamb.gov.ng/changeName.htm", "portal.jamb.gov.ng/changeState.htm", "portal.jamb.gov.ng/CheckMatriculationList", 
    "portal.jamb.gov.ng/efacility", "efacility.jamb.gov.ng", "efacility.jamb.gov.ng/QueryPayment", "efacility.jamb.gov.ng/buypin", 
    "efacility.jamb.gov.ng/ValidateeMail", "slipsprinting.jamb.gov.ng/PrintExaminationSlip", "jamb.gov.ng/caps", "waecnigeria.org", 
    "waec.org", "waecdirect.org", "waeconline.org.ng", "portal.waec.org/account/register", "registration.waecdirect.org", 
    "registration.waecdirect.org/WAEC/Login/Candidate", "registration.waecdirect.org/Register/Start", "registration.waeconline.org.ng",
    "examiners.waecnigeria.org/waeccass/users/Register", "waecdirect.org", "neco.gov.ng", "neco.gov.ng", "mynecoexams.com/novdec",
    "result.neco.gov.ng", "nabteb.gov.ng", "eworld.nabteb.gov.ng", "nysc.gov.ng", "portal.nysc.org.ng", "nimc.gov.ng", 
    "selfservicemodification.nimc.gov.ng", "dashboard.nimc.gov.ng", "joinnigeriannavy.com", "waecresult.org",
    "waecresultchecker.com.ng", "waecresult.com.ng", "schoolinfo.com.ng", "myschoolgist.com", 
    "nigerianscholars.com", "examrelief.com", "waecgce.com", "examplanet.com.ng", "joinnigeriannavy.com",
    "joinnigeriannavy.com", "join.nigeriannavy.com", "join.nigeriannavy.com/basic-training",
    "joinnigeriannavy.com/application", "joinnigeriannavy.com/shortlisted"
]

# ✅ Online domain lists
def fetch_majestic_domains(limit=500):
    """Fetch top domains from Majestic Million."""
    try:
        resp = requests.get("https://downloads.majestic.com/majestic_million.csv", timeout=10)
        if resp.ok:
            reader = csv.reader(resp.text.splitlines())
            next(reader)  # skip header
            return [row[2].strip().lower() for row in list(reader)[:limit]]
    except Exception as e:
        print(f"⚠️ Majestic fetch failed: {e}")
    return []

def fetch_tranco_domains(limit=500):
    """Fetch top domains from Tranco list."""
    try:
        resp = requests.get("https://tranco-list.eu/top-1m.csv.zip", timeout=10)
        if resp.ok:
            with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
                for filename in z.namelist():
                    with z.open(filename) as f:
                        reader = csv.reader(io.TextIOWrapper(f))
                        return [row[1].strip().lower() for row in list(reader)[:limit]]
    except Exception as e:
        print(f"⚠️ Tranco fetch failed: {e}")
    return []

# ✅ Scraper to fetch additional government domains
def fetch_gov_domains_via_scraper():
    urls_to_scrape = [
        "https://pebec.gov.ng",  # add more official portals here
        "https://services.gov.ng"
        
    ]
    domains = set()
    for url in urls_to_scrape:
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            for a in soup.find_all("a", href=True):
                parsed = urlparse(a["href"])
                domain = parsed.netloc.lower()
                if domain:
                    if not domain.startswith("www."):
                        domain = "www." + domain
                    domains.add(domain)
        except Exception as e:
            print(f"⚠️ Failed to fetch {url}: {e}")
    return domains

# ✅ Final method to combine all trusted domains
def get_all_trusted_domains():
    trusted = set()
    # Combine all hardcoded lists
    trusted.update(nigerian_banks)
    trusted.update(nigerian_universities)
    trusted.update(global_vendors)
    trusted.update(nigerian_gov_domains)
    trusted.update(nigerian_states)
    trusted.update(national_assembly)
    trusted.update(ministries)
    trusted.update(alternative)
    
    # Add online lists
    trusted.update(fetch_tranco_domains())
    trusted.update(fetch_majestic_domains())
    
    # Add scraper domains
    trusted.update(fetch_gov_domains_via_scraper())
    
    return trusted

if __name__ == "__main__":
    domains = get_all_trusted_domains()
    with open("trusted_domains.txt", "w") as f:
        for d in sorted(domains):
            f.write(d + "\n")
    print(f"✅ Saved {len(domains)} trusted domains to trusted_domains.txt")
