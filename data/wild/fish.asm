time_group EQUS "0," ; use the nth TimeFishGroups entry

fishgroup: MACRO
; chance, old rod, good rod, super rod
	db \1
	dw \2, \3, \4
ENDM

FishGroups:
; entries correspond to FISHGROUP_* constants
	table_width FISHGROUP_DATA_LENGTH, FishGroups
	fishgroup 50 percent + 1, .Shore_Old,            .Shore_Good,            .Shore_Super
	fishgroup 50 percent + 1, .Ocean_Old,            .Ocean_Good,            .Ocean_Super
	fishgroup 50 percent + 1, .Lake_Old,             .Lake_Good,             .Lake_Super
	fishgroup 50 percent + 1, .Pond_Old,             .Pond_Good,             .Pond_Super
	fishgroup 50 percent + 1, .Dratini_Old,          .Dratini_Good,          .Dratini_Super
	fishgroup 50 percent + 1, .Qwilfish_Swarm_Old,   .Qwilfish_Swarm_Good,   .Qwilfish_Swarm_Super
	fishgroup 50 percent + 1, .Remoraid_Swarm_Old,   .Remoraid_Swarm_Good,   .Remoraid_Swarm_Super
	fishgroup 50 percent + 1, .Gyarados_Old,         .Gyarados_Good,         .Gyarados_Super
	fishgroup 50 percent + 1, .Dratini_2_Old,        .Dratini_2_Good,        .Dratini_2_Super
	fishgroup 50 percent + 1, .WhirlIslands_Old,     .WhirlIslands_Good,     .WhirlIslands_Super
	fishgroup 50 percent + 1, .Qwilfish_Old,         .Qwilfish_Good,         .Qwilfish_Super
	fishgroup 50 percent + 1, .Remoraid_Old,         .Remoraid_Good,         .Remoraid_Super
	fishgroup 50 percent + 1, .Qwilfish_NoSwarm_Old, .Qwilfish_NoSwarm_Good, .Qwilfish_NoSwarm_Super
	assert_table_length NUM_FISHGROUPS

.Shore_Old:
	db  70 percent + 1, RATTATA,    10
	db  85 percent + 1, RATTATA,    10
	db 100 percent,     SWINUB,     10
.Shore_Good:
	db  35 percent,     RATTATA,    20
	db  70 percent,     SWINUB,     20
	db  90 percent + 1, SWINUB,     20
	db 100 percent,     time_group 0
.Shore_Super:
	db  40 percent,     SWINUB,     40
	db  70 percent,     time_group 1
	db  90 percent + 1, SWINUB,     40
	db 100 percent,     PILOSWINE,  40

.Ocean_Old:
	db  70 percent + 1, RATTATA,    10
	db  85 percent + 1, RATTATA,    10
	db 100 percent,     HOOTHOOT,   10
.Ocean_Good:
	db  35 percent,     RATTATA,    20
	db  70 percent,     HOOTHOOT,   20
	db  90 percent + 1, KABUTO,     20
	db 100 percent,     time_group 2
.Ocean_Super:
	db  40 percent,     KABUTO,     40
	db  70 percent,     time_group 3
	db  90 percent + 1, NOCTOWL,    40
	db 100 percent,     KABUTOPS,   40

.Lake_Old:
	db  70 percent + 1, RATTATA,    10
	db  85 percent + 1, RATTATA,    10
	db 100 percent,     SCYTHER,    10
.Lake_Good:
	db  35 percent,     RATTATA,    20
	db  70 percent,     SCYTHER,    20
	db  90 percent + 1, SCYTHER,    20
	db 100 percent,     time_group 4
.Lake_Super:
	db  40 percent,     SCYTHER,    40
	db  70 percent,     time_group 5
	db  90 percent + 1, RATTATA,    40
	db 100 percent,     SCIZOR,     40

.Pond_Old:
	db  70 percent + 1, RATTATA,    10
	db  85 percent + 1, RATTATA,    10
	db 100 percent,     MAREEP,     10
.Pond_Good:
	db  35 percent,     RATTATA,    20
	db  70 percent,     MAREEP,     20
	db  90 percent + 1, MAREEP,     20
	db 100 percent,     time_group 6
.Pond_Super:
	db  40 percent,     MAREEP,     40
	db  70 percent,     time_group 7
	db  90 percent + 1, RATTATA,    40
	db 100 percent,     MAREEP,     40

.Dratini_Old:
	db  70 percent + 1, RATTATA,    10
	db  85 percent + 1, RATTATA,    10
	db 100 percent,     RATTATA,    10
.Dratini_Good:
	db  35 percent,     RATTATA,    20
	db  70 percent,     RATTATA,    20
	db  90 percent + 1, RATTATA,    20
	db 100 percent,     time_group 8
.Dratini_Super:
	db  40 percent,     RATTATA,    40
	db  70 percent,     time_group 9
	db  90 percent + 1, RATTATA,    40
	db 100 percent,     KAKUNA,     40

.Qwilfish_Swarm_Old:
	db  70 percent + 1, RATTATA,    5
	db  85 percent + 1, RATTATA,    5
	db 100 percent,     TANGELA,    5
.Qwilfish_Swarm_Good:
	db  35 percent,     RATTATA,    20
	db  70 percent,     TANGELA,    20
	db  90 percent + 1, TANGELA,    20
	db 100 percent,     time_group 10
.Qwilfish_Swarm_Super:
	db  40 percent,     TANGELA,    40
	db  70 percent,     time_group 11
	db  90 percent + 1, TANGELA,    40
	db 100 percent,     TANGELA,    40

.Remoraid_Swarm_Old:
	db  70 percent + 1, RATTATA,    10
	db  85 percent + 1, RATTATA,    10
	db 100 percent,     SEEL,       10
.Remoraid_Swarm_Good:
	db  35 percent,     RATTATA,    20
	db  70 percent,     SEEL,       20
	db  90 percent + 1, SEEL,       20
	db 100 percent,     time_group 12
.Remoraid_Swarm_Super:
	db  40 percent,     SEEL,       40
	db  70 percent,     time_group 13
	db  90 percent + 1, SEEL,       40
	db 100 percent,     SEEL,       40

.Gyarados_Old:
	db  70 percent + 1, RATTATA,    10
	db  85 percent + 1, RATTATA,    10
	db 100 percent,     RATTATA,    10
.Gyarados_Good:
	db  35 percent,     RATTATA,    20
	db  70 percent,     RATTATA,    20
	db  90 percent + 1, RATTATA,    20
	db 100 percent,     time_group 14
.Gyarados_Super:
	db  40 percent,     RATTATA,    40
	db  70 percent,     time_group 15
	db  90 percent + 1, RATTATA,    40
	db 100 percent,     RATTATA,    40

.Dratini_2_Old:
	db  70 percent + 1, RATTATA,    10
	db  85 percent + 1, RATTATA,    10
	db 100 percent,     RATTATA,    10
.Dratini_2_Good:
	db  35 percent,     RATTATA,    10
	db  70 percent,     RATTATA,    10
	db  90 percent + 1, RATTATA,    10
	db 100 percent,     time_group 16
.Dratini_2_Super:
	db  40 percent,     RATTATA,    10
	db  70 percent,     time_group 17
	db  90 percent + 1, RATTATA,    10
	db 100 percent,     KAKUNA,     10

.WhirlIslands_Old:
	db  70 percent + 1, RATTATA,    10
	db  85 percent + 1, RATTATA,    10
	db 100 percent,     SWINUB,     10
.WhirlIslands_Good:
	db  35 percent,     RATTATA,    20
	db  70 percent,     SWINUB,     20
	db  90 percent + 1, SWINUB,     20
	db 100 percent,     time_group 18
.WhirlIslands_Super:
	db  40 percent,     SWINUB,     40
	db  70 percent,     time_group 19
	db  90 percent + 1, PILOSWINE,  40
	db 100 percent,     SKIPLOOM,   40

.Qwilfish_NoSwarm_Old:
.Qwilfish_Old:
	db  70 percent + 1, RATTATA,    10
	db  85 percent + 1, RATTATA,    10
	db 100 percent,     HOOTHOOT,   10
.Qwilfish_NoSwarm_Good:
.Qwilfish_Good:
	db  35 percent,     RATTATA,    20
	db  70 percent,     HOOTHOOT,   20
	db  90 percent + 1, HOOTHOOT,   20
	db 100 percent,     time_group 20
.Qwilfish_NoSwarm_Super:
.Qwilfish_Super:
	db  40 percent,     HOOTHOOT,   40
	db  70 percent,     time_group 21
	db  90 percent + 1, RATTATA,    40
	db 100 percent,     TANGELA,    40

.Remoraid_Old:
	db  70 percent + 1, RATTATA,    10
	db  85 percent + 1, RATTATA,    10
	db 100 percent,     MAREEP,     10
.Remoraid_Good:
	db  35 percent,     RATTATA,    20
	db  70 percent,     MAREEP,     20
	db  90 percent + 1, MAREEP,     20
	db 100 percent,     time_group 6
.Remoraid_Super:
	db  40 percent,     MAREEP,     40
	db  70 percent,     time_group 7
	db  90 percent + 1, RATTATA,    40
	db 100 percent,     SEEL,       40

TimeFishGroups:
	;  day              nite
	db MILTANK,    20,  STARYU,     20 ; 0
	db MILTANK,    40,  STARYU,     40 ; 1
	db DIGLETT,    20,  SHELLDER,   20 ; 2
	db DIGLETT,    40,  SHELLDER,   40 ; 3
	db SCYTHER,    20,  GOLDEEN,    20 ; 4
	db SCYTHER,    40,  GOLDEEN,    40 ; 5
	db MAREEP,     20,  POLIWAG,    20 ; 6
	db MAREEP,     40,  POLIWAG,    40 ; 7
	db WEEDLE,     20,  DRATINI,    20 ; 8
	db WEEDLE,     40,  DRATINI,    40 ; 9
	db TANGELA,    20,  QWILFISH,   20 ; 10
	db TANGELA,    40,  QWILFISH,   40 ; 11
	db SEEL,       20,  REMORAID,   20 ; 12
	db SEEL,       40,  REMORAID,   40 ; 13
	db RATICATE,   20,  GYARADOS,   20 ; 14
	db RATICATE,   40,  GYARADOS,   40 ; 15
	db WEEDLE,     10,  DRATINI,    10 ; 16
	db WEEDLE,     10,  DRATINI,    10 ; 17
	db HOPPIP,     20,  HORSEA,     20 ; 18
	db HOPPIP,     40,  HORSEA,     40 ; 19
	db HOOTHOOT,   20,  TENTACOOL,  20 ; 20
	db HOOTHOOT,   40,  TENTACOOL,  40 ; 21
	
FishGroups_Names::
	table_width 2, FishGroups_Names
	dw Group1_Name
	dw Group2_Name
	dw Group3_Name
	dw Group4_Name
	dw Group5_Name
	dw Group6_Name
	dw Group7_Name
	dw Group8_Name
	dw Group9_Name
	dw Group10_Name
	dw Group11_Name
	dw Group12_Name
	dw Group13_Name
	assert_table_length NUM_FISHGROUPS ; (13, NONE is not included in the count)

Group1_Name:
    db " SHORE@"
Group2_Name:
    db " OCEAN@"
Group3_Name:
    db " LAKE@"
Group4_Name:
    db " POND@"
Group5_Name:
    db " WEEDLE@"
Group6_Name:
    db " TANGELA SWARM@"
Group7_Name:
    db " SEEL SWARM@"
Group8_Name:
    db " RATICATE@"
Group9_Name:
    db " ROUTE 45@"
Group10_Name:
    db " WHIRL ISLE@"
Group11_Name:
    db " TANGELA@"
Group12_Name:
    db " SEEL@"
Group13_Name:
    db " ROUTE 12@"

GetFishGroupName:
; given fishing group num in 'a'
; return str ptr in 'de'
	dec a
	add a ; doubles the index since ptrs are 2 bytes
	ld hl, FishGroups_Names
	ld d, 0
	ld e, a
	add hl, de
	ld e, [hl]
	inc hl
	ld d, [hl]
	ret

GetMapsFishGroup::
	dec d ; map num
	dec e ; map group
	push de
	ld d, 0
	; 'e' is the map group
	ld hl, MapGroupPointers
	add hl, de ; since ptrs are 2 bytes, double the index
	add hl, de
	ld a, BANK(MapGroupPointers)
	call GetFarWord
	pop de
	ld a, d ; map num becomes the index, do the same as map group
	ld bc, MAP_LENGTH
	; hl is pointing to map group ptr
	call AddNTimes ;  Add bc * a to hl.
	; fish group is the very last byte in the entry
	ld bc, MAP_LENGTH - 1
	add hl, bc
	ld a, BANK(MapGroupPointers)
	call GetFarByte
	; ld a, [hl] ; fishing group
	cp FISHGROUP_NONE
	jr z, .fishgroup_none
	call GetFishGroupName
	; ptr to fishgroup name is in de
	ret
.fishgroup_none
	xor a
	ld d, a
	ld e, a
	ret
