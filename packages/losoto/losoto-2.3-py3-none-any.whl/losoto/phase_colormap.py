from matplotlib.colors import ListedColormap

# cm_data = np.roll(np.array(colorcet.cyclic_mrybm_35_75_c68), 79).tolist()
cm_data = [[ 0.65830839, 0.46993917, 0.04941288],
           [ 0.66433742, 0.4662019 , 0.05766473],
           [ 0.67020869, 0.46248014, 0.0653456 ],
           [ 0.67604299, 0.45869838, 0.07273174],
           [ 0.68175228, 0.45491407, 0.07979262],
           [ 0.6874028 , 0.45108417, 0.08667103],
           [ 0.6929505 , 0.44723893, 0.09335869],
           [ 0.69842619, 0.44335768, 0.09992839],
           [ 0.7038123 , 0.43945328, 0.1063871 ],
           [ 0.70912069, 0.43551765, 0.11277174],
           [ 0.71434524, 0.43155576, 0.11909348],
           [ 0.71949289, 0.42756272, 0.12537606],
           [ 0.72455619, 0.4235447 , 0.13162325],
           [ 0.72954895, 0.41949098, 0.13786305],
           [ 0.73445172, 0.41541774, 0.14408039],
           [ 0.73929496, 0.41129973, 0.15032217],
           [ 0.74403834, 0.40717158, 0.15654335],
           [ 0.74873695, 0.40298519, 0.16282282],
           [ 0.75332319, 0.39880107, 0.16907566],
           [ 0.75788083, 0.39454245, 0.17542179],
           [ 0.7623326 , 0.39028096, 0.18175915],
           [ 0.76673205, 0.38596549, 0.18816819],
           [ 0.77105247, 0.38162141, 0.19461532],
           [ 0.77529528, 0.37724732, 0.20110652],
           [ 0.77948666, 0.37281509, 0.2076873 ],
           [ 0.78358534, 0.36836772, 0.21429736],
           [ 0.78763763, 0.363854  , 0.22101648],
           [ 0.79161134, 0.35930804, 0.2277974 ],
           [ 0.79550606, 0.3547299 , 0.23464353],
           [ 0.79935398, 0.35007959, 0.24161832],
           [ 0.80311671, 0.34540152, 0.24865892],
           [ 0.80681033, 0.34067452, 0.25580075],
           [ 0.8104452 , 0.33588248, 0.26307222],
           [ 0.8139968 , 0.33105538, 0.27043183],
           [ 0.81747689, 0.32617526, 0.27791096],
           [ 0.82089415, 0.32122629, 0.28553846],
           [ 0.82422713, 0.3162362 , 0.29327617],
           [ 0.82747661, 0.31120154, 0.30113388],
           [ 0.83066399, 0.30608459, 0.30917579],
           [ 0.83376307, 0.30092244, 0.31734921],
           [ 0.83677286, 0.29571346, 0.32566199],
           [ 0.83969693, 0.29044723, 0.33413665],
           [ 0.84253873, 0.28511151, 0.34279962],
           [ 0.84528297, 0.27972917, 0.35162078],
           [ 0.84792704, 0.27430045, 0.36060681],
           [ 0.85046793, 0.26882624, 0.36976395],
           [ 0.85291056, 0.26328859, 0.37913116],
           [ 0.855242  , 0.25770888, 0.38868217],
           [ 0.85745673, 0.25209367, 0.39841601],
           [ 0.85955023, 0.24644737, 0.40833625],
           [ 0.86151767, 0.24077563, 0.41844557],
           [ 0.86335392, 0.23508521, 0.42874606],
           [ 0.86505685, 0.22937288, 0.43926008],
           [ 0.86661606, 0.22366308, 0.44996127],
           [ 0.86802578, 0.21796785, 0.46084758],
           [ 0.86928003, 0.21230132, 0.47191554],
           [ 0.87037274, 0.20667988, 0.48316015],
           [ 0.87129781, 0.2011224 , 0.49457479],
           [ 0.87204914, 0.19565041, 0.50615118],
           [ 0.87262076, 0.19028829, 0.51787932],
           [ 0.87300686, 0.18506334, 0.5297475 ],
           [ 0.8732019 , 0.18000588, 0.54174232],
           [ 0.87320066, 0.1751492 , 0.55384874],
           [ 0.87299833, 0.17052942, 0.56605016],
           [ 0.87259058, 0.16618514, 0.57832856],
           [ 0.87197361, 0.16215698, 0.59066466],
           [ 0.87114414, 0.15848667, 0.60303881],
           [ 0.87009966, 0.15521687, 0.61542844],
           [ 0.86883823, 0.15238892, 0.62781175],
           [ 0.86735858, 0.15004199, 0.64016651],
           [ 0.8656601 , 0.14821149, 0.65247022],
           [ 0.86374282, 0.14692762, 0.66470043],
           [ 0.86160744, 0.14621386, 0.67683495],
           [ 0.85925523, 0.14608582, 0.68885204],
           [ 0.85668805, 0.14655046, 0.70073065],
           [ 0.85390829, 0.14760576, 0.71245054],
           [ 0.85091881, 0.14924094, 0.7239925 ],
           [ 0.84772287, 0.15143717, 0.73533849],
           [ 0.84432409, 0.15416865, 0.74647174],
           [ 0.84072639, 0.15740403, 0.75737678],
           [ 0.83693394, 0.16110786, 0.76803952],
           [ 0.83295108, 0.16524205, 0.77844723],
           [ 0.82878232, 0.16976729, 0.78858858],
           [ 0.82443225, 0.17464414, 0.7984536 ],
           [ 0.81990551, 0.179834  , 0.80803365],
           [ 0.81520674, 0.18529984, 0.8173214 ],
           [ 0.81034059, 0.19100664, 0.82631073],
           [ 0.80531176, 0.1969216 , 0.83499645],
           [ 0.80012467, 0.20301465, 0.84337486],
           [ 0.79478367, 0.20925826, 0.8514432 ],
           [ 0.78929302, 0.21562737, 0.85919957],
           [ 0.78365681, 0.22209936, 0.86664294],
           [ 0.77787898, 0.22865386, 0.87377308],
           [ 0.7719633 , 0.23527265, 0.88059043],
           [ 0.76591335, 0.24193947, 0.88709606],
           [ 0.7597325 , 0.24863985, 0.89329158],
           [ 0.75342394, 0.25536094, 0.89917908],
           [ 0.74699063, 0.26209137, 0.90476105],
           [ 0.74043533, 0.2688211 , 0.91004033],
           [ 0.73376055, 0.27554128, 0.91502   ],
           [ 0.72696862, 0.28224415, 0.91970339],
           [ 0.7200616 , 0.2889229 , 0.92409395],
           [ 0.71304134, 0.29557159, 0.92819525],
           [ 0.70590945, 0.30218508, 0.9320109 ],
           [ 0.69866732, 0.30875887, 0.93554451],
           [ 0.69131609, 0.31528914, 0.93879964],
           [ 0.68385669, 0.32177259, 0.94177976],
           [ 0.6762898 , 0.32820641, 0.94448822],
           [ 0.6686159 , 0.33458824, 0.94692818],
           [ 0.66083524, 0.3409161 , 0.94910264],
           [ 0.65294785, 0.34718834, 0.95101432],
           [ 0.64495358, 0.35340362, 0.95266571],
           [ 0.63685208, 0.35956083, 0.954059  ],
           [ 0.62864284, 0.3656591 , 0.95519608],
           [ 0.62032517, 0.3716977 , 0.95607853],
           [ 0.61189825, 0.37767607, 0.95670757],
           [ 0.60336117, 0.38359374, 0.95708408],
           [ 0.59471291, 0.3894503 , 0.95720861],
           [ 0.58595242, 0.39524541, 0.95708134],
           [ 0.5770786 , 0.40097871, 0.95670212],
           [ 0.56809041, 0.40664983, 0.95607045],
           [ 0.55898686, 0.41225834, 0.95518556],
           [ 0.54976709, 0.41780374, 0.95404636],
           [ 0.5404304 , 0.42328541, 0.95265153],
           [ 0.53097635, 0.42870263, 0.95099953],
           [ 0.52140479, 0.43405447, 0.94908866],
           [ 0.51171597, 0.43933988, 0.94691713],
           [ 0.50191056, 0.44455757, 0.94448311],
           [ 0.49198981, 0.44970607, 0.94178481],
           [ 0.48195555, 0.45478367, 0.93882055],
           [ 0.47181035, 0.45978843, 0.93558888],
           [ 0.46155756, 0.46471821, 0.93208866],
           [ 0.45119801, 0.46957218, 0.92831786],
           [ 0.44073852, 0.47434688, 0.92427669],
           [ 0.43018722, 0.47903864, 0.9199662 ],
           [ 0.41955166, 0.4836444 , 0.91538759],
           [ 0.40884063, 0.48816094, 0.91054293],
           [ 0.39806421, 0.49258494, 0.90543523],
           [ 0.38723377, 0.49691301, 0.90006852],
           [ 0.37636206, 0.50114173, 0.89444794],
           [ 0.36546127, 0.5052684 , 0.88857877],
           [ 0.35454654, 0.5092898 , 0.88246819],
           [ 0.34363779, 0.51320158, 0.87612664],
           [ 0.33275309, 0.51700082, 0.86956409],
           [ 0.32191166, 0.52068487, 0.86279166],
           [ 0.31113372, 0.52425144, 0.85582152],
           [ 0.3004404 , 0.52769862, 0.84866679],
           [ 0.28985326, 0.53102505, 0.84134123],
           [ 0.27939616, 0.53422931, 0.83386051],
           [ 0.26909181, 0.53731099, 0.82623984],
           [ 0.258963  , 0.5402702 , 0.81849475],
           [ 0.24903239, 0.54310763, 0.8106409 ],
           [ 0.23932229, 0.54582448, 0.80269392],
           [ 0.22985664, 0.54842189, 0.79467122],
           [ 0.2206551 , 0.55090241, 0.78658706],
           [ 0.21173641, 0.55326901, 0.77845533],
           [ 0.20311843, 0.55552489, 0.77028973],
           [ 0.1948172 , 0.55767365, 0.76210318],
           [ 0.1868466 , 0.55971922, 0.75390763],
           [ 0.17921799, 0.56166586, 0.74571407],
           [ 0.1719422 , 0.56351747, 0.73753498],
           [ 0.16502295, 0.56527915, 0.72937754],
           [ 0.15846116, 0.566956  , 0.72124819],
           [ 0.15225499, 0.56855297, 0.71315321],
           [ 0.14639876, 0.57007506, 0.70509769],
           [ 0.14088284, 0.57152729, 0.69708554],
           [ 0.13569366, 0.57291467, 0.68911948],
           [ 0.13081385, 0.57424211, 0.68120108],
           [ 0.12622247, 0.57551447, 0.67333078],
           [ 0.12189539, 0.57673644, 0.66550792],
           [ 0.11780654, 0.57791235, 0.65773233],
           [ 0.11392613, 0.5790468 , 0.64999984],
           [ 0.11022348, 0.58014398, 0.64230637],
           [ 0.10666732, 0.58120782, 0.63464733],
           [ 0.10322631, 0.58224198, 0.62701729],
           [ 0.0998697 , 0.58324982, 0.61941001],
           [ 0.09656813, 0.58423445, 0.61181853],
           [ 0.09329429, 0.58519864, 0.60423523],
           [ 0.09002364, 0.58614483, 0.5966519 ],
           [ 0.08673514, 0.58707512, 0.58905979],
           [ 0.08341199, 0.58799127, 0.58144971],
           [ 0.08004245, 0.58889466, 0.57381211],
           [ 0.07662083, 0.58978633, 0.56613714],
           [ 0.07314852, 0.59066692, 0.55841474],
           [ 0.06963541, 0.5915367 , 0.55063471],
           [ 0.06610144, 0.59239556, 0.54278681],
           [ 0.06257861, 0.59324304, 0.53486082],
           [ 0.05911304, 0.59407833, 0.52684614],
           [ 0.05576765, 0.5949003 , 0.5187322 ],
           [ 0.05262511, 0.59570732, 0.51050978],
           [ 0.04978881, 0.5964975 , 0.50216936],
           [ 0.04738319, 0.59726862, 0.49370174],
           [ 0.04555067, 0.59801813, 0.48509809],
           [ 0.04444396, 0.59874316, 0.47635   ],
           [ 0.04421323, 0.59944056, 0.46744951],
           [ 0.04498918, 0.60010687, 0.45838913],
           [ 0.04686604, 0.60073837, 0.44916187],
           [ 0.04988979, 0.60133103, 0.43976125],
           [ 0.05405573, 0.60188055, 0.4301812 ],
           [ 0.05932209, 0.60238289, 0.42040543],
           [ 0.06560774, 0.60283258, 0.41043772],
           [ 0.07281962, 0.60322442, 0.40027363],
           [ 0.08086177, 0.60355283, 0.38990941],
           [ 0.08964366, 0.60381194, 0.37934208],
           [ 0.09908952, 0.60399554, 0.36856412],
           [ 0.10914617, 0.60409695, 0.35755799],
           [ 0.11974119, 0.60410858, 0.34634096],
           [ 0.13082746, 0.6040228 , 0.33491416],
           [ 0.14238003, 0.60383119, 0.323267  ],
           [ 0.1543847 , 0.60352425, 0.31138823],
           [ 0.16679093, 0.60309301, 0.29931029],
           [ 0.17959757, 0.60252668, 0.2870237 ],
           [ 0.19279966, 0.60181364, 0.27452964],
           [ 0.20634465, 0.60094466, 0.2618794 ],
           [ 0.22027287, 0.5999043 , 0.24904251],
           [ 0.23449833, 0.59868591, 0.23611022],
           [ 0.24904416, 0.5972746 , 0.2230778 ],
           [ 0.26382006, 0.59566656, 0.21004673],
           [ 0.2788104 , 0.5938521 , 0.19705484],
           [ 0.29391494, 0.59183348, 0.18421621],
           [ 0.3090634 , 0.58961302, 0.17161942],
           [ 0.32415577, 0.58720132, 0.15937753],
           [ 0.3391059 , 0.58461164, 0.14759012],
           [ 0.35379624, 0.58186793, 0.13637734],
           [ 0.36817905, 0.5789861 , 0.12580054],
           [ 0.38215966, 0.57599512, 0.1159504 ],
           [ 0.39572824, 0.57290928, 0.10685038],
           [ 0.40881926, 0.56975727, 0.09855521],
           [ 0.42148106, 0.56654159, 0.09104002],
           [ 0.43364953, 0.56329296, 0.08434116],
           [ 0.44538908, 0.56000859, 0.07841305],
           [ 0.45672421, 0.5566943 , 0.07322913],
           [ 0.46765017, 0.55336373, 0.06876762],
           [ 0.47819138, 0.5500213 , 0.06498436],
           [ 0.48839686, 0.54666195, 0.06182163],
           [ 0.49828924, 0.5432874 , 0.05922726],
           [ 0.50789114, 0.53989827, 0.05714466],
           [ 0.51722475, 0.53649429, 0.05551476],
           [ 0.5263115 , 0.53307443, 0.05427793],
           [ 0.53517186, 0.52963707, 0.05337567],
           [ 0.54382515, 0.52618009, 0.05275208],
           [ 0.55228947, 0.52270103, 0.05235479],
           [ 0.56058163, 0.51919713, 0.0521356 ],
           [ 0.56871719, 0.51566545, 0.05205062],
           [ 0.57671045, 0.51210292, 0.0520602 ],
           [ 0.5845745 , 0.50850636, 0.05212851],
           [ 0.59232129, 0.50487256, 0.05222299],
           [ 0.5999617 , 0.50119827, 0.05231367],
           [ 0.60750568, 0.49748022, 0.05237234],
           [ 0.61496232, 0.49371512, 0.05237168],
           [ 0.62233999, 0.48989963, 0.05228423],
           [ 0.62964652, 0.48603032, 0.05208127],
           [ 0.63688935, 0.48210362, 0.05173155],
           [ 0.64407572, 0.4781157 , 0.0511996 ],
           [ 0.65121289, 0.47406244, 0.05044367],
           [ 0.65830839, 0.46993917, 0.04941288]];
cm_phase = ListedColormap(cm_data, name='phase')
