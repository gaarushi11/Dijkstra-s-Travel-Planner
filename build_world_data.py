# build_world_data.py
import csv
import math

print(">> Starting Global Multi-Modal Dataset Generation...")

# 1. Geographic Node Clusters (Top Regional Cities)
regional_nodes = {
    "USA": [
        ("New York", 40.7128, -74.0060), ("Los Angeles", 34.0522, -118.2437),
        ("Chicago", 41.8781, -87.6298), ("Houston", 29.7604, -95.3698),
        ("Phoenix", 33.4484, -112.0740), ("Philadelphia", 39.9526, -75.1652),
        ("San Antonio", 29.4241, -98.4936), ("San Diego", 32.7157, -117.1611),
        ("Dallas", 32.7767, -96.7970), ("San Jose", 37.3382, -121.8863),
        ("Austin", 30.2672, -97.7431), ("Jacksonville", 30.3322, -81.6557),
        ("Fort Worth", 32.7555, -97.3308), ("Columbus", 39.9612, -82.9988),
        ("Charlotte", 35.2271, -80.8431), ("San Francisco", 37.7749, -122.4194),
        ("Indianapolis", 39.7684, -86.1581), ("Seattle", 47.6062, -122.3321),
        ("Denver", 39.7392, -104.9903), ("Washington DC", 38.8951, -77.0364),
        ("Boston", 42.3601, -71.0589), ("El Paso", 31.7619, -106.4850),
        ("Nashville", 36.1627, -86.7816), ("Detroit", 42.3314, -83.0458),
        ("Oklahoma City", 35.4676, -97.5164), ("Portland", 45.5152, -122.6784),
        ("Las Vegas", 36.1716, -115.1391), ("Memphis", 35.1495, -90.0490)
    ],
    "India": [
        ("Mumbai", 19.0760, 72.8777), ("Delhi", 28.7041, 77.1025),
        ("Bangalore", 12.9716, 77.5946), ("Hyderabad", 17.3850, 78.4867),
        ("Ahmedabad", 23.0225, 72.5714), ("Chennai", 13.0827, 80.2707),
        ("Kolkata", 22.5726, 88.3639), ("Surat", 21.1702, 72.8311),
        ("Pune", 18.5204, 73.8567), ("Jaipur", 26.9124, 75.7873),
        ("Lucknow", 26.8467, 80.9462), ("Kanpur", 26.4499, 80.3319),
        ("Nagpur", 21.1458, 79.0882), ("Indore", 22.7196, 75.8577),
        ("Thane", 19.2183, 72.9781), ("Bhopal", 23.2599, 77.4126),
        ("Visakhapatnam", 17.6868, 83.2185), ("Patna", 25.5941, 85.1376),
        ("Vadodara", 22.3072, 73.1812), ("Ghaziabad", 28.6692, 77.4538),
        ("Ludhiana", 30.9010, 75.8573), ("Agra", 27.1767, 78.0081),
        ("Nashik", 19.9975, 73.7898), ("Faridabad", 28.4089, 77.3178)
    ],
    "Europe": [
        ("Paris", 48.8566, 2.3522), ("London", 51.5074, -0.1278),
        ("Berlin", 52.5200, 13.4050), ("Madrid", 40.4167, -3.7492),
        ("Rome", 41.9028, 12.4964), ("Bucharest", 44.4268, 26.1025),
        ("Vienna", 48.2082, 16.3738), ("Hamburg", 53.5511, 9.9937),
        ("Budapest", 47.4979, 19.0402), ("Warsaw", 52.2297, 21.0122),
        ("Barcelona", 41.3851, 2.1734), ("Munich", 48.1351, 11.5820),
        ("Milan", 45.4642, 9.1900), ("Prague", 50.0755, 14.4378),
        ("Sofia", 42.6977, 23.3219), ("Brussels", 50.8503, 4.3517),
        ("Birmingham", 52.4862, -1.8904), ("Manchester", 53.4808, -2.2426),
        ("Cologne", 50.9375, 6.9603), ("Amsterdam", 52.3676, 4.9041),
        ("Frankfurt", 50.1109, 8.6821), ("Lyon", 45.7500, 4.8500)
    ],
    "Canada": [
        ("Toronto", 43.6532, -79.3832), ("Montreal", 45.5017, -73.5673),
        ("Vancouver", 49.2827, -123.1207), ("Calgary", 51.0447, -114.0719),
        ("Edmonton", 53.5461, -113.4938), ("Ottawa", 45.4215, -75.6972),
        ("Winnipeg", 49.8951, -97.1384), ("Quebec City", 46.8139, -71.2080),
        ("Hamilton", 43.2557, -79.8711), ("Halifax", 44.6488, -63.5752)
    ],
    "East Asia": [
        ("Tokyo", 35.6762, 139.6503), ("Osaka", 34.6937, 135.5023),
        ("Seoul", 37.5665, 126.9780), ("Busan", 35.1796, 129.0756),
        ("Beijing", 39.9042, 116.4074), ("Shanghai", 31.2304, 121.4737),
        ("Guangzhou", 23.1291, 113.2644), ("Shenzhen", 22.5431, 114.0579),
        ("Hong Kong", 22.3193, 114.1694), ("Taipei", 25.0330, 121.5654)
    ],
    "Southeast Asia": [
        ("Singapore", 1.3521, 103.8198), ("Bangkok", 13.7563, 100.5018),
        ("Kuala Lumpur", 3.1390, 101.6869), ("Jakarta", -6.2088, 106.8456),
        ("Manila", 14.5995, 120.9842), ("Ho Chi Minh City", 10.8231, 106.6297),
        ("Hanoi", 21.0278, 105.8342), ("Phnom Penh", 11.5564, 104.9282),
        ("Yangon", 16.8409, 96.1735), ("Denpasar", -8.6705, 115.2126)
    ],
    "Middle East": [
        ("Dubai", 25.2048, 55.2708), ("Abu Dhabi", 24.4539, 54.3773),
        ("Doha", 25.2854, 51.5310), ("Riyadh", 24.7136, 46.6753),
        ("Jeddah", 21.4858, 39.1925), ("Kuwait City", 29.3759, 47.9774),
        ("Muscat", 23.5880, 58.3829), ("Tel Aviv", 32.0853, 34.7818),
        ("Amman", 31.9539, 35.9106), ("Istanbul", 41.0082, 28.9784)
    ],
    "Australia": [
        ("Sydney", -33.8688, 151.2093), ("Melbourne", -37.8136, 144.9631),
        ("Brisbane", -27.4698, 153.0251), ("Perth", -31.9523, 115.8613),
        ("Adelaide", -34.9285, 138.6007), ("Canberra", -35.2809, 149.1300),
        ("Hobart", -42.8821, 147.3272), ("Darwin", -12.4634, 130.8456),
        ("Gold Coast", -28.0167, 153.4000), ("Cairns", -16.9186, 145.7781)
    ],
    "South America": [
        ("Sao Paulo", -23.5558, -46.6396), ("Rio de Janeiro", -22.9068, -43.1729),
        ("Buenos Aires", -34.6037, -58.3816), ("Santiago", -33.4489, -70.6693),
        ("Lima", -12.0464, -77.0428), ("Bogota", 4.7110, -74.0721),
        ("Medellin", 6.2442, -75.5812), ("Quito", -0.1807, -78.4678),
        ("Montevideo", -34.9011, -56.1645), ("La Paz", -16.4897, -68.1193)
    ],
    "Africa": [
        ("Cairo", 30.0444, 31.2357), ("Lagos", 6.5244, 3.3792),
        ("Johannesburg", -26.2041, 28.0473), ("Cape Town", -33.9249, 18.4241),
        ("Nairobi", -1.2921, 36.8219), ("Casablanca", 33.5731, -7.5898),
        ("Addis Ababa", 8.9806, 38.7578), ("Accra", 5.6037, -0.1870),
        ("Tunis", 36.8065, 10.1815), ("Dakar", 14.7167, -17.4677)
    ]
}

def add_unique_nodes(region, additions):
    existing = {city for city, _, _ in regional_nodes.setdefault(region, [])}
    for city in additions:
        if city[0] not in existing:
            regional_nodes[region].append(city)
            existing.add(city[0])

# Extra coverage: at least one representative city for each state/province/territory
# in the federal countries already emphasized by the dataset, plus Mexico.
add_unique_nodes("USA", [
    ("Birmingham AL", 33.5186, -86.8104), ("Anchorage", 61.2181, -149.9003),
    ("Little Rock", 34.7465, -92.2896), ("Hartford", 41.7658, -72.6734),
    ("Dover", 39.1582, -75.5244), ("Miami", 25.7617, -80.1918),
    ("Atlanta", 33.7490, -84.3880), ("Honolulu", 21.3099, -157.8581),
    ("Boise", 43.6150, -116.2023), ("Louisville", 38.2527, -85.7585),
    ("New Orleans", 29.9511, -90.0715), ("Portland ME", 43.6591, -70.2568),
    ("Baltimore", 39.2904, -76.6122), ("Minneapolis", 44.9778, -93.2650),
    ("Jackson MS", 32.2988, -90.1848), ("Kansas City", 39.0997, -94.5786),
    ("Billings", 45.7833, -108.5007), ("Omaha", 41.2565, -95.9345),
    ("Manchester NH", 42.9956, -71.4548), ("Newark", 40.7357, -74.1724),
    ("Albuquerque", 35.0844, -106.6504), ("Raleigh", 35.7796, -78.6382),
    ("Fargo", 46.8772, -96.7898), ("Cleveland", 41.4993, -81.6944),
    ("Tulsa", 36.1540, -95.9928), ("Providence", 41.8240, -71.4128),
    ("Charleston SC", 32.7765, -79.9311), ("Sioux Falls", 43.5446, -96.7311),
    ("Knoxville", 35.9606, -83.9207), ("Salt Lake City", 40.7608, -111.8910),
    ("Burlington", 44.4759, -73.2121), ("Richmond", 37.5407, -77.4360),
    ("Charleston WV", 38.3498, -81.6326), ("Milwaukee", 43.0389, -87.9065),
    ("Cheyenne", 41.1400, -104.8202)
])

add_unique_nodes("India", [
    ("Amaravati", 16.5062, 80.6480), ("Itanagar", 27.0844, 93.6053),
    ("Guwahati", 26.1445, 91.7362), ("Raipur", 21.2514, 81.6296),
    ("Panaji", 15.4909, 73.8278), ("Gandhinagar", 23.2156, 72.6369),
    ("Chandigarh", 30.7333, 76.7794), ("Shimla", 31.1048, 77.1734),
    ("Ranchi", 23.3441, 85.3096), ("Thiruvananthapuram", 8.5241, 76.9366),
    ("Shillong", 25.5788, 91.8933), ("Aizawl", 23.7271, 92.7176),
    ("Kohima", 25.6751, 94.1086), ("Bhubaneswar", 20.2961, 85.8245),
    ("Gangtok", 27.3389, 88.6065), ("Agartala", 23.8315, 91.2868),
    ("Dehradun", 30.3165, 78.0322), ("Port Blair", 11.6234, 92.7265),
    ("Daman", 20.3974, 72.8328), ("Srinagar", 34.0837, 74.7973),
    ("Leh", 34.1526, 77.5771), ("Kavaratti", 10.5593, 72.6358),
    ("Puducherry", 11.9416, 79.8083), ("Imphal", 24.8170, 93.9368)
])

add_unique_nodes("Canada", [
    ("St Johns", 47.5615, -52.7126), ("Charlottetown", 46.2382, -63.1311),
    ("Fredericton", 45.9636, -66.6431), ("Regina", 50.4452, -104.6189),
    ("Whitehorse", 60.7212, -135.0568), ("Yellowknife", 62.4540, -114.3718),
    ("Iqaluit", 63.7467, -68.5170)
])

add_unique_nodes("Australia", [
    ("Newcastle AU", -32.9283, 151.7817), ("Wollongong", -34.4278, 150.8931),
    ("Geelong", -38.1499, 144.3617), ("Townsville", -19.2590, 146.8169),
    ("Alice Springs", -23.6980, 133.8807), ("Launceston", -41.4332, 147.1441)
])

add_unique_nodes("South America", [
    ("Brasilia", -15.7939, -47.8828), ("Salvador", -12.9777, -38.5016),
    ("Fortaleza", -3.7319, -38.5267), ("Belo Horizonte", -19.9167, -43.9345),
    ("Manaus", -3.1190, -60.0217), ("Curitiba", -25.4284, -49.2733),
    ("Recife", -8.0476, -34.8770), ("Porto Alegre", -30.0346, -51.2177),
    ("Belem", -1.4558, -48.4902), ("Goiania", -16.6869, -49.2648),
    ("Florianopolis", -27.5949, -48.5482), ("Vitoria", -20.3155, -40.3128),
    ("Campo Grande", -20.4697, -54.6201), ("Cuiaba", -15.6014, -56.0979),
    ("Natal", -5.7793, -35.2009), ("Joao Pessoa", -7.1195, -34.8450),
    ("Maceio", -9.6498, -35.7089), ("Aracaju", -10.9472, -37.0731),
    ("Teresina", -5.0892, -42.8019), ("Sao Luis", -2.5391, -44.2829),
    ("Palmas", -10.1840, -48.3336), ("Porto Velho", -8.7608, -63.8999),
    ("Rio Branco", -9.9747, -67.8243), ("Boa Vista", 2.8235, -60.6758),
    ("Macapa", 0.0356, -51.0705)
])

regional_nodes["Mexico"] = [
    ("Mexico City", 19.4326, -99.1332), ("Guadalajara", 20.6597, -103.3496),
    ("Monterrey", 25.6866, -100.3161), ("Puebla", 19.0414, -98.2063),
    ("Toluca", 19.2826, -99.6557), ("Queretaro", 20.5888, -100.3899),
    ("Merida", 20.9674, -89.5926), ("Cancun", 21.1619, -86.8515),
    ("Tijuana", 32.5149, -117.0382), ("Hermosillo", 29.0729, -110.9559),
    ("Chihuahua", 28.6353, -106.0889), ("Saltillo", 25.4232, -101.0053),
    ("Durango MX", 24.0277, -104.6532), ("Zacatecas", 22.7709, -102.5832),
    ("Aguascalientes", 21.8853, -102.2916), ("San Luis Potosi", 22.1565, -100.9855),
    ("Guanajuato", 21.0190, -101.2574), ("Morelia", 19.7059, -101.1949),
    ("Colima", 19.2452, -103.7241), ("Tepic", 21.5042, -104.8946),
    ("Culiacan", 24.8091, -107.3940), ("La Paz MX", 24.1426, -110.3128),
    ("Villahermosa", 17.9895, -92.9475), ("Tuxtla Gutierrez", 16.7569, -93.1292),
    ("Oaxaca", 17.0732, -96.7266), ("Chilpancingo", 17.5515, -99.5006),
    ("Cuernavaca", 18.9242, -99.2216), ("Tlaxcala", 19.3182, -98.2375),
    ("Pachuca", 20.1011, -98.7591), ("Xalapa", 19.5438, -96.9102),
    ("Campeche", 19.8301, -90.5349), ("Chetumal", 18.5001, -88.2961)
]

add_unique_nodes("Africa", [
    ("Alexandria", 31.2001, 29.9187), ("Giza", 30.0131, 31.2089),
    ("Algiers", 36.7538, 3.0588), ("Oran", 35.6971, -0.6308),
    ("Rabat", 34.0209, -6.8416), ("Marrakesh", 31.6295, -7.9811),
    ("Tripoli", 32.8872, 13.1913), ("Benghazi", 32.1167, 20.0667),
    ("Khartoum", 15.5007, 32.5599), ("Port Sudan", 19.6158, 37.2164),
    ("Kampala", 0.3476, 32.5825), ("Kigali", -1.9441, 30.0619),
    ("Bujumbura", -3.3614, 29.3599), ("Dar es Salaam", -6.7924, 39.2083),
    ("Mombasa", -4.0435, 39.6682), ("Mogadishu", 2.0469, 45.3182),
    ("Djibouti City", 11.5721, 43.1456), ("Asmara", 15.3229, 38.9251),
    ("Luanda", -8.8390, 13.2894), ("Kinshasa", -4.4419, 15.2663),
    ("Brazzaville", -4.2634, 15.2429), ("Libreville", 0.4162, 9.4673),
    ("Douala", 4.0511, 9.7679), ("Yaounde", 3.8480, 11.5021),
    ("Abidjan", 5.3600, -4.0083), ("Yamoussoukro", 6.8276, -5.2893),
    ("Kumasi", 6.6666, -1.6163), ("Ibadan", 7.3775, 3.9470),
    ("Abuja", 9.0765, 7.3986), ("Kano", 12.0022, 8.5920),
    ("Bamako", 12.6392, -8.0029), ("Ouagadougou", 12.3714, -1.5197),
    ("Niamey", 13.5116, 2.1254), ("Conakry", 9.6412, -13.5784),
    ("Freetown", 8.4657, -13.2317), ("Monrovia", 6.3156, -10.8074),
    ("Banjul", 13.4549, -16.5790), ("Nouakchott", 18.0735, -15.9582),
    ("Windhoek", -22.5609, 17.0658), ("Gaborone", -24.6282, 25.9231),
    ("Lusaka", -15.3875, 28.3228), ("Harare", -17.8252, 31.0335),
    ("Maputo", -25.9692, 32.5732), ("Antananarivo", -18.8792, 47.5079),
    ("Port Louis", -20.1609, 57.5012), ("Victoria SC", -4.6191, 55.4513)
])

add_unique_nodes("Europe", [
    ("Dublin", 53.3498, -6.2603), ("Cork", 51.8985, -8.4756),
    ("Edinburgh", 55.9533, -3.1883), ("Glasgow", 55.8642, -4.2518),
    ("Cardiff", 51.4816, -3.1791), ("Belfast", 54.5973, -5.9301),
    ("Lisbon", 38.7223, -9.1393), ("Porto", 41.1579, -8.6291),
    ("Valencia", 39.4699, -0.3763), ("Seville", 37.3891, -5.9845),
    ("Marseille", 43.2965, 5.3698), ("Nice", 43.7102, 7.2620),
    ("Zurich", 47.3769, 8.5417), ("Geneva", 46.2044, 6.1432),
    ("Stockholm", 59.3293, 18.0686), ("Gothenburg", 57.7089, 11.9746),
    ("Oslo", 59.9139, 10.7522), ("Bergen", 60.3913, 5.3221),
    ("Copenhagen", 55.6761, 12.5683), ("Aarhus", 56.1629, 10.2039),
    ("Helsinki", 60.1699, 24.9384), ("Tallinn", 59.4370, 24.7536),
    ("Riga", 56.9496, 24.1052), ("Vilnius", 54.6872, 25.2797),
    ("Krakow", 50.0647, 19.9450), ("Wroclaw", 51.1079, 17.0385),
    ("Bratislava", 48.1486, 17.1077), ("Ljubljana", 46.0569, 14.5058),
    ("Zagreb", 45.8150, 15.9819), ("Belgrade", 44.7866, 20.4489),
    ("Sarajevo", 43.8563, 18.4131), ("Skopje", 41.9981, 21.4254),
    ("Tirana", 41.3275, 19.8187), ("Podgorica", 42.4304, 19.2594),
    ("Athens", 37.9838, 23.7275), ("Thessaloniki", 40.6401, 22.9444),
    ("Nicosia", 35.1856, 33.3823), ("Reykjavik", 64.1466, -21.9426),
    ("Kyiv", 50.4501, 30.5234), ("Lviv", 49.8397, 24.0297),
    ("Chisinau", 47.0105, 28.8638), ("Minsk", 53.9006, 27.5590)
])

add_unique_nodes("Europe", [
    ("Venice", 45.4408, 12.3155), ("The Hague", 52.0705, 4.3007),
    ("Rotterdam", 51.9244, 4.4777), ("Utrecht", 52.0907, 5.1214),
    ("Eindhoven", 51.4416, 5.4697), ("Antwerp", 51.2194, 4.4025),
    ("Ghent", 51.0543, 3.7174), ("Bruges", 51.2093, 3.2247),
    ("Luxembourg City", 49.6116, 6.1319), ("Monaco", 43.7384, 7.4246),
    ("San Marino", 43.9424, 12.4578), ("Vatican City", 41.9029, 12.4534),
    ("Florence", 43.7696, 11.2558), ("Naples", 40.8518, 14.2681),
    ("Turin", 45.0703, 7.6869), ("Bologna", 44.4949, 11.3426),
    ("Pisa", 43.7228, 10.4017), ("Verona", 45.4384, 10.9916),
    ("Palermo", 38.1157, 13.3615), ("Genoa", 44.4056, 8.9463),
    ("Bilbao", 43.2630, -2.9350), ("Granada", 37.1773, -3.5986),
    ("Malaga", 36.7213, -4.4214), ("Cordoba", 37.8882, -4.7794),
    ("Toledo", 39.8628, -4.0273), ("Salamanca", 40.9701, -5.6635),
    ("Montpellier", 43.6110, 3.8767), ("Toulouse", 43.6047, 1.4442),
    ("Bordeaux", 44.8378, -0.5792), ("Nantes", 47.2184, -1.5536),
    ("Strasbourg", 48.5734, 7.7521), ("Lille", 50.6292, 3.0573),
    ("Dresden", 51.0504, 13.7373), ("Leipzig", 51.3397, 12.3731),
    ("Dusseldorf", 51.2277, 6.7735), ("Stuttgart", 48.7758, 9.1829),
    ("Nuremberg", 49.4521, 11.0767), ("Bremen", 53.0793, 8.8017),
    ("Heidelberg", 49.3988, 8.6724), ("Salzburg", 47.8095, 13.0550),
    ("Innsbruck", 47.2692, 11.4041), ("Graz", 47.0707, 15.4395),
    ("Basel", 47.5596, 7.5886), ("Bern", 46.9480, 7.4474),
    ("Lausanne", 46.5197, 6.6323), ("Lucerne", 47.0502, 8.3093),
    ("Split", 43.5081, 16.4402), ("Dubrovnik", 42.6507, 18.0944),
    ("Mostar", 43.3438, 17.8078), ("Pristina", 42.6629, 21.1655),
    ("Varna", 43.2141, 27.9147), ("Plovdiv", 42.1354, 24.7453),
    ("Cluj-Napoca", 46.7712, 23.6236), ("Timisoara", 45.7489, 21.2087),
    ("Iasi", 47.1585, 27.6014), ("Odessa", 46.4825, 30.7233),
    ("Krakow", 50.0647, 19.9450), ("Gdansk", 54.3520, 18.6466),
    ("Poznan", 52.4064, 16.9252), ("Brno", 49.1951, 16.6068),
    ("Kosice", 48.7164, 21.2611), ("Malmo", 55.6050, 13.0038),
    ("Uppsala", 59.8586, 17.6389), ("Trondheim", 63.4305, 10.3951),
    ("Stavanger", 58.9700, 5.7331), ("Tromso", 69.6492, 18.9553),
    ("Odense", 55.4038, 10.4024), ("Turku", 60.4518, 22.2666),
    ("Tampere", 61.4978, 23.7610), ("Tartu", 58.3776, 26.7290)
])

add_unique_nodes("Africa", [
    ("Marrakech", 31.6295, -7.9811), ("Fez", 34.0181, -5.0078),
    ("Tangier", 35.7595, -5.8340), ("Luxor", 25.6872, 32.6396),
    ("Aswan", 24.0889, 32.8998), ("Sharm El Sheikh", 27.9158, 34.3299),
    ("Zanzibar City", -6.1659, 39.2026), ("Arusha", -3.3869, 36.6830),
    ("Mwanza", -2.5164, 32.9175), ("Entebbe", 0.0512, 32.4637),
    ("Marrakesh", 31.6295, -7.9811), ("Pretoria", -25.7479, 28.2293),
    ("Durban", -29.8587, 31.0218), ("Bloemfontein", -29.0852, 26.1596),
    ("Port Elizabeth", -33.9608, 25.6022), ("Livingstone", -17.8419, 25.8543)
])

add_unique_nodes("East Asia", [
    ("Macau", 22.1987, 113.5439), ("Kyoto", 35.0116, 135.7681),
    ("Nara", 34.6851, 135.8048), ("Kobe", 34.6901, 135.1955),
    ("Hiroshima", 34.3853, 132.4553), ("Sendai", 38.2682, 140.8694),
    ("Jeju City", 33.4996, 126.5312), ("Suzhou", 31.2989, 120.5853),
    ("Qingdao", 36.0671, 120.3826), ("Dalian", 38.9140, 121.6147),
    ("Harbin", 45.8038, 126.5349), ("Kunming", 25.0389, 102.7183),
    ("Guilin", 25.2345, 110.1799), ("Lhasa", 29.6520, 91.1721)
])

add_unique_nodes("Southeast Asia", [
    ("Hoi An", 15.8801, 108.3380), ("Da Nang", 16.0544, 108.2022),
    ("Hue", 16.4637, 107.5909), ("Siem Reap", 13.3671, 103.8448),
    ("Sihanoukville", 10.6253, 103.5234), ("George Town", 5.4141, 100.3288),
    ("Malacca", 2.1896, 102.2501), ("Baguio", 16.4023, 120.5960),
    ("Yogyakarta", -7.7956, 110.3695), ("Makassar", -5.1477, 119.4327)
])

add_unique_nodes("Oceania", [
    ("Rotorua", -38.1368, 176.2497), ("Dunedin", -45.8788, 170.5028),
    ("Hamilton NZ", -37.7870, 175.2793), ("Tauranga", -37.6878, 176.1651),
    ("Napier", -39.4928, 176.9120), ("Nelson", -41.2706, 173.2840),
    ("Rarotonga", -21.2292, -159.7763), ("Avarua", -21.2070, -159.7710)
])

regional_nodes["Central Asia"] = [
    ("Astana", 51.1694, 71.4491), ("Almaty", 43.2220, 76.8512),
    ("Tashkent", 41.2995, 69.2401), ("Samarkand", 39.6542, 66.9597),
    ("Bishkek", 42.8746, 74.5698), ("Osh", 40.5139, 72.8161),
    ("Dushanbe", 38.5598, 68.7870), ("Khujand", 40.2833, 69.6333),
    ("Ashgabat", 37.9601, 58.3261), ("Turkmenabat", 39.0733, 63.5786)
]

regional_nodes["South Asia"] = [
    ("Karachi", 24.8607, 67.0011), ("Lahore", 31.5204, 74.3587),
    ("Islamabad", 33.6844, 73.0479), ("Dhaka", 23.8103, 90.4125),
    ("Chittagong", 22.3569, 91.7832), ("Sylhet", 24.8949, 91.8687),
    ("Kathmandu", 27.7172, 85.3240), ("Pokhara", 28.2096, 83.9856),
    ("Colombo", 6.9271, 79.8612), ("Kandy", 7.2906, 80.6337),
    ("Male", 4.1755, 73.5093), ("Thimphu", 27.4728, 89.6390)
]

regional_nodes["West Asia"] = [
    ("Yerevan", 40.1792, 44.4991), ("Gyumri", 40.7894, 43.8475),
    ("Baku", 40.4093, 49.8671), ("Ganja", 40.6828, 46.3606),
    ("Tbilisi", 41.7151, 44.8271), ("Batumi", 41.6168, 41.6367),
    ("Tehran", 35.6892, 51.3890), ("Isfahan", 32.6546, 51.6680),
    ("Shiraz", 29.5918, 52.5837), ("Mashhad", 36.2605, 59.6168),
    ("Baghdad", 33.3152, 44.3661), ("Erbil", 36.1901, 43.9930)
]

add_unique_nodes("Middle East", [
    ("Beirut", 33.8938, 35.5018), ("Damascus", 33.5138, 36.2765),
    ("Medina", 24.5247, 39.5692), ("Mecca", 21.3891, 39.8579),
    ("Manama", 26.2235, 50.5876), ("Sanaa", 15.3694, 44.1910),
    ("Aden", 12.7855, 45.0187), ("Izmir", 38.4237, 27.1428),
    ("Ankara", 39.9334, 32.8597), ("Antalya", 36.8969, 30.7133)
])

add_unique_nodes("East Asia", [
    ("Nagoya", 35.1815, 136.9066), ("Fukuoka", 33.5902, 130.4017),
    ("Sapporo", 43.0618, 141.3545), ("Yokohama", 35.4437, 139.6380),
    ("Incheon", 37.4563, 126.7052), ("Daegu", 35.8714, 128.6014),
    ("Tianjin", 39.3434, 117.3616), ("Chengdu", 30.5728, 104.0668),
    ("Wuhan", 30.5928, 114.3055), ("Xian", 34.3416, 108.9398),
    ("Chongqing", 29.4316, 106.9123), ("Hangzhou", 30.2741, 120.1551),
    ("Nanjing", 32.0603, 118.7969), ("Ulaanbaatar", 47.8864, 106.9057)
])

add_unique_nodes("Southeast Asia", [
    ("Chiang Mai", 18.7883, 98.9853), ("Phuket", 7.8804, 98.3923),
    ("Surabaya", -7.2575, 112.7521), ("Bandung", -6.9175, 107.6191),
    ("Medan", 3.5952, 98.6722), ("Cebu City", 10.3157, 123.8854),
    ("Davao", 7.1907, 125.4553), ("Vientiane", 17.9757, 102.6331),
    ("Luang Prabang", 19.8834, 102.1347), ("Mandalay", 21.9588, 96.0891),
    ("Naypyidaw", 19.7633, 96.0785), ("Bandar Seri Begawan", 4.9031, 114.9398),
    ("Dili", -8.5569, 125.5603)
])

regional_nodes["Oceania"] = [
    ("Auckland", -36.8509, 174.7645), ("Wellington", -41.2865, 174.7762),
    ("Christchurch", -43.5321, 172.6362), ("Queenstown", -45.0312, 168.6626),
    ("Suva", -18.1248, 178.4501), ("Nadi", -17.7765, 177.4356),
    ("Port Moresby", -9.4438, 147.1803), ("Lae", -6.7155, 146.9999),
    ("Honiara", -9.4456, 159.9729), ("Port Vila", -17.7333, 168.3273),
    ("Noumea", -22.2711, 166.4416), ("Apia", -13.8507, -171.7514),
    ("Pago Pago", -14.2756, -170.7020), ("Nuku'alofa", -21.1394, -175.2049),
    ("Papeete", -17.5516, -149.5585), ("Tarawa", 1.4518, 172.9717),
    ("Majuro", 7.1164, 171.1858), ("Palikir", 6.9174, 158.1850),
    ("Yaren", -0.5477, 166.9209)
]

# 2. Haversine Geometry Formula for Realistic Edge Costs
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth's radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

cities_out = []
routes_out = []

# Map region main hubs for long-haul international flights
hubs = {
    "USA": "New York",
    "India": "Mumbai",
    "Europe": "London",
    "Canada": "Toronto",
    "Mexico": "Mexico City",
    "East Asia": "Tokyo",
    "Southeast Asia": "Singapore",
    "Central Asia": "Tashkent",
    "South Asia": "Karachi",
    "West Asia": "Tehran",
    "Middle East": "Dubai",
    "Australia": "Sydney",
    "Oceania": "Auckland",
    "South America": "Sao Paulo",
    "Africa": "Cairo"
}

# Populate Nodes
for region, cities in regional_nodes.items():
    for city, lat, lon in cities:
        cities_out.append([f'"{region}","{city}",{lat},{lon}'])

# Generate Ground & Local Mesh Routes Dynamically
for region, cities in regional_nodes.items():
    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            c1, lat1, lon1 = cities[i]
            c2, lat2, lon2 = cities[j]
            dist = calculate_distance(lat1, lon1, lat2, lon2)
            
            # Ground routes (Train/Car) generated for localized proximity pairs (< 600km)
            if dist < 600:
                # Train Option
                t_time = round(dist / 120.0, 2) # 120 km/h average
                t_cost = round(dist * 0.12, 2)
                routes_out.append([f'"{c1}","{c2}","train",{t_time},{t_cost},"Express Line Service"'])
                routes_out.append([f'"{c2}","{c1}","train",{t_time},{t_cost},"Express Line Service"'])
                
                # Highway Option
                c_time = round(dist / 90.0, 2) # 90 km/h average
                c_cost = round(dist * 0.08, 2)
                routes_out.append([f'"{c1}","{c2}","car",{c_time},{c_cost},"National Highway Corridor"'])
                routes_out.append([f'"{c2}","{c1}","car",{c_time},{c_cost},"National Highway Corridor"'])
            
            # Regional Flights for medium-long distances within the same zone
            elif dist < 2500:
                f_time = round((dist / 750.0) + 0.5, 2) # flight speed + buffering overhead
                f_cost = round(100 + (dist * 0.15), 2)
                routes_out.append([f'"{c1}","{c2}","plane",{f_time},{f_cost},"Regional Flight Connection"'])
                routes_out.append([f'"{c2}","{c1}","plane",{f_time},{f_cost},"Regional Flight Connection"'])

# Create Inter-Continental High-Speed Flights between global backbones
hub_regions = list(hubs.keys())
for i in range(len(hub_regions)):
    for j in range(i + 1, len(hub_regions)):
        r1, r2 = hub_regions[i], hub_regions[j]
        h1_name = hubs[r1]
        h2_name = hubs[r2]
        
        # Pull matching data indices
        h1 = [c for c in regional_nodes[r1] if c[0] == h1_name][0]
        h2 = [c for c in regional_nodes[r2] if c[0] == h2_name][0]
        
        dist = calculate_distance(h1[1], h1[2], h2[1], h2[2])
        f_time = round((dist / 850.0) + 1.5, 2)
        f_cost = round(400 + (dist * 0.10), 2)
        
        routes_out.append([f'"{h1_name}","{h2_name}","plane",{f_time},{f_cost},"Intercontinental Hub Flight"'])
        routes_out.append([f'"{h2_name}","{h1_name}","plane",{f_time},{f_cost},"Intercontinental Hub Flight"'])

# 3. Save Out Flat Data Files directly matching your C++ parser structures
with open("cities.csv", "w", newline="", encoding="utf-8") as f:
    for row in cities_out:
        f.write(row[0] + "\n")

with open("routes.csv", "w", newline="", encoding="utf-8") as f:
    for row in routes_out:
        f.write(row[0] + "\n")

print(f">> Successfully generated {len(cities_out)} massive global cities!")
print(f">> Successfully connected {len(routes_out)} dense multi-modal transit legs!")
