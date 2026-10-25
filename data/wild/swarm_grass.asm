; Pokémon swarms in grass

SwarmGrassWildMons:

; Dunsparce swarm
	map_id DARK_CAVE_VIOLET_ENTRANCE
	db 4 percent, 4 percent, 4 percent ; encounter rates: morn/day/nite
	; morn
	db 3, BULBASAUR
	db 3, KANGASKHAN
	db 2, IGGLYBUFF
	db 2, BULBASAUR
	db 2, KANGASKHAN
	db 4, KANGASKHAN
	db 4, KANGASKHAN
	; day
	db 3, BULBASAUR
	db 3, KANGASKHAN
	db 2, IGGLYBUFF
	db 2, BULBASAUR
	db 2, KANGASKHAN
	db 4, KANGASKHAN
	db 4, KANGASKHAN
	; nite
	db 3, BULBASAUR
	db 3, KANGASKHAN
	db 2, IGGLYBUFF
	db 2, BULBASAUR
	db 2, KANGASKHAN
	db 4, KANGASKHAN
	db 4, KANGASKHAN

; Yanma swarm
	map_id ROUTE_35
	db 10 percent, 10 percent, 10 percent ; encounter rates: morn/day/nite
	; morn
	db 12, ODDISH
	db 12, MACHOP
	db 12, MR__MIME
	db 14, MR__MIME
	db 14, CHARMANDER
	db 10, LAPRAS
	db 10, LAPRAS
	; day
	db 12, ODDISH
	db 12, MACHOP
	db 12, MR__MIME
	db 14, MR__MIME
	db 14, CHARMANDER
	db 10, LAPRAS
	db 10, LAPRAS
	; nite
	db 12, ODDISH
	db 12, MACHOP
	db 12, MR__MIME
	db 14, MR__MIME
	db 14, TENTACOOL
	db 10, LAPRAS
	db 10, LAPRAS

	db -1 ; end
