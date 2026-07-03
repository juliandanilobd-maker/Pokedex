## INFORME DE COBERTURA

Name                                    Stmts   Miss  Cover   Missing
---------------------------------------------------------------------
app\__init__.py                             0      0   100%
app\api\__init__.py                         0      0   100%
app\api\routes.py                         186     32    83%   229-263, 543-565, 586-612
app\cache\__init__.py                       0      0   100%
app\cache\cache_manager.py                 35      0   100%
app\clients\__init__.py                     0      0   100%
app\clients\pokeapi_client.py              56      3    95%   43, 138-139
app\core\__init__.py                        0      0   100%
app\core\config.py                         29      1    97%   67
app\core\constants.py                       0      0   100%
app\core\logging_config.py                 23      0   100%
app\data\__init__.py                        0      0   100%
app\data\data\__init__.py                   0      0   100%
app\data\scripts\__init__.py                0      0   100%
app\data\scripts\dataset_generator.py      83      0   100%
app\dependencies\__init__.py                0      0   100%
app\dependencies\dependencias.py           41      6    85%   30-31, 64, 68, 72, 76
app\models\__init__.py                      0      0   100%
app\models\pokemon_models.py              119      0   100%
app\parsers\__init__.py                     0      0   100%
app\parsers\evolution_parser.py            29      2    93%   22-24
app\parsers\pokemon_parser.py              30      3    90%   116-125
app\services\__init__.py                    0      0   100%
app\services\alerts_service.py             53      0   100%
app\services\analyzer_service.py           60      0   100%
app\services\battle_service.py             38      0   100%
app\services\evolution_service.py          11      0   100%
app\services\filter_service.py             55      0   100%
app\services\pokemon_service.py            17      2    88%   41-42
app\services\predictor_service.py          40      1    98%   102
app\services\reporter_service.py           64      1    98%   167
app\services\simulator_service.py          65      2    97%   185-186
app\services\team_service.py              104      3    97%   188, 204, 230
app\utils\__init__.py                       0      0   100%
---------------------------------------------------------------------
TOTAL                                    1138     56    95%