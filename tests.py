from bs4 import BeautifulSoup
from feed_to_csv import should_include_listing, parse_listing


def test_listings_that_dont_belong():
    """
    Listings should be excluded if they have the wrong year,
    or if 'and' is not in the Description
    """
    PAST_DATE = {
        'Appliances': '',
        'Bathrooms': u'',
        'Bedrooms': u'0',
        'DateListed': u'2014-10-03 00:00:00',
        'Description': u'Enjoy amazing ocean and island views from this 10+ acre parcel situated in a convenient and peaceful area of the Santa Monica mountains. Just minutes from beaches or the 101, Castro Peak is located off of Latigo canyon in an area sprinkled with vineyards, ranches and horse properties. A paved road leads you to the site which features considerable useable land and multiple development areas. This is an area of new development. Build your dream.',
        'MlsId': u'14799273',
        'MlsName': u'CLAW',
        'Price': u'535000.00',
        'Rooms': '',
        'StreetAddress': u'0 Castro Peak Mountainway'
    }

    FUTURE_DATE = {
        'Appliances': '',
        'Bathrooms': u'',
        'Bedrooms': u'0',
        'DateListed': u'2019-10-03 00:00:00',
        'Description': u'Enjoy amazing ocean and island views from this 10+ acre parcel situated in a convenient and peaceful area of the Santa Monica mountains. Just minutes from beaches or the 101, Castro Peak is located off of Latigo canyon in an area sprinkled with vineyards, ranches and horse properties. A paved road leads you to the site which features considerable useable land and multiple development areas. This is an area of new development. Build your dream.',
        'MlsId': u'14799273',
        'MlsName': u'CLAW',
        'Price': u'535000.00',
        'Rooms': '',
        'StreetAddress': u'0 Castro Peak Mountainway'
    }


    MISSING_AND_IN_DESC = {
        'Appliances': u'Built-Ins,Range Hood,Microwave,RangeOven',
        'Bathrooms': u'',
        'Bedrooms': u'3',
        'DateListed': u'2016-03-03 00:00:00',
        'Description': u'A STUNNING Architectural beautifully designed with pillowed stone floors, hand rubbed Venetian plaster walls, 11 ft ceilings filled with natural light, theatrical mood lighting, 3 fireplaces, two huge ocean front decks - and the always sandy beach just about 13 minutes from Santa Monica. The Great Room has extensive seating, exquisite art, 2 huge antique barn doors as backdrop for the 65" LED Smart TV (with 3D, wifi, surround sound) and is open to the European kitchen with service for 24. There are 2 Master Suites: one with private deck, steam shower, spa tub (all ocean front) & huge WIC , the 2nd Master has private entry, kitchenette, large sitting room and spa bath. The 3rd guest suite is as elegant and peaceful. Beautifully furnished with flat screens throughout, AC, 3 car garage and a guaranteed feeling of Serenity. June $30,000; Summer (July, Aug, Sept) at $45,000/mo.'.replace(' and ', ''),
        'MlsId': u'15883387',
        'MlsName': u'CLAW',
        'Price': u'23500.00',
        'Rooms': u'bedrooms,bathrooms',
        'StreetAddress': u'21310 PACIFIC COAST HWY'
    }

    assert not should_include_listing(PAST_DATE)
    assert not should_include_listing(FUTURE_DATE)
    assert not should_include_listing(MISSING_AND_IN_DESC)

def test_listings_that_do_belong():
    CORRECT_DATE_WITH_AND = {
        'Appliances': '',
         'Bathrooms': u'',
         'Bedrooms': u'0',
         'DateListed': u'2016-02-11 00:00:00',
         'Description': u'Beautiful ocean and coastline views from this private lot situated off of PCH. Amazing views of the Point Dume cliffs with the opportunity to enjoy incredible sunsets without a long drive up a canyon. Also, being the last house on the street ensures maximum privacy. Currently there is an active Coastal Development Permit for development of a 7,366 square foot residence and pool. This is a fantastic opportunity to build a large custom estate in Malibu that is centrally located, close to the beach with deeded beach rights. So much hard work has been done!',
         'MlsId': u'15965091',
         'MlsName': u'CLAW',
         'Price': u'2988000.00',
         'Rooms': '',
         'StreetAddress': u'27061 SEA VISTA DR'
    }

    CORRECT_DATE_WITH_UPPERCASE_AND = {
        'Appliances': '',
         'Bathrooms': u'',
         'Bedrooms': u'0',
         'DateListed': u'2016-12-11 00:00:00',
         'Description': u'Beautiful ocean AND coastline views from this private lot situated off of PCH. Amazing views of the Point Dume cliffs with the opportunity to enjoy incredible sunsets without a long drive up a canyon. Also, being the last house on the street ensures maximum privacy. Currently there is an active Coastal Development Permit for development of a 7,366 square foot residence AND pool. This is a fantastic opportunity to build a large custom estate in Malibu that is centrally located, close to the beach with deeded beach rights. So much hard work has been done!',
         'MlsId': u'15965091',
         'MlsName': u'CLAW',
         'Price': u'2988000.00',
         'Rooms': '',
         'StreetAddress': u'27061 SEA VISTA DR'
    }

    assert should_include_listing(CORRECT_DATE_WITH_AND)
    assert should_include_listing(CORRECT_DATE_WITH_UPPERCASE_AND)

MULTIPLE_ROOMS_MULTIPLE_APPLIANCES = '''<Listing><Location><StreetAddress>23826 MALIBU RD</StreetAddress><UnitNumber/><City>Malibu</City><State>CA</State><Zip>90265</Zip><ParcelID/><Lat>34.03283</Lat><Long>-118.69457</Long><County/><StreetIntersection/><DisplayAddress>Yes</DisplayAddress></Location><ListingDetails><Status>For Rent</Status><Price>72500.00</Price><ListingUrl>http://www.thepartnerstrust.com/property/42923211/syn/43/</ListingUrl><MlsId>15888095</MlsId><MlsName>CLAW</MlsName><ProviderListingId>42923211</ProviderListingId><DateListed>2015-03-18 00:00:00</DateListed><VirtualTourUrl>http://www.thepartnerstrust.com/property/42923211/syn/43/</VirtualTourUrl><ListingEmail>zillow-41@leadrelay.com</ListingEmail><AlwaysEmailAgent>0</AlwaysEmailAgent><ShortSale/><REO/></ListingDetails><RentalDetails><Availability/><LeaseTerm/><DepositFees/><UtilitiesIncluded><Water/><Sewage/><Garbage/><Electricity/><Gas/><Internet/><Cable/><SatTV/></UtilitiesIncluded><PetsAllowed><NoPets/><Cats/><SmallDogs/><LargeDogs/></PetsAllowed></RentalDetails><BasicDetails><PropertyType>Apartment</PropertyType><Title>23826 MALIBU RD</Title><Description>July &amp; August not available. "Captured in Paradise." Arguably on the most desired sandy beach of Malibu, this home-away-from-home offers a sophisticated zen ambiance &amp; elegance at the beach. This private escape has a gated courtyard entry, which leads to an open dining/kitchen/living area, all stepping out to the private backyard with spa and expansive tanning deck. Inside are 4 bedrooms and 4.5 bathrooms, including a luxurious master suite. Complete with detached guest home and media room, this one-of-a-kind property was tastefully designed. Only a short jaunt to Malibu's finest shops, restaurants, and famous surf breaks, this rare offering is the perfect spot from which to enjoy Malibu's sunrises and sunsets. Available for long term furnished lease for $72,500/month</Description><Bedrooms>5</Bedrooms><Bathrooms/><FullBathrooms>4</FullBathrooms><HalfBathrooms>1</HalfBathrooms><ThreeQuarterBathrooms/><LivingArea>3009</LivingArea><LotSize>0.34</LotSize><year-built>1975</year-built></BasicDetails><Pictures><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/0/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/1/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/2/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/3/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/4/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/5/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/6/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/7/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/8/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/9/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/10/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/11/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/12/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/13/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/14/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/15/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/16/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/17/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/18/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/19/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/20/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/21/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/22/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/23/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/24/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/25/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/26/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/27/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/28/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/29/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/30/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/31/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/32/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/33/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/34/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/35/v70/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42923211/36/v70/</PictureUrl><Caption/></Picture></Pictures><Agent><FirstName>Madison</FirstName><LastName>Hildebrand</LastName><EmailAddress>madison@themalibulife.com</EmailAddress><PictureUrl>http://media.thepartnerstrust.com/pics/realtor/659891/107176/</PictureUrl><OfficeLineNumber>310-818-5788</OfficeLineNumber><MobilePhoneLineNumber>310-818-5788</MobilePhoneLineNumber><FaxLineNumber/></Agent><Office><BrokerageName>Partners Trust</BrokerageName><BrokerPhone>310-858-6800</BrokerPhone><BrokerEmail>inquire@thepartnerstrust.com</BrokerEmail><BrokerWebsite>http://www.thepartnerstrust.com/</BrokerWebsite><StreetAddress>23410 Civic Center Way, C1</StreetAddress><UnitNumber/><City>Malibu</City><State>CA</State><Zip>90265</Zip><OfficeName>Malibu</OfficeName><FranchiseName>Partners Trust</FranchiseName></Office><OpenHouses><OpenHouse/></OpenHouses><Fees><Fee><FeeType/><FeeAmount/><FeePeriod>Monthly</FeePeriod></Fee></Fees><Neighborhood><Name/><Description/></Neighborhood><RichDetails><AdditionalFeatures/><Appliances><Appliance>Built-Ins</Appliance><Appliance>Range Hood</Appliance><Appliance>Microwave</Appliance><Appliance>RangeOven</Appliance></Appliances><ArchitectureStyle>Traditional</ArchitectureStyle><Attic/><BarbecueArea/><Basement/><BuildingUnitCount/><CableReady/><CeilingFan/><CondoFloorNum/><CoolingSystems><CoolingSystem>Central</CoolingSystem></CoolingSystems><Deck/><DisabledAccess/><Dock/><Doorman/><DoublePaneWindows/><Elevator>No</Elevator><ExteriorTypes><ExteriorType/></ExteriorTypes><Fireplace/><FloorCoverings><FloorCovering/></FloorCoverings><Garden/><Gated/><Greenhouse/><HeatingFuels><HeatingFuel>Central Furnace</HeatingFuel></HeatingFuels><HottubSpa/><Intercom/><JettedBathTub>No</JettedBathTub><Lawn/><LegalDescription/><MotherInLaw/><NumFloors/><NumParkingSpaces/><ParkingTypes><ParkingType/></ParkingTypes><Patio/><Pond/><Pool/><Porch/><RoofTypes><RoofType/></RoofTypes><RoomCount>2</RoomCount><Rooms><Room>bedrooms</Room><Room>bathrooms</Room></Rooms><RvParking/><Sauna/><SecuritySystem>No</SecuritySystem><Skylight/><SportsCourt/><SprinkerSystem/><VaultedCeiling/><ViewTypes><ViewType/></ViewTypes><Waterfront/><Wetbar/><WhatOwnerLoves/><Wired/><YearUpdated/><FitnessCenter/><BasketballCourt/><TennisCourt/><NearTransportation/><ControlledAccess/><Over55ActiveCommunity/><AssistedLivingCommunity/><Storage/><FencedYard/><PropertyName/><Furnished/><HighspeedInternet/><OnsiteLaundry/><CableSatTV/><Taxes><Tax><TaxYear/><TaxAmount/></Tax></Taxes><NewConstruction/></RichDetails></Listing>'''

def test_multiple_rooms_comma_joined():
    listing_dict = parse_listing(BeautifulSoup(MULTIPLE_ROOMS_MULTIPLE_APPLIANCES, 'xml'))
    assert listing_dict['Rooms'] == 'bedrooms,bathrooms'

def test_multiple_appliances_comma_joined():
    listing_dict = parse_listing(BeautifulSoup(MULTIPLE_ROOMS_MULTIPLE_APPLIANCES, 'xml'))
    assert listing_dict['Appliances'] == 'Built-Ins,Range Hood,Microwave,RangeOven'

def test_empty_appliances_produces_empty_string():
    EMPTY_APPLIANCES = '''<Listing><Location><StreetAddress>0 SADDLE PEAK RD</StreetAddress><UnitNumber/><City>Malibu</City><State>CA</State><Zip>90290</Zip><ParcelID/><Lat>34.077269</Lat><Long>-118.614425</Long><County/><StreetIntersection/><DisplayAddress>Yes</DisplayAddress></Location><ListingDetails><Status>Active</Status><Price>200000.00</Price><ListingUrl>http://www.thepartnerstrust.com/property/42922064/syn/43/</ListingUrl><MlsId>14802845</MlsId><MlsName>CLAW</MlsName><ProviderListingId>42922064</ProviderListingId><DateListed>2014-10-17 00:00:00</DateListed><VirtualTourUrl>http://www.thepartnerstrust.com/property/42922064/syn/43/</VirtualTourUrl><ListingEmail>zillow-41@leadrelay.com</ListingEmail><AlwaysEmailAgent>0</AlwaysEmailAgent><ShortSale/><REO/></ListingDetails><RentalDetails><Availability/><LeaseTerm/><DepositFees/><UtilitiesIncluded><Water/><Sewage/><Garbage/><Electricity/><Gas/><Internet/><Cable/><SatTV/></UtilitiesIncluded><PetsAllowed><NoPets/><Cats/><SmallDogs/><LargeDogs/></PetsAllowed></RentalDetails><BasicDetails><PropertyType>VacantLand</PropertyType><Title>0 SADDLE PEAK RD</Title><Description>Spectacular views from this 4+ acre property perched on the ridge between PCH and the Valley. Two APNs - 4438-034-037 and 031 being sold together. Plus, there is a lot next door for sale too! A, paved private road leads you almost to the site. This lot has development challenges - not for the faint of heart. Property has been owned by the same family for over 40 years. Reports and information is limited.</Description><Bedrooms>0</Bedrooms><Bathrooms/><FullBathrooms/><HalfBathrooms/><ThreeQuarterBathrooms/><LivingArea/><LotSize>4.2</LotSize><year-built/></BasicDetails><Pictures><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42922064/0/v7/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42922064/1/v7/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42922064/2/v7/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42922064/3/v7/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42922064/4/v7/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42922064/5/v7/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42922064/6/v7/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42922064/7/v7/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42922064/8/v7/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42922064/9/v7/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42922064/10/v7/</PictureUrl><Caption/></Picture><Picture><PictureUrl>http://media.thepartnerstrust.com/pics/property/42922064/11/v7/</PictureUrl><Caption/></Picture></Pictures><Agent><FirstName>Madison</FirstName><LastName>Hildebrand</LastName><EmailAddress>madison@themalibulife.com</EmailAddress><PictureUrl>http://media.thepartnerstrust.com/pics/realtor/659891/107176/</PictureUrl><OfficeLineNumber>310-818-5788</OfficeLineNumber><MobilePhoneLineNumber>310-818-5788</MobilePhoneLineNumber><FaxLineNumber/></Agent><Office><BrokerageName>Partners Trust</BrokerageName><BrokerPhone>310-858-6800</BrokerPhone><BrokerEmail>inquire@thepartnerstrust.com</BrokerEmail><BrokerWebsite>http://www.thepartnerstrust.com/</BrokerWebsite><StreetAddress>23410 Civic Center Way, C1</StreetAddress><UnitNumber/><City>Malibu</City><State>CA</State><Zip>90265</Zip><OfficeName>Malibu</OfficeName><FranchiseName>Partners Trust</FranchiseName></Office><OpenHouses><OpenHouse/></OpenHouses><Fees><Fee><FeeType/><FeeAmount/><FeePeriod>Monthly</FeePeriod></Fee></Fees><Neighborhood><Name/><Description/></Neighborhood><RichDetails><AdditionalFeatures/><Appliances/><ArchitectureStyle/><Attic/><BarbecueArea/><Basement/><BuildingUnitCount/><CableReady/><CeilingFan/><CondoFloorNum/><CoolingSystems><CoolingSystem/></CoolingSystems><Deck/><DisabledAccess/><Dock/><Doorman/><DoublePaneWindows/><Elevator>No</Elevator><ExteriorTypes><ExteriorType/></ExteriorTypes><Fireplace/><FloorCoverings><FloorCovering/></FloorCoverings><Garden/><Gated/><Greenhouse/><HeatingFuels><HeatingFuel/></HeatingFuels><HottubSpa/><Intercom/><JettedBathTub>No</JettedBathTub><Lawn/><LegalDescription/><MotherInLaw/><NumFloors/><NumParkingSpaces/><ParkingTypes><ParkingType/></ParkingTypes><Patio/><Pond/><Pool/><Porch/><RoofTypes><RoofType/></RoofTypes><RoomCount>0</RoomCount><RvParking/><Sauna/><SecuritySystem>No</SecuritySystem><Skylight/><SportsCourt/><SprinkerSystem/><VaultedCeiling/><ViewTypes><ViewType/></ViewTypes><Waterfront/><Wetbar/><WhatOwnerLoves/><Wired/><YearUpdated/><FitnessCenter/><BasketballCourt/><TennisCourt/><NearTransportation/><ControlledAccess/><Over55ActiveCommunity/><AssistedLivingCommunity/><Storage/><FencedYard/><PropertyName/><Furnished/><HighspeedInternet/><OnsiteLaundry/><CableSatTV/><Taxes><Tax><TaxYear/><TaxAmount/></Tax></Taxes><NewConstruction/></RichDetails></Listing>'''

    listing_dict = parse_listing(BeautifulSoup(EMPTY_APPLIANCES, 'xml'))
    assert listing_dict['Appliances'] == ''

if __name__ == '__main__':
    import nose
    nose.run()
