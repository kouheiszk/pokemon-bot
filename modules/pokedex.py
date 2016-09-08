#!/usr/bin/python
# -*- coding: utf-8 -*-
import enum


class Pokedex(enum.Enum):
    MISSINGNO = 0
    BULBASAUR = 1
    IVYSAUR = 2
    VENUSAUR = 3
    CHARMANDER = 4
    CHARMELEON = 5
    CHARIZARD = 6
    SQUIRTLE = 7
    WARTORTLE = 8
    BLASTOISE = 9
    CATERPIE = 10
    METAPOD = 11
    BUTTERFREE = 12
    WEEDLE = 13
    KAKUNA = 14
    BEEDRILL = 15
    PIDGEY = 16
    PIDGEOTTO = 17
    PIDGEOT = 18
    RATTATA = 19
    RATICATE = 20
    SPEAROW = 21
    FEAROW = 22
    EKANS = 23
    ARBOK = 24
    PIKACHU = 25
    RAICHU = 26
    SANDSHREW = 27
    SANDSLASH = 28
    NIDORAN_FEMALE = 29
    NIDORINA = 30
    NIDOQUEEN = 31
    NIDORAN_MALE = 32
    NIDORINO = 33
    NIDOKING = 34
    CLEFAIRY = 35
    CLEFABLE = 36
    VULPIX = 37
    NINETALES = 38
    JIGGLYPUFF = 39
    WIGGLYTUFF = 40
    ZUBAT = 41
    GOLBAT = 42
    ODDISH = 43
    GLOOM = 44
    VILEPLUME = 45
    PARAS = 46
    PARASECT = 47
    VENONAT = 48
    VENOMOTH = 49
    DIGLETT = 50
    DUGTRIO = 51
    MEOWTH = 52
    PERSIAN = 53
    PSYDUCK = 54
    GOLDUCK = 55
    MANKEY = 56
    PRIMEAPE = 57
    GROWLITHE = 58
    ARCANINE = 59
    POLIWAG = 60
    POLIWHIRL = 61
    POLIWRATH = 62
    ABRA = 63
    KADABRA = 64
    ALAKAZAM = 65
    MACHOP = 66
    MACHOKE = 67
    MACHAMP = 68
    BELLSPROUT = 69
    WEEPINBELL = 70
    VICTREEBEL = 71
    TENTACOOL = 72
    TENTACRUEL = 73
    GEODUDE = 74
    GRAVELER = 75
    GOLEM = 76
    PONYTA = 77
    RAPIDASH = 78
    SLOWPOKE = 79
    SLOWBRO = 80
    MAGNEMITE = 81
    MAGNETON = 82
    FARFETCHD = 83
    DODUO = 84
    DODRIO = 85
    SEEL = 86
    DEWGONG = 87
    GRIMER = 88
    MUK = 89
    SHELLDER = 90
    CLOYSTER = 91
    GASTLY = 92
    HAUNTER = 93
    GENGAR = 94
    ONIX = 95
    DROWZEE = 96
    HYPNO = 97
    KRABBY = 98
    KINGLER = 99
    VOLTORB = 100
    ELECTRODE = 101
    EXEGGCUTE = 102
    EXEGGUTOR = 103
    CUBONE = 104
    MAROWAK = 105
    HITMONLEE = 106
    HITMONCHAN = 107
    LICKITUNG = 108
    KOFFING = 109
    WEEZING = 110
    RHYHORN = 111
    RHYDON = 112
    CHANSEY = 113
    TANGELA = 114
    KANGASKHAN = 115
    HORSEA = 116
    SEADRA = 117
    GOLDEEN = 118
    SEAKING = 119
    STARYU = 120
    STARMIE = 121
    MR_MIME = 122
    SCYTHER = 123
    JYNX = 124
    ELECTABUZZ = 125
    MAGMAR = 126
    PINSIR = 127
    TAUROS = 128
    MAGIKARP = 129
    GYARADOS = 130
    LAPRAS = 131
    DITTO = 132
    EEVEE = 133
    VAPOREON = 134
    JOLTEON = 135
    FLAREON = 136
    PORYGON = 137
    OMANYTE = 138
    OMASTAR = 139
    KABUTO = 140
    KABUTOPS = 141
    AERODACTYL = 142
    SNORLAX = 143
    ARTICUNO = 144
    ZAPDOS = 145
    MOLTRES = 146
    DRATINI = 147
    DRAGONAIR = 148
    DRAGONITE = 149
    MEWTWO = 150
    MEW = 151

    @property
    def max_cp(self):
        cps = {Pokedex.MISSINGNO: 0, Pokedex.BULBASAUR: 1072, Pokedex.IVYSAUR: 1632, Pokedex.VENUSAUR: 2580,
               Pokedex.CHARMANDER: 955, Pokedex.CHARMELEON: 1557, Pokedex.CHARIZARD: 2602, Pokedex.SQUIRTLE: 1009,
               Pokedex.WARTORTLE: 1583, Pokedex.BLASTOISE: 2542, Pokedex.CATERPIE: 444, Pokedex.METAPOD: 478,
               Pokedex.BUTTERFREE: 1455, Pokedex.WEEDLE: 449, Pokedex.KAKUNA: 485, Pokedex.BEEDRILL: 1440,
               Pokedex.PIDGEY: 680, Pokedex.PIDGEOTTO: 1224, Pokedex.PIDGEOT: 2091, Pokedex.RATTATA: 582,
               Pokedex.RATICATE: 1444, Pokedex.SPEAROW: 687, Pokedex.FEAROW: 1746, Pokedex.EKANS: 824,
               Pokedex.ARBOK: 1767, Pokedex.PIKACHU: 888, Pokedex.RAICHU: 2028, Pokedex.SANDSHREW: 799,
               Pokedex.SANDSLASH: 1810, Pokedex.NIDORAN_FEMALE: 876, Pokedex.NIDORINA: 1405, Pokedex.NIDOQUEEN: 2485,
               Pokedex.NIDORAN_MALE: 843, Pokedex.NIDORINO: 1373, Pokedex.NIDOKING: 2475, Pokedex.CLEFAIRY: 1201,
               Pokedex.CLEFABLE: 2398, Pokedex.VULPIX: 831, Pokedex.NINETALES: 2188, Pokedex.JIGGLYPUFF: 918,
               Pokedex.WIGGLYTUFF: 2177, Pokedex.ZUBAT: 643, Pokedex.GOLBAT: 1921, Pokedex.ODDISH: 1148,
               Pokedex.GLOOM: 1689, Pokedex.VILEPLUME: 2493, Pokedex.PARAS: 917, Pokedex.PARASECT: 1747,
               Pokedex.VENONAT: 1029, Pokedex.VENOMOTH: 1890, Pokedex.DIGLETT: 457, Pokedex.DUGTRIO: 1169,
               Pokedex.MEOWTH: 756, Pokedex.PERSIAN: 1632, Pokedex.PSYDUCK: 1110, Pokedex.GOLDUCK: 2387,
               Pokedex.MANKEY: 879, Pokedex.PRIMEAPE: 1865, Pokedex.GROWLITHE: 1335, Pokedex.ARCANINE: 2984,
               Pokedex.POLIWAG: 796, Pokedex.POLIWHIRL: 1340, Pokedex.POLIWRATH: 2505, Pokedex.ABRA: 600,
               Pokedex.KADABRA: 1132, Pokedex.ALAKAZAM: 1814, Pokedex.MACHOP: 1090, Pokedex.MACHOKE: 1761,
               Pokedex.MACHAMP: 2594, Pokedex.BELLSPROUT: 1117, Pokedex.WEEPINBELL: 1724, Pokedex.VICTREEBEL: 2531,
               Pokedex.TENTACOOL: 905, Pokedex.TENTACRUEL: 2220, Pokedex.GEODUDE: 849, Pokedex.GRAVELER: 1434,
               Pokedex.GOLEM: 2303, Pokedex.PONYTA: 1516, Pokedex.RAPIDASH: 2199, Pokedex.SLOWPOKE: 1219,
               Pokedex.SLOWBRO: 2597, Pokedex.MAGNEMITE: 891, Pokedex.MAGNETON: 1880, Pokedex.FARFETCHD: 1264,
               Pokedex.DODUO: 855, Pokedex.DODRIO: 1836, Pokedex.SEEL: 1107, Pokedex.DEWGONG: 2146,
               Pokedex.GRIMER: 1284, Pokedex.MUK: 2603, Pokedex.SHELLDER: 823, Pokedex.CLOYSTER: 2053,
               Pokedex.GASTLY: 804, Pokedex.HAUNTER: 1380, Pokedex.GENGAR: 2078, Pokedex.ONIX: 857,
               Pokedex.DROWZEE: 1075, Pokedex.HYPNO: 2184, Pokedex.KRABBY: 792, Pokedex.KINGLER: 1646,
               Pokedex.VOLTORB: 840, Pokedex.ELECTRODE: 1646, Pokedex.EXEGGCUTE: 1100, Pokedex.EXEGGUTOR: 2955,
               Pokedex.CUBONE: 1007, Pokedex.MAROWAK: 1657, Pokedex.HITMONLEE: 1493, Pokedex.HITMONCHAN: 1517,
               Pokedex.LICKITUNG: 1627, Pokedex.KOFFING: 1152, Pokedex.WEEZING: 2250, Pokedex.RHYHORN: 1182,
               Pokedex.RHYDON: 2243, Pokedex.CHANSEY: 675, Pokedex.TANGELA: 1740, Pokedex.KANGASKHAN: 2043,
               Pokedex.HORSEA: 795, Pokedex.SEADRA: 1713, Pokedex.GOLDEEN: 965, Pokedex.SEAKING: 2044,
               Pokedex.STARYU: 938, Pokedex.STARMIE: 2182, Pokedex.MR_MIME: 1494, Pokedex.SCYTHER: 2074,
               Pokedex.JYNX: 1717, Pokedex.ELECTABUZZ: 2119, Pokedex.MAGMAR: 2265, Pokedex.PINSIR: 2122,
               Pokedex.TAUROS: 1845, Pokedex.MAGIKARP: 263, Pokedex.GYARADOS: 2689, Pokedex.LAPRAS: 2981,
               Pokedex.DITTO: 920, Pokedex.EEVEE: 1077, Pokedex.VAPOREON: 2816, Pokedex.JOLTEON: 2140,
               Pokedex.FLAREON: 2643, Pokedex.PORYGON: 1692, Pokedex.OMANYTE: 1120, Pokedex.OMASTAR: 2234,
               Pokedex.KABUTO: 1105, Pokedex.KABUTOPS: 2130, Pokedex.AERODACTYL: 2165, Pokedex.SNORLAX: 3113,
               Pokedex.ARTICUNO: 2978, Pokedex.ZAPDOS: 3114, Pokedex.MOLTRES: 3240, Pokedex.DRATINI: 983,
               Pokedex.DRAGONAIR: 1748, Pokedex.DRAGONITE: 3500, Pokedex.MEWTWO: 4145, Pokedex.MEW: 3299}
        return cps[self]

    @property
    def evolve_candies(self):
        costs = {Pokedex.MISSINGNO: 0, Pokedex.BULBASAUR: 25, Pokedex.IVYSAUR: 100, Pokedex.VENUSAUR: 0,
                 Pokedex.CHARMANDER: 25, Pokedex.CHARMELEON: 100, Pokedex.CHARIZARD: 0, Pokedex.SQUIRTLE: 25,
                 Pokedex.WARTORTLE: 100, Pokedex.BLASTOISE: 0, Pokedex.CATERPIE: 12, Pokedex.METAPOD: 50,
                 Pokedex.BUTTERFREE: 0, Pokedex.WEEDLE: 12, Pokedex.KAKUNA: 50, Pokedex.BEEDRILL: 0, Pokedex.PIDGEY: 12,
                 Pokedex.PIDGEOTTO: 50, Pokedex.PIDGEOT: 0, Pokedex.RATTATA: 25, Pokedex.RATICATE: 0,
                 Pokedex.SPEAROW: 50, Pokedex.FEAROW: 0, Pokedex.EKANS: 50, Pokedex.ARBOK: 0, Pokedex.PIKACHU: 50,
                 Pokedex.RAICHU: 0, Pokedex.SANDSHREW: 50, Pokedex.SANDSLASH: 0, Pokedex.NIDORAN_FEMALE: 25,
                 Pokedex.NIDORINA: 100, Pokedex.NIDOQUEEN: 0, Pokedex.NIDORAN_MALE: 25, Pokedex.NIDORINO: 100,
                 Pokedex.NIDOKING: 0, Pokedex.CLEFAIRY: 50, Pokedex.CLEFABLE: 0, Pokedex.VULPIX: 50,
                 Pokedex.NINETALES: 0, Pokedex.JIGGLYPUFF: 50, Pokedex.WIGGLYTUFF: 0, Pokedex.ZUBAT: 50,
                 Pokedex.GOLBAT: 0, Pokedex.ODDISH: 25, Pokedex.GLOOM: 100, Pokedex.VILEPLUME: 0, Pokedex.PARAS: 50,
                 Pokedex.PARASECT: 0, Pokedex.VENONAT: 50, Pokedex.VENOMOTH: 0, Pokedex.DIGLETT: 50, Pokedex.DUGTRIO: 0,
                 Pokedex.MEOWTH: 50, Pokedex.PERSIAN: 0, Pokedex.PSYDUCK: 50, Pokedex.GOLDUCK: 0, Pokedex.MANKEY: 50,
                 Pokedex.PRIMEAPE: 0, Pokedex.GROWLITHE: 50, Pokedex.ARCANINE: 0, Pokedex.POLIWAG: 25,
                 Pokedex.POLIWHIRL: 100, Pokedex.POLIWRATH: 0, Pokedex.ABRA: 25, Pokedex.KADABRA: 100,
                 Pokedex.ALAKAZAM: 0, Pokedex.MACHOP: 25, Pokedex.MACHOKE: 100, Pokedex.MACHAMP: 0,
                 Pokedex.BELLSPROUT: 25, Pokedex.WEEPINBELL: 100, Pokedex.VICTREEBEL: 0, Pokedex.TENTACOOL: 50,
                 Pokedex.TENTACRUEL: 0, Pokedex.GEODUDE: 25, Pokedex.GRAVELER: 100, Pokedex.GOLEM: 0,
                 Pokedex.PONYTA: 50, Pokedex.RAPIDASH: 0, Pokedex.SLOWPOKE: 50, Pokedex.SLOWBRO: 0,
                 Pokedex.MAGNEMITE: 50, Pokedex.MAGNETON: 0, Pokedex.FARFETCHD: 0, Pokedex.DODUO: 50, Pokedex.DODRIO: 0,
                 Pokedex.SEEL: 50, Pokedex.DEWGONG: 0, Pokedex.GRIMER: 50, Pokedex.MUK: 0, Pokedex.SHELLDER: 50,
                 Pokedex.CLOYSTER: 0, Pokedex.GASTLY: 25, Pokedex.HAUNTER: 100, Pokedex.GENGAR: 0, Pokedex.ONIX: 0,
                 Pokedex.DROWZEE: 50, Pokedex.HYPNO: 0, Pokedex.KRABBY: 50, Pokedex.KINGLER: 0, Pokedex.VOLTORB: 50,
                 Pokedex.ELECTRODE: 0, Pokedex.EXEGGCUTE: 50, Pokedex.EXEGGUTOR: 0, Pokedex.CUBONE: 50,
                 Pokedex.MAROWAK: 0, Pokedex.HITMONLEE: 0, Pokedex.HITMONCHAN: 0, Pokedex.LICKITUNG: 0,
                 Pokedex.KOFFING: 50, Pokedex.WEEZING: 0, Pokedex.RHYHORN: 50, Pokedex.RHYDON: 0, Pokedex.CHANSEY: 0,
                 Pokedex.TANGELA: 0, Pokedex.KANGASKHAN: 0, Pokedex.HORSEA: 50, Pokedex.SEADRA: 0, Pokedex.GOLDEEN: 50,
                 Pokedex.SEAKING: 0, Pokedex.STARYU: 50, Pokedex.STARMIE: 0, Pokedex.MR_MIME: 0, Pokedex.SCYTHER: 0,
                 Pokedex.JYNX: 0, Pokedex.ELECTABUZZ: 0, Pokedex.MAGMAR: 0, Pokedex.PINSIR: 0, Pokedex.TAUROS: 0,
                 Pokedex.MAGIKARP: 400, Pokedex.GYARADOS: 0, Pokedex.LAPRAS: 0, Pokedex.DITTO: 0, Pokedex.EEVEE: 25,
                 Pokedex.VAPOREON: 0, Pokedex.JOLTEON: 0, Pokedex.FLAREON: 0, Pokedex.PORYGON: 0, Pokedex.OMANYTE: 50,
                 Pokedex.OMASTAR: 0, Pokedex.KABUTO: 50, Pokedex.KABUTOPS: 0, Pokedex.AERODACTYL: 0, Pokedex.SNORLAX: 0,
                 Pokedex.ARTICUNO: 0, Pokedex.ZAPDOS: 0, Pokedex.MOLTRES: 0, Pokedex.DRATINI: 25,
                 Pokedex.DRAGONAIR: 100, Pokedex.DRAGONITE: 0, Pokedex.MEWTWO: 0, Pokedex.MEW: 0}
        return costs[self]

    @property
    def evolves(self):
        map = {Pokedex.BULBASAUR: Pokedex.IVYSAUR, Pokedex.IVYSAUR: Pokedex.VENUSAUR,
               Pokedex.CHARMANDER: Pokedex.CHARMELEON, Pokedex.CHARMELEON: Pokedex.CHARIZARD,
               Pokedex.SQUIRTLE: Pokedex.WARTORTLE, Pokedex.WARTORTLE: Pokedex.BLASTOISE,
               Pokedex.CATERPIE: Pokedex.METAPOD, Pokedex.METAPOD: Pokedex.BUTTERFREE, Pokedex.WEEDLE: Pokedex.KAKUNA,
               Pokedex.KAKUNA: Pokedex.BEEDRILL, Pokedex.PIDGEY: Pokedex.PIDGEOTTO, Pokedex.PIDGEOTTO: Pokedex.PIDGEOT,
               Pokedex.RATTATA: Pokedex.RATICATE, Pokedex.SPEAROW: Pokedex.FEAROW, Pokedex.EKANS: Pokedex.ARBOK,
               Pokedex.PIKACHU: Pokedex.RAICHU, Pokedex.SANDSHREW: Pokedex.SANDSLASH,
               Pokedex.NIDORAN_FEMALE: Pokedex.NIDORINA, Pokedex.NIDORINA: Pokedex.NIDOQUEEN,
               Pokedex.NIDORAN_MALE: Pokedex.NIDORINO, Pokedex.NIDORINO: Pokedex.NIDOKING,
               Pokedex.CLEFAIRY: Pokedex.CLEFABLE, Pokedex.VULPIX: Pokedex.NINETALES,
               Pokedex.JIGGLYPUFF: Pokedex.WIGGLYTUFF, Pokedex.ZUBAT: Pokedex.GOLBAT, Pokedex.ODDISH: Pokedex.GLOOM,
               Pokedex.GLOOM: Pokedex.VILEPLUME, Pokedex.PARAS: Pokedex.PARASECT, Pokedex.VENONAT: Pokedex.VENOMOTH,
               Pokedex.DIGLETT: Pokedex.DUGTRIO, Pokedex.MEOWTH: Pokedex.PERSIAN, Pokedex.PSYDUCK: Pokedex.GOLDUCK,
               Pokedex.MANKEY: Pokedex.PRIMEAPE, Pokedex.GROWLITHE: Pokedex.ARCANINE,
               Pokedex.POLIWAG: Pokedex.POLIWHIRL, Pokedex.POLIWHIRL: Pokedex.POLIWRATH, Pokedex.ABRA: Pokedex.KADABRA,
               Pokedex.KADABRA: Pokedex.ALAKAZAM, Pokedex.MACHOP: Pokedex.MACHOKE, Pokedex.MACHOKE: Pokedex.MACHAMP,
               Pokedex.BELLSPROUT: Pokedex.WEEPINBELL, Pokedex.WEEPINBELL: Pokedex.VICTREEBEL,
               Pokedex.TENTACOOL: Pokedex.TENTACRUEL, Pokedex.GEODUDE: Pokedex.GRAVELER,
               Pokedex.GRAVELER: Pokedex.GOLEM, Pokedex.PONYTA: Pokedex.RAPIDASH, Pokedex.SLOWPOKE: Pokedex.SLOWBRO,
               Pokedex.MAGNEMITE: Pokedex.MAGNETON, Pokedex.DODUO: Pokedex.DODRIO, Pokedex.SEEL: Pokedex.DEWGONG,
               Pokedex.GRIMER: Pokedex.MUK, Pokedex.SHELLDER: Pokedex.CLOYSTER, Pokedex.GASTLY: Pokedex.HAUNTER,
               Pokedex.HAUNTER: Pokedex.GENGAR, Pokedex.DROWZEE: Pokedex.HYPNO, Pokedex.KRABBY: Pokedex.KINGLER,
               Pokedex.VOLTORB: Pokedex.ELECTRODE, Pokedex.EXEGGCUTE: Pokedex.EXEGGUTOR,
               Pokedex.CUBONE: Pokedex.MAROWAK, Pokedex.KOFFING: Pokedex.WEEZING, Pokedex.RHYHORN: Pokedex.RHYDON,
               Pokedex.HORSEA: Pokedex.SEADRA, Pokedex.GOLDEEN: Pokedex.SEAKING, Pokedex.STARYU: Pokedex.STARMIE,
               Pokedex.MAGIKARP: Pokedex.GYARADOS, Pokedex.EEVEE: Pokedex.VAPOREON, Pokedex.EEVEE: Pokedex.JOLTEON,
               Pokedex.EEVEE: Pokedex.FLAREON, Pokedex.OMANYTE: Pokedex.OMASTAR, Pokedex.KABUTO: Pokedex.KABUTOPS,
               Pokedex.DRATINI: Pokedex.DRAGONAIR, Pokedex.DRAGONAIR: Pokedex.DRAGONITE}
        return map.get(self, None)

    @property
    def rarity(self):
        rarities = {}
        rarities[Rarity.MYTHIC] = [Pokedex.MEW]
        rarities[Rarity.LEGENDARY] = [Pokedex.ZAPDOS, Pokedex.MOLTRES, Pokedex.MEWTWO, Pokedex.ARTICUNO]
        rarities[Rarity.EPIC] = [Pokedex.DITTO, Pokedex.VENUSAUR, Pokedex.TAUROS, Pokedex.DRAGONITE, Pokedex.CLEFABLE,
                                 Pokedex.CHARIZARD, Pokedex.BLASTOISE]
        rarities[Rarity.VERY_RARE] = [Pokedex.WEEPINBELL, Pokedex.WARTORTLE, Pokedex.VILEPLUME, Pokedex.VICTREEBEL,
                                      Pokedex.VENOMOTH, Pokedex.VAPOREON, Pokedex.SLOWBRO, Pokedex.RAICHU,
                                      Pokedex.POLIWRATH, Pokedex.PINSIR, Pokedex.PIDGEOT, Pokedex.OMASTAR,
                                      Pokedex.NIDOQUEEN, Pokedex.NIDOKING, Pokedex.MUK, Pokedex.MAROWAK, Pokedex.LAPRAS,
                                      Pokedex.KANGASKHAN, Pokedex.KABUTOPS, Pokedex.IVYSAUR, Pokedex.GYARADOS,
                                      Pokedex.GOLEM, Pokedex.GENGAR, Pokedex.EXEGGUTOR, Pokedex.DRAGONAIR,
                                      Pokedex.DEWGONG, Pokedex.CHARMELEON, Pokedex.BEEDRILL, Pokedex.ALAKAZAM]
        rarities[Rarity.RARE] = [Pokedex.WIGGLYTUFF, Pokedex.WEEZING, Pokedex.TENTACRUEL, Pokedex.TANGELA,
                                 Pokedex.STARMIE, Pokedex.SNORLAX, Pokedex.SCYTHER, Pokedex.SEAKING, Pokedex.SEADRA,
                                 Pokedex.RHYDON, Pokedex.RAPIDASH, Pokedex.PRIMEAPE, Pokedex.PORYGON, Pokedex.POLIWHIRL,
                                 Pokedex.PARASECT, Pokedex.ONIX, Pokedex.OMANYTE, Pokedex.NINETALES, Pokedex.NIDORINO,
                                 Pokedex.NIDORINA, Pokedex.MR_MIME, Pokedex.MAGMAR, Pokedex.MACHOKE, Pokedex.MACHAMP,
                                 Pokedex.LICKITUNG, Pokedex.KINGLER, Pokedex.JOLTEON, Pokedex.HYPNO, Pokedex.HITMONCHAN,
                                 Pokedex.GLOOM, Pokedex.GOLDUCK, Pokedex.FLAREON, Pokedex.FEAROW, Pokedex.FARFETCHD,
                                 Pokedex.ELECTABUZZ, Pokedex.DUGTRIO, Pokedex.DRATINI, Pokedex.DODRIO, Pokedex.CLOYSTER,
                                 Pokedex.CHANSEY, Pokedex.BUTTERFREE, Pokedex.ARCANINE, Pokedex.AERODACTYL]
        rarities[Rarity.UNCOMMON] = [Pokedex.VULPIX, Pokedex.TENTACOOL, Pokedex.STARYU, Pokedex.SQUIRTLE,
                                     Pokedex.SPEAROW, Pokedex.SHELLDER, Pokedex.SEEL, Pokedex.SANDSLASH,
                                     Pokedex.RHYHORN, Pokedex.RATICATE, Pokedex.PSYDUCK, Pokedex.PONYTA,
                                     Pokedex.PIKACHU, Pokedex.PIDGEOTTO, Pokedex.PERSIAN, Pokedex.METAPOD,
                                     Pokedex.MAGNETON, Pokedex.KOFFING, Pokedex.KADABRA, Pokedex.KABUTO, Pokedex.KAKUNA,
                                     Pokedex.JYNX, Pokedex.JIGGLYPUFF, Pokedex.HORSEA, Pokedex.HITMONLEE,
                                     Pokedex.HAUNTER, Pokedex.GROWLITHE, Pokedex.GRIMER, Pokedex.GRAVELER,
                                     Pokedex.GOLBAT, Pokedex.EXEGGCUTE, Pokedex.ELECTRODE, Pokedex.CUBONE,
                                     Pokedex.CLEFAIRY, Pokedex.CHARMANDER, Pokedex.BULBASAUR, Pokedex.ARBOK,
                                     Pokedex.ABRA]
        rarities[Rarity.COMMON] = [Pokedex.WEEDLE, Pokedex.VOLTORB, Pokedex.VENONAT, Pokedex.SLOWPOKE,
                                   Pokedex.SANDSHREW, Pokedex.POLIWAG, Pokedex.PARAS, Pokedex.ODDISH,
                                   Pokedex.NIDORAN_MALE, Pokedex.NIDORAN_FEMALE, Pokedex.MEOWTH, Pokedex.MANKEY,
                                   Pokedex.MAGNEMITE, Pokedex.MAGIKARP, Pokedex.MACHOP, Pokedex.KRABBY, Pokedex.GOLDEEN,
                                   Pokedex.GEODUDE, Pokedex.GASTLY, Pokedex.EEVEE, Pokedex.EKANS, Pokedex.DROWZEE,
                                   Pokedex.DODUO, Pokedex.DIGLETT, Pokedex.CATERPIE, Pokedex.BELLSPROUT]
        rarities[Rarity.CRITTER] = [Pokedex.ZUBAT, Pokedex.PIDGEY, Pokedex.RATTATA]

        for rarity in rarities:
            if self.value in rarities[rarity]:
                return rarity

    def __str__(self):
        if self.value == 1:
            return "フシギダネ"
        elif self.value == 2:
            return "フシギソウ"
        elif self.value == 3:
            return "フシギバナ"
        elif self.value == 4:
            return "ヒトカゲ"
        elif self.value == 5:
            return "リザード"
        elif self.value == 6:
            return "リザードン"
        elif self.value == 7:
            return "ゼニガメ"
        elif self.value == 8:
            return "カメール"
        elif self.value == 9:
            return "カメックス"
        elif self.value == 10:
            return "キャタピー"
        elif self.value == 11:
            return "トランセル"
        elif self.value == 12:
            return "バタフリー"
        elif self.value == 13:
            return "ビードル"
        elif self.value == 14:
            return "コクーン"
        elif self.value == 15:
            return "スピアー"
        elif self.value == 16:
            return "ポッポ"
        elif self.value == 17:
            return "ピジョン"
        elif self.value == 18:
            return "ピジョット"
        elif self.value == 19:
            return "コラッタ"
        elif self.value == 20:
            return "ラッタ"
        elif self.value == 21:
            return "オニスズメ"
        elif self.value == 22:
            return "オニドリル"
        elif self.value == 23:
            return "アーボ"
        elif self.value == 24:
            return "アーボック"
        elif self.value == 25:
            return "ピカチュウ"
        elif self.value == 26:
            return "ライチュウ"
        elif self.value == 27:
            return "サンド"
        elif self.value == 28:
            return "サンドパン"
        elif self.value == 29:
            return "ニドラン♀"
        elif self.value == 30:
            return "ニドリーナ"
        elif self.value == 31:
            return "ニドクイン"
        elif self.value == 32:
            return "ニドラン♂"
        elif self.value == 33:
            return "ニドリーノ"
        elif self.value == 34:
            return "ニドキング"
        elif self.value == 35:
            return "ピッピ"
        elif self.value == 36:
            return "ピクシー"
        elif self.value == 37:
            return "ロコン"
        elif self.value == 38:
            return "キュウコン"
        elif self.value == 39:
            return "プリン"
        elif self.value == 40:
            return "プクリン"
        elif self.value == 41:
            return "ズバット"
        elif self.value == 42:
            return "ゴルバット"
        elif self.value == 43:
            return "ナゾノクサ"
        elif self.value == 44:
            return "クサイハナ"
        elif self.value == 45:
            return "ラフレシア"
        elif self.value == 46:
            return "パラス"
        elif self.value == 47:
            return "パラセクト"
        elif self.value == 48:
            return "コンパン"
        elif self.value == 49:
            return "モルフォン"
        elif self.value == 50:
            return "ディグダ"
        elif self.value == 51:
            return "ダグトリオ"
        elif self.value == 52:
            return "ニャース"
        elif self.value == 53:
            return "ペルシアン"
        elif self.value == 54:
            return "コダック"
        elif self.value == 55:
            return "ゴルダック"
        elif self.value == 56:
            return "マンキー"
        elif self.value == 57:
            return "オコリザル"
        elif self.value == 58:
            return "ガーディ"
        elif self.value == 59:
            return "ウインディ"
        elif self.value == 60:
            return "ニョロモ"
        elif self.value == 61:
            return "ニョロゾ"
        elif self.value == 62:
            return "ニョロボン"
        elif self.value == 63:
            return "ケーシィ"
        elif self.value == 64:
            return "ユンゲラー"
        elif self.value == 65:
            return "フーディン"
        elif self.value == 66:
            return "ワンリキー"
        elif self.value == 67:
            return "ゴーリキー"
        elif self.value == 68:
            return "カイリキー"
        elif self.value == 69:
            return "マダツボミ"
        elif self.value == 70:
            return "ウツドン"
        elif self.value == 71:
            return "ウツボット"
        elif self.value == 72:
            return "メノクラゲ"
        elif self.value == 73:
            return "ドククラゲ"
        elif self.value == 74:
            return "イシツブテ"
        elif self.value == 75:
            return "ゴローン"
        elif self.value == 76:
            return "ゴローニャ"
        elif self.value == 77:
            return "ポニータ"
        elif self.value == 78:
            return "ギャロップ"
        elif self.value == 79:
            return "ヤドン"
        elif self.value == 80:
            return "ヤドラン"
        elif self.value == 81:
            return "コイル"
        elif self.value == 82:
            return "レアコイル"
        elif self.value == 83:
            return "カモネギ"
        elif self.value == 84:
            return "ドードー"
        elif self.value == 85:
            return "ドードリオ"
        elif self.value == 86:
            return "パウワウ"
        elif self.value == 87:
            return "ジュゴン"
        elif self.value == 88:
            return "ベトベター"
        elif self.value == 89:
            return "ベトベトン"
        elif self.value == 90:
            return "シェルダー"
        elif self.value == 91:
            return "パルシェン"
        elif self.value == 92:
            return "ゴース"
        elif self.value == 93:
            return "ゴースト"
        elif self.value == 94:
            return "ゲンガー"
        elif self.value == 95:
            return "イワーク"
        elif self.value == 96:
            return "スリープ"
        elif self.value == 97:
            return "スリーパー"
        elif self.value == 98:
            return "クラブ"
        elif self.value == 99:
            return "キングラー"
        elif self.value == 100:
            return "ビリリダマ"
        elif self.value == 101:
            return "マルマイン"
        elif self.value == 102:
            return "タマタマ"
        elif self.value == 103:
            return "ナッシー"
        elif self.value == 104:
            return "カラカラ"
        elif self.value == 105:
            return "ガラガラ"
        elif self.value == 106:
            return "サワムラー"
        elif self.value == 107:
            return "エビワラー"
        elif self.value == 108:
            return "ベロリンガ"
        elif self.value == 109:
            return "ドガース"
        elif self.value == 110:
            return "マタドガス"
        elif self.value == 111:
            return "サイホーン"
        elif self.value == 112:
            return "サイドン"
        elif self.value == 113:
            return "ラッキー"
        elif self.value == 114:
            return "モンジャラ"
        elif self.value == 115:
            return "ガルーラ"
        elif self.value == 116:
            return "タッツー"
        elif self.value == 117:
            return "シードラ"
        elif self.value == 118:
            return "トサキント"
        elif self.value == 119:
            return "アズマオウ"
        elif self.value == 120:
            return "ヒトデマン"
        elif self.value == 121:
            return "スターミー"
        elif self.value == 122:
            return "バリヤード"
        elif self.value == 123:
            return "ストライク"
        elif self.value == 124:
            return "ルージュラ"
        elif self.value == 125:
            return "エレブー"
        elif self.value == 126:
            return "ブーバー"
        elif self.value == 127:
            return "カイロス"
        elif self.value == 128:
            return "ケンタロス"
        elif self.value == 129:
            return "コイキング"
        elif self.value == 130:
            return "ギャラドス"
        elif self.value == 131:
            return "ラプラス"
        elif self.value == 132:
            return "メタモン"
        elif self.value == 133:
            return "イーブイ"
        elif self.value == 134:
            return "シャワーズ"
        elif self.value == 135:
            return "サンダース"
        elif self.value == 136:
            return "ブースター"
        elif self.value == 137:
            return "ポリゴン"
        elif self.value == 138:
            return "オムナイト"
        elif self.value == 139:
            return "オムスター"
        elif self.value == 140:
            return "カブト"
        elif self.value == 141:
            return "カブトプス"
        elif self.value == 142:
            return "プテラ"
        elif self.value == 143:
            return "カビゴン"
        elif self.value == 144:
            return "フリーザー"
        elif self.value == 145:
            return "サンダー"
        elif self.value == 146:
            return "ファイヤー"
        elif self.value == 147:
            return "ミニリュウ"
        elif self.value == 148:
            return "ハクリュー"
        elif self.value == 149:
            return "カイリュー"
        elif self.value == 150:
            return "ミュウツー"
        elif self.value == 151:
            return "ミュウ"
        else:
            return "不明"


class Rarity(enum.Enum):
    CRITTER = 0
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    VERY_RARE = 4
    EPIC = 5
    LEGENDARY = 6
    MYTHIC = 7

    def __str__(self):
        if self.value == 0:
            return "E"
        elif self.value == 1:
            return "D"
        elif self.value == 2:
            return "C"
        elif self.value == 3:
            return "B"
        elif self.value == 4:
            return "A"
        elif self.value == 5:
            return "S"
        elif self.value == 6:
            return "SS"
        elif self.value == 7:
            return "SSS"
        else:
            return "???"
