"""
generateLink():
Generate link to site to be scraped given the site, departure location, arrival location, departure location and departure date

TODO:
Kayak
Trivago
TripAdvisor
Travelocity

scrape():
get data from site given site specification and url link
"""

SITES = ("kayak", "trivago", "travelocity", "tripadvisor")

def generateLink(site, departFrom, arriveAt, departureDate):
    """
    params:
    site: str -> specifies which site is being scraped, allows for determination of how link is generated
    
    departFrom: str -> specifies airport to depart from
    arriveAt  : str -> specifies airport to arrive at
    departureDate: str in yyyy-mm-dd format -> specifies date of departure

    returns:
    str -> link to specified site with given information, sorted by price
    """
    try: 
        assert site in SITES
    except:
        #TODO: Implement error catching
        pass
    else:
        if site == SITES[0]:
            # Kayak
            pass
        elif site == SITES[1]:
            # trivago
            pass
        elif site == SITES[2]:
            # travelocity
            pass
        elif site == SITES[3]:
            # tripadvisor
            pass

def scrape(site, url):
    pass

