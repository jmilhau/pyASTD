Structure des machines :


machine['MACHINE']              nom de la machine (string)
machine['SETS']                 liste d'ensembles (string)
machine['VARIABLES']            liste variables (string)
machine['INVARIANT']            liste d'invariants (string)
machine['INITIALISATION']       liste d'affectations (string)
machine['OPERATIONS']           dictionnaire { nomOp -> op }

machine['OPERATIONS'][sigma]    dictionnaire 

machine['OPERATIONS']['sigma']['name']          normalement égal à 'sigma'
machine['OPERATIONS']['sigma']['param']         tuple des paramètres
machine['OPERATIONS']['sigma']['PRE']           liste des précondition en disjonction
machine['OPERATIONS']['sigma']['THEN']          liste de tuple (condition,substitution) pour les SELECTs