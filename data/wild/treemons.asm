TreeMons::
; entries correspond to TREEMON_SET_* constants
	table_width 2, TreeMons
	dw TreeMonSet_City
	dw TreeMonSet_Canyon
	dw TreeMonSet_Town
	dw TreeMonSet_Route
	dw TreeMonSet_Kanto
	dw TreeMonSet_Lake
	dw TreeMonSet_Forest
	assert_table_length NUM_TREEMON_SETS

RockSmashMons::
	; broke off from the above table, for nayru's pokedex
	; delineation was needed because there is no 'rare' table for rocksmash
	table_width 2, RockSmashMons
	dw TreeMonSet_Rock
	assert_table_length NUM_ROCKSMASH_SETS
; Two tables each (common, rare).
; Structure:
;	db  %, species, level

TreeMonSet_City:
TreeMonSet_Canyon:
; common
	db 50, PORYGON,    10
	db 15, PORYGON,    10
	db 15, PORYGON,    10
	db 10, TAUROS,     10
	db  5, TAUROS,     10
	db  5, TAUROS,     10
	db -1
; rare
	db 50, PORYGON,    10
	db 15, WOBBUFFET,  10
	db 15, WOBBUFFET,  10
	db 10, TAUROS,     10
	db  5, TAUROS,     10
	db  5, TAUROS,     10
	db -1

TreeMonSet_Town:
; common
	db 50, PORYGON,    10
	db 15, SLOWPOKE,   10
	db 15, PORYGON,    10
	db 10, TAUROS,     10
	db  5, TAUROS,     10
	db  5, TAUROS,     10
	db -1
; rare
	db 50, PORYGON,    10
	db 15, WOBBUFFET,  10
	db 15, WOBBUFFET,  10
	db 10, TAUROS,     10
	db  5, TAUROS,     10
	db  5, TAUROS,     10
	db -1

TreeMonSet_Route:
; common
	db 50, TENTACOOL,  10
	db 15, KOFFING,    10
	db 15, CHANSEY,    10
	db 10, MARILL,     10
	db  5, MARILL,     10
	db  5, MARILL,     10
	db -1
; rare
	db 50, TENTACOOL,  10
	db 15, ELEKID,     10
	db 15, ELEKID,     10
	db 10, MARILL,     10
	db  5, MARILL,     10
	db  5, MARILL,     10
	db -1

TreeMonSet_Kanto:
; common
	db 50, TENTACOOL,  10
	db 15, SLOWPOKE,   10
	db 15, TENTACOOL,  10
	db 10, MARILL,     10
	db  5, MARILL,     10
	db  5, MARILL,     10
	db -1
; rare
	db 50, TENTACOOL,  10
	db 15, ELEKID,     10
	db 15, ELEKID,     10
	db 10, MARILL,     10
	db  5, MARILL,     10
	db  5, MARILL,     10
	db -1

TreeMonSet_Lake:
; common
	db 50, TENTACOOL,  10
	db 15, VENONAT,    10
	db 15, TENTACOOL,  10
	db 10, MARILL,     10
	db  5, MARILL,     10
	db  5, MARILL,     10
	db -1
; rare
	db 50, TENTACOOL,  10
	db 15, ELEKID,     10
	db 15, ELEKID,     10
	db 10, MARILL,     10
	db  5, MARILL,     10
	db  5, MARILL,     10
	db -1

TreeMonSet_Forest:
; common
	db 50, TENTACOOL,  10
	db 15, ELEKID,     10
	db 15, ELEKID,     10
	db 10, TENTACRUEL, 10
	db  5, TYRANITAR,  10
	db  5, DRAGONITE,  10
	db -1
; rare
	db 50, TENTACOOL,  10
	db 15, LARVITAR,   10
	db 15, DRATINI,    10
	db 10, TENTACOOL,  10
	db  5, PUPITAR,    10
	db  5, DRAGONAIR,  10
	db -1

; Rock smash sets dont have common/rare tables
; can have as many entries as you want as long as the % adds up to 100
; feel free to add new rock smash sets
TreeMonSet_Rock:
	db 90, SWINUB,     15
	db 10, FARFETCH_D, 15
	db -1
