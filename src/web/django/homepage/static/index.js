var center = ol.proj.transform([37.41, 8.82], 'EPSG:4326', 'EPSG:3857');

var view = new ol.View({
    center: ol.proj.fromLonLat([2.333333, 48.866667]),
    zoom: 10
})

var map = new ol.Map({
    target: 'map',
    layers: [new ol.layer.Tile({
        source: new ol.source.OSM()
    })],
    view: view
});

var geojsonObject = {
    "type": "FeatureCollection",
    "features": [{
        "type": "Feature",
        "properties": {
          "stroke": "#555555",
          "stroke-width": 2,
          "stroke-opacity": 1,
          "fill": "#00aa22",
          "fill-opacity": 0.5
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[2.320902853673183, 48.863057390616895], [2.320941363405975, 48.8630455227806], [2.324735595380242, 48.8618856488404], [2.3252307880557153, 48.86173175907539], [2.325237201197246, 48.86172976720177], [2.325279730372084, 48.861717449370154], [2.326102290322419, 48.861478060902286], [2.327067639951823, 48.86114585015794], [2.328311532595535, 48.86073713622665], [2.328327173989778, 48.860731178585795], [2.329523658986177, 48.86026806571577], [2.329815344893258, 48.86016485062229], [2.329856100299037, 48.86015037087975], [2.329904495269684, 48.86013325563593], [2.329908983447546, 48.86013158099519], [2.332910100578299, 48.85934960615888], [2.332445797611004, 48.8585085069548], [2.333265988697765, 48.8582645608496], [2.333248549636101, 48.85824313466106], [2.333242974138866, 48.85823628381196], [2.332750055836757, 48.85763064497636], [2.331672866804062, 48.856314246964295], [2.331145683633401, 48.855623310218895], [2.330841142533798, 48.85519874921245], [2.330700542924902, 48.85496376287147], [2.330457888762933, 48.85446024342495], [2.330432690483256, 48.85441707908065], [2.329378444140045, 48.852735462156524], [2.329309916041171, 48.85261396800675], [2.3284185653936, 48.85182479473357], [2.327193140060224, 48.85162533447336], [2.326865727988169, 48.851408400755986], [2.326638734244415, 48.85126152914954], [2.325273597561204, 48.85069666188126], [2.324139714658669, 48.85023026446265], [2.3232865349741942, 48.84982576851045], [2.322898103749189, 48.84963489967507], [2.322133510014468, 48.84924973357273], [2.320541155736984, 48.84841994209822], [2.320177634658829, 48.84823128935817], [2.32008367508204, 48.8481801294956], [2.3193552186153212, 48.8478450423334], [2.319079057823354, 48.84773439185731], [2.318043161953749, 48.847338123691166], [2.316571525922003, 48.84682460831802], [2.316097509191232, 48.84666304155859], [2.313729873598172, 48.84593328656336], [2.313641280957853, 48.845990046203234], [2.312091028580114, 48.846983212758936], [2.311767709159531, 48.84719033639172], [2.311625847644086, 48.847281216555366], [2.311486631207579, 48.847368855176626], [2.311260835819493, 48.847510996658556], [2.311155377296785, 48.84757938949668], [2.310525952151246, 48.84798758363206], [2.310378251508753, 48.84795218786006], [2.308219888290114, 48.847434925901986], [2.3080419591723302, 48.84739225374763], [2.307339709005096, 48.847139376795404], [2.306149310004038, 48.84789994583024], [2.303746047913422, 48.84943929154836], [2.300964661201576, 48.85123012651538], [2.300883913456113, 48.851176131084145], [2.299322310264648, 48.852174427333274], [2.297923418787436, 48.853068650104696], [2.297388894455644, 48.85341164261926], [2.295929526344629, 48.85434804668676], [2.295868050746559, 48.854387490546586], [2.29574570829236, 48.85446598873217], [2.293079176013769, 48.85617407768941], [2.292935322260579, 48.85626502245174], [2.290780998017134, 48.85763978855226], [2.29070227350634, 48.85769001146594], [2.290621248453761, 48.85774171362002], [2.290611522324999, 48.85774791817999], [2.290601723337746, 48.85775416817441], [2.290591924335898, 48.857760419067276], [2.290582125356189, 48.857766668160714], [2.290572326349741, 48.85777291905187], [2.290562527353085, 48.85777916904292], [2.290552728354078, 48.857785419033156], [2.290549110963099, 48.857787726020156], [2.290542932054, 48.857791670837265], [2.290533137114455, 48.8577979226486], [2.290523340797328, 48.8578041753503], [2.290513543127311, 48.857810427143825], [2.290503749531353, 48.85781667986005], [2.290493953219519, 48.85782293165997], [2.290484158268119, 48.85782918346714], [2.290474361951584, 48.857835435265365], [2.290464565608205, 48.857841688861356], [2.290454769274722, 48.85784794155719], [2.2904449743139192, 48.85785419336102], [2.290435177987979, 48.8578604451559], [2.29042538165969, 48.85786669694998], [2.290415586679587, 48.85787294965055], [2.290411987116157, 48.85787524774541], [2.290405790358843, 48.85787920054366], [2.290395995361893, 48.85788545414185], [2.290386199024097, 48.857891705932566], [2.290376402684053, 48.85789795772246], [2.290366607692297, 48.85790421041883], [2.290356811347552, 48.85791046220704], [2.290347016363241, 48.85791671400249], [2.290340730189204, 48.857920726523844], [2.290337220001545, 48.85792296668829], [2.290327420911721, 48.85792921935711], [2.289839040379379, 48.858240852910015], [2.291251449328896, 48.85935283814257], [2.291558697794395, 48.85961018034319], [2.291559637128033, 48.85961096654392], [2.291778091813364, 48.859781458773185], [2.291954451320872, 48.85990948851705], [2.292681256210368, 48.86043711353505], [2.293613042382569, 48.8611206542698], [2.293916786125047, 48.8613295552173], [2.29419576276334, 48.861521138827825], [2.29432082507884, 48.86158971183439], [2.294660601380633, 48.861761595439255], [2.295089767941716, 48.861962289236715], [2.2954253429459293, 48.86210764732262], [2.295557229801291, 48.862169115607394], [2.295886813903742, 48.86231437413768], [2.296014614111395, 48.86236846385564], [2.2961522687598412, 48.86242202051613], [2.296224578576981, 48.862451344645066], [2.296365882978674, 48.862505281357706], [2.296383264465269, 48.86251128689651], [2.296521218371363, 48.86256009990083], [2.296570586048064, 48.86257611794765], [2.296624366059855, 48.86259476373113], [2.296747985580188, 48.86263391951963], [2.2967833914035403, 48.862645175205806], [2.296843205727061, 48.86266525483823], [2.297054412601712, 48.86273483822627], [2.297242596094284, 48.86279268440504], [2.297430508756709, 48.862850529591846], [2.297435580037067, 48.86285190479282], [2.297543203597627, 48.862882754759625], [2.297921354423242, 48.86298370095845], [2.298573842319958, 48.8631331094409], [2.298670053670455, 48.86315607073508], [2.2989494214201383, 48.86321677692943], [2.299228107948811, 48.863268892372474], [2.29923179985754, 48.86326965865298], [2.299236392802037, 48.8632703222872], [2.299782117619565, 48.86334915190465], [2.299786477938701, 48.86334978177994], [2.299788774565893, 48.86335000116842], [2.300074597688598, 48.863381076497944], [2.300478428006688, 48.86341628007419], [2.301070050573896, 48.86344881177568], [2.3011179272878453, 48.863451459360725], [2.301590057912434, 48.86347435738185], [2.301727780606055, 48.86347669530921], [2.301756058885901, 48.86347717507086], [2.301920326403111, 48.86347996173324], [2.301946347899939, 48.86348040130559], [2.302030309905541, 48.86348177237047], [2.305379187923055, 48.86353840134594], [2.305380434937092, 48.863538419375885], [2.305615668883199, 48.863541968979185], [2.310264173591303, 48.863624697583866], [2.310298117752702, 48.86362533658689], [2.310386298005485, 48.86362688528127], [2.315288893801303, 48.86371144188118], [2.315289913186723, 48.86371145940487], [2.316406146479132, 48.86373061298977], [2.318472737942571, 48.863777361507424], [2.318539119607862, 48.863775570279714], [2.31860672764467, 48.863769643598054], [2.318675293964827, 48.8637578783667], [2.318741669005619, 48.863743144463726], [2.319427206867646, 48.863525262788144], [2.319516090876288, 48.86349704121495], [2.319776050279907, 48.86341460801522], [2.319865054793965, 48.863386210594776], [2.3203159868873042, 48.86324292772078], [2.320316580955533, 48.863242737734666], [2.320902339026845, 48.863057553176816], [2.320902853673183, 48.863057390616895]]]
        }
    }]
};

var originalSource = new ol.source.Vector({
    features: (new ol.format.GeoJSON()).readFeatures(geojsonObject, {
        featureProjection: 'EPSG:3857'
    })
});

var originalLayer = new ol.layer.Vector({
    source: originalSource
});

map.addLayer(originalLayer);
